from django.db import models
from pathlib import Path


class FileManager(models.Manager):
    def create(self, **kwargs):
        if 'path' in kwargs:
            kwargs['name'] = Path(kwargs['path']).name
        return super(FileManager, self).create(**kwargs)


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
        super(GeoDataFile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Файл с геоданными'
        verbose_name_plural = 'Файлы с геоданными'
        db_table = 'geo_data_files'
        ordering = ['-created']
