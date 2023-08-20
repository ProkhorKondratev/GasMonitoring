from django.contrib.gis.db import models
from .mixins import LifeCycleModelMixin


class ProtectedObject(models.Model):
    is_show = models.BooleanField(
        verbose_name='Показывать на карте',
        help_text='Показывать этот объект на карте',
        default=True
    )
    name = models.CharField(
        max_length=254,
        verbose_name='Имя',
        help_text='Название охраняемого объекта',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание охраняемого объекта',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Охраняемый объект'
        verbose_name_plural = 'Охраняемые объекты'


class ProtectedObjectGeometry(LifeCycleModelMixin):
    parent_object = models.ForeignKey(
        ProtectedObject,
        related_name='protected_object_geometry',
        related_query_name='protected_object_geometry',
        on_delete=models.SET_NULL,
        verbose_name='Охраняемый объект',
        help_text='Охраняемый объект',
        null=True,
        blank=True,
    )
    geom = models.GeometryCollectionField(
        srid=4326,
        dim=2,
        verbose_name='Геометрия',
        help_text='Геометрия охраняемого объекта',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Геометрия охраняемого объекта'
        verbose_name_plural = 'Геометрии охраняемых объектов'

    def __str__(self):
        return self.parent_object.name if self.parent_object else 'Геометрия охраняемого объекта'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ZMR(models.Model):
    protected_object = models.ForeignKey(
        ProtectedObject,
        related_name='protection_zmr',
        related_query_name='protection_zmr',
        on_delete=models.SET_NULL,
        verbose_name='Охраняемый объект',
        help_text='Охраняемый объект',
        null=True,
        blank=True,
    )
    is_show = models.BooleanField(
        verbose_name='Показывать на карте',
        help_text='Показывать эту зону на карте',
        default=True
    )
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
        return self.name if self.name else 'Охранная зона'


class ZMRGeometry(LifeCycleModelMixin):
    parent_object = models.ForeignKey(
        ZMR,
        related_name='zmr_geometry',
        related_query_name='zmr_geometry',
        on_delete=models.SET_NULL,
        verbose_name='Зона',
        help_text='Зона минимальных расстояний объекта',
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
        return self.parent_object.name if self.parent_object else 'Геометрия зоны'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class OZ(models.Model):
    protected_object = models.ForeignKey(
        ProtectedObject,
        related_name='protection_oz',
        related_query_name='protection_oz',
        on_delete=models.SET_NULL,
        verbose_name='Охраняемый объект',
        help_text='Охраняемый объект',
        null=True,
        blank=True,
    )
    is_show = models.BooleanField(
        verbose_name='Показывать на карте',
        help_text='Показывать эту зону на карте',
        default=True
    )
    name = models.CharField(
        max_length=254,
        verbose_name='Имя',
        help_text='Название охранной зоны',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание ОЗ',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ОЗ'
        verbose_name_plural = 'ОЗ'


class OZGeometry(LifeCycleModelMixin):
    parent_object = models.ForeignKey(
        OZ,
        related_name='oz_geometry',
        related_query_name='oz_geometry',
        on_delete=models.SET_NULL,
        verbose_name='Охранная зона',
        help_text='Охранная зона объекта',
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
        verbose_name = 'Геометрия ОЗ'
        verbose_name_plural = 'Геометрии ОЗ'

    def __str__(self):
        return self.parent_object.name if self.parent_object else 'Геометрия зоны'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
