from django.contrib.gis.db import models
from datetime import datetime


class LifeCycleModelMixin(models.Model):
    is_relevant = models.BooleanField(
        default=True,
        verbose_name='Актуальна',
        help_text='Актуальность геометрии зоны',
    )
    date_start = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата начала',
        help_text='Дата начала действия геометрии',
        null=True,
        blank=True,
    )
    date_end = models.DateTimeField(
        verbose_name='Дата окончания',
        help_text='Дата окончания действия геометрии',
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.date_end:
            self.is_relevant = False
        super().save(*args, **kwargs)


class LifeCycleUpdateMixin:
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        readonly_fields += ('date_start', 'date_end', 'is_relevant')
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (
            ('Жизненный цикл', {
                'fields': ('is_relevant', 'date_start', 'date_end'),
            }),
        )
        return fieldsets

    def perform_update(self, serializer):
        old_instance_data = serializer.instance.__dict__.copy()
        old_instance_data.pop('_state')
        old_instance_data.pop('id')
        old_instance_data.update(serializer.validated_data)

        serializer.instance.date_end = datetime.now()
        serializer.instance.save()

        serializer.Meta.model.objects.create(**old_instance_data)
        return serializer

    def save_model(self, request, obj, form, change):
        if change and 'geom' in form.changed_data:
            obj = self.model.objects.get(id=obj.id)

            new_data = form.cleaned_data.copy()
            for field in self.model._meta.fields:
                field_name = field.name
                if field_name not in form.changed_data:
                    new_data[field_name] = getattr(obj, field_name)

            new_data.pop('id')
            self.model.objects.create(**new_data)

            obj.date_end = datetime.now()

        obj.save()
        return obj
