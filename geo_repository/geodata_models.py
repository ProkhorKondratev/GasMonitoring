from django.contrib.gis.db import models
from pathlib import Path
import sqlite3
from django.contrib.gis.geos import Point, MultiPoint


class FileManager(models.Manager):
    @staticmethod
    def get_rectangle(geo_file):
        if not geo_file.rectangle:
            conn = sqlite3.connect(geo_file.path)
            cursor = conn.cursor()
            cursor.execute("SELECT min_x, min_y, max_x, max_y FROM gpkg_contents")
            result = cursor.fetchone()
            conn.close()
            return MultiPoint([
                Point(result[0], result[1], srid=3857),
                Point(result[2], result[3], srid=3857)], srid=3857) \
                .envelope.transform(4326, clone=True)

    def create(self, **kwargs):
        file = super().create(**kwargs)
        file.name = Path(file.path).name
        file.rectangle = FileManager.get_rectangle(file)

        file.save()
        return file


class File(models.Model):

    objects = FileManager()

    name = models.CharField(
        verbose_name='Имя',
        db_column='name',
        max_length=255,
        null=True,
        blank=True,
        help_text='Имя файла',
    )

    path = models.CharField(
        verbose_name='Полный путь',
        db_column='path',
        max_length=255,
        null=False,
        blank=False,
        help_text='Полный путь до файла или директории',
    )

    created = models.DateTimeField(
        verbose_name='Дата создания',
        db_column='created',
        auto_now_add=True,
        help_text='Дата создания',
    )

    size = models.BigIntegerField(
        verbose_name='Размер',
        db_column='size',
        null=True,
        blank=True,
        help_text='Размер в байтах',
    )

    def save(self, *args, **kwargs):
        if self.name is None:
            self.name = Path(self.path).name
        if Path(self.path).exists() and Path(self.path).is_file():
            self.size = Path(self.path).stat().st_size
        super(File, self).save(*args, **kwargs)

    def __str__(self):
        return f'Файл: {self.name if self.name else self.path}'

    class Meta:
        abstract = True


class Folder(File):
    def __str__(self):
        return f'Папка: {self.name if self.name else self.path}'

    def save(self, *args, **kwargs):
        if self.name is None:
            self.name = Path(self.path).name
        if self.size is None and Path(self.path).exists() and Path(self.path).is_dir():
            self.size = sum(f.stat().st_size for f in Path(self.path).rglob('*') if f.is_file())
        super(Folder, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class GeoDataFileSettings(models.Model):
    """
    Для хранения схемы данных файла с геоданными.
    """
    rectangle = models.PolygonField(
        verbose_name='Охват',
        srid=4326,
        dim=2,
        null=True,
        blank=True,
        help_text='Охват тайлового слоя',
    )

    is_show = models.BooleanField(
        verbose_name='Показывать на карте',
        help_text='Показывать этот слой на карте',
        default=True
    )

    minimum_level = models.IntegerField(
        verbose_name='Минимальный масштаб',
        null=True,
        blank=True,
        help_text='Минимальный масштаб',
        default=0
    )

    maximum_level = models.IntegerField(
        verbose_name='Максимальный масштаб',
        null=True,
        blank=True,
        help_text='Максимальный масштаб',
        default=25
    )

    tileWidth = models.IntegerField(
        verbose_name='Ширина тайла',
        null=True,
        blank=True,
        help_text='Ширина тайла',
        default=256
    )

    tileHeight = models.IntegerField(
        verbose_name='Высота тайла',
        null=True,
        blank=True,
        help_text='Высота тайла',
        default=256
    )

    class Meta:
        abstract = True


class GeoDataTypes(models.TextChoices):
    """
    Тип геоданных в файле.

    """

    ORTHO = 'ortho', 'Ортофотоплан'
    DEM = 'dem', 'Цифровая модель рельефа'


class GeoDataFile(File, GeoDataFileSettings):

    data_type = models.CharField(
        verbose_name='Тип данных',
        db_column='data_type',
        max_length=255,
        null=True,
        blank=True,
        choices=GeoDataTypes.choices,
        default=GeoDataTypes.ORTHO,
        help_text='Тип данных',
    )


    def __str__(self):
        return f'Геоданные: {self.name if self.name else self.path}'

    def save(self, *args, **kwargs):
        if self.path.endswith('ortho.gpkg'):
            self.name = GeoDataTypes.ORTHO.label
            self.data_type = GeoDataTypes.ORTHO
        elif self.path.endswith('dem.gpkg'):
            self.name = GeoDataTypes.DEM.label
            self.data_type = GeoDataTypes.DEM

        self.rectangle = FileManager.get_rectangle(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Файл с геоданными'
        verbose_name_plural = 'Файлы с геоданными'
        db_table = 'geo_data_files'
        ordering = ['-created']
