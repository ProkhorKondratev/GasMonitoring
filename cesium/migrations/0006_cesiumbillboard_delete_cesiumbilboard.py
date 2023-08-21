# Generated by Django 4.2.4 on 2023-08-11 10:44

import cesium.models
import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cesium', '0005_cesiumbilboard_cesiumlabel_cesiumpoint_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CesiumBillboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Название объекта', max_length=255, null=True, verbose_name='Название')),
                ('show', models.BooleanField(default=True, help_text='Включает отображение объекта', verbose_name='Отображение')),
                ('heightReference', models.IntegerField(choices=[(0, 'Без изменений'), (1, 'Прижать к поверхности Земли'), (2, 'Использовать высоту относительно точки на поверхности Земли')], default=0, help_text='Выравнивание значка по высоте', verbose_name='Выравнивание по высоте')),
                ('scaleByDistance', models.JSONField(default=cesium.models.default_near_far_scalar, help_text='Определяет масштабирование объекта в зависимости от расстояния до камеры', verbose_name='Масштабирование по расстоянию')),
                ('translucencyByDistance', models.JSONField(default=cesium.models.default_near_far_scalar, help_text='Определяет прозрачность объекта в зависимости от расстояния до камеры', verbose_name='Прозрачность по расстоянию')),
                ('distanceDisplayCondition', models.JSONField(default=cesium.models.default_near_far, help_text='Устанавливает диапазон, в котором объект будет отображаться', verbose_name='Отображение по расстоянию')),
                ('scale', models.FloatField(default=1.0, help_text='Масштабирование значка', verbose_name='Масштабирование')),
                ('pixelOffset', models.JSONField(default=cesium.models.default_cartesian2, help_text='Смещение объекта относительно координат в пикселях', verbose_name='Смещение')),
                ('eyeOffset', models.JSONField(default=cesium.models.default_cartesian3, help_text='Смещение объекта относительно камеры', verbose_name='Смещение относительно камеры')),
                ('horizontalOrigin', models.IntegerField(choices=[(0, 'По центру'), (1, 'Слева'), (2, 'Справа')], default=0, help_text='Горизонтальное выравнивание объекта', verbose_name='Горизонтальное выравнивание')),
                ('verticalOrigin', models.IntegerField(choices=[(0, 'По центру'), (1, 'Снизу'), (3, 'Сверху')], default=0, help_text='Вертикальное выравнивание объекта', verbose_name='Вертикальное выравнивание')),
                ('pixelOffsetScaleByDistance', models.JSONField(default=cesium.models.default_near_far_scalar, help_text='Определяет смещение объекта в зависимости от расстояния до камеры', verbose_name='Смещение по расстоянию')),
                ('image', models.ImageField(blank=True, default=None, help_text='Иконка для визуализации типа объекта', null=True, upload_to='bilboard_images', verbose_name='Иконка типа')),
                ('color', colorfield.fields.ColorField(default='#FF000000', help_text='Цвет значка', image_field=None, max_length=18, samples=[('#FF0000', 'Красный'), ('#00FF00', 'Зеленый'), ('#0000FF', 'Синий'), ('#FFFF00', 'Желтый')], verbose_name='Цвет')),
                ('rotation', models.FloatField(default=0.0, help_text='Поворот значка', verbose_name='Поворот')),
                ('alignedAxis', models.JSONField(default=cesium.models.default_cartesian3, help_text='Ось выравнивания значка', verbose_name='Ось выравнивания')),
                ('width', models.IntegerField(default=64, help_text='Ширина значка (в пикселях)', verbose_name='Ширина')),
                ('height', models.IntegerField(default=64, help_text='Высота значка (в пикселях)', verbose_name='Высота')),
            ],
            options={
                'verbose_name': 'Стиль значка',
                'verbose_name_plural': 'Стили значков',
            },
        ),
        migrations.DeleteModel(
            name='CesiumBilboard',
        ),
    ]
