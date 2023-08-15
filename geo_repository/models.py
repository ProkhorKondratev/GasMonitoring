from django.contrib.gis.db import models
from .mixins import LifeCycleModelMixin


class ZMR(models.Model):

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


class OZ(models.Model):

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

    zone = models.ForeignKey(
        OZ,
        related_name='oz_geometry',
        related_query_name='oz_geometry',
        on_delete=models.SET_NULL,
        verbose_name='Геометрия охранной зоны',
        help_text='Геометрия охранной зоны объекта',
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
        return self.zone.name if self.zone else 'Геометрия зоны'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
