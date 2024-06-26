# Generated by Django 4.2.4 on 2023-08-11 11:22

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cesium', '0010_alter_cesiumpolyline_depthfailmaterial_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cesiumbillboard',
            name='scale',
            field=models.FloatField(blank=True, default=1.0, help_text='Масштабирование значка', null=True, verbose_name='Масштабирование'),
        ),
        migrations.AlterField(
            model_name='cesiumlabel',
            name='backgroundColor',
            field=colorfield.fields.ColorField(blank=True, default='#FF000000', help_text='Цвет фона метки', image_field=None, max_length=18, null=True, samples=[('#FF0000', 'Красный'), ('#00FF00', 'Зеленый'), ('#0000FF', 'Синий'), ('#FFFF00', 'Желтый')], verbose_name='Цвет фона'),
        ),
        migrations.AlterField(
            model_name='cesiumlabel',
            name='fillColor',
            field=colorfield.fields.ColorField(blank=True, default='#FF000000', help_text='Цвет заливки метки', image_field=None, max_length=18, null=True, samples=[('#FF0000', 'Красный'), ('#00FF00', 'Зеленый'), ('#0000FF', 'Синий'), ('#FFFF00', 'Желтый')], verbose_name='Цвет заливки'),
        ),
        migrations.AlterField(
            model_name='cesiumlabel',
            name='outlineColor',
            field=colorfield.fields.ColorField(blank=True, default='#FF000000', help_text='Цвет обводки метки', image_field=None, max_length=18, null=True, samples=[('#FF0000', 'Красный'), ('#00FF00', 'Зеленый'), ('#0000FF', 'Синий'), ('#FFFF00', 'Желтый')], verbose_name='Цвет обводки'),
        ),
        migrations.AlterField(
            model_name='cesiumlabel',
            name='outlineWidth',
            field=models.FloatField(blank=True, default=1.0, help_text='Ширина обводки метки (в пикселях)', null=True, verbose_name='Ширина обводки'),
        ),
        migrations.AlterField(
            model_name='cesiumlabel',
            name='scale',
            field=models.FloatField(blank=True, default=1.0, help_text='Масштабирование значка', null=True, verbose_name='Масштабирование'),
        ),
    ]
