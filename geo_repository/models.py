from django.contrib.gis.db import models
from .mixins import LifeCycleModelMixin


class ZMR(models.Model):
    name = models.CharField(
        max_length=254,
        verbose_name='Название',
        help_text='Название зоны',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание зоны',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Зона'
        verbose_name_plural = 'Зоны'

    def __str__(self):
        return self.name


class ZMRGeometry(LifeCycleModelMixin):
    zone = models.ForeignKey(
        ZMR,
        related_name='zmr_geometry',
        related_query_name='zmr_geometry',
        on_delete=models.SET_NULL,
        verbose_name='Зона',
        help_text='Зона',
        null=True,
        blank=True,
    )
    geom = models.MultiPolygonField(
        srid=4326,
        dim=2,
        verbose_name='Геометрия',
        help_text='Геометрия зоны',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Геометрия зоны'
        verbose_name_plural = 'Геометрии зон'

    def __str__(self):
        return self.zone.name if self.zone else 'Геометрия зоны'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
