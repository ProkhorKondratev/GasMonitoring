# Generated by Django 4.2.4 on 2023-08-10 08:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cesium', '0003_alter_cesiumviewer_terrainproviderviewmodels_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TileProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название тайлового сервера', max_length=50, verbose_name='Название')),
                ('type', models.CharField(choices=[('UrlTemplateImageryProvider', 'Тайловый сервер по URL (XYZ)'), ('SingleTileImageryProvider', 'Одиночное изображение'), ('TerrainProvider', 'Рельеф')], default='UrlTemplateImageryProvider', help_text='Тип тайлового сервера', max_length=50, verbose_name='Тип')),
                ('url', models.URLField(help_text='URL тайлового сервера. Пример: https://maps.google.com/maps/vt?lyrs=s,h&x={x}&y={y}&z={z}', unique=True, verbose_name='URL')),
                ('credit', models.CharField(blank=True, help_text='Подпись источника данных тайлового сервера', max_length=200, null=True, verbose_name='Авторство')),
                ('minimumLevel', models.IntegerField(default=0, help_text='Минимальный уровень тайлового сервера', verbose_name='Минимальный уровень')),
                ('maximumLevel', models.IntegerField(blank=True, default=None, help_text='Максимальный уровень тайлового сервера', null=True, verbose_name='Максимальный уровень')),
                ('tileWidth', models.IntegerField(default=256, help_text='Ширина тайла в пикселях', verbose_name='Ширина тайла')),
                ('tileHeight', models.IntegerField(default=256, help_text='Высота тайла в пикселях', verbose_name='Высота тайла')),
            ],
            options={
                'verbose_name': 'Тайловый сервер',
                'verbose_name_plural': 'Тайловые сервера',
            },
        ),
        migrations.AlterModelOptions(
            name='providerviewmodel',
            options={'verbose_name': 'Тайловый слой', 'verbose_name_plural': 'Тайловые слои'},
        ),
        migrations.RemoveField(
            model_name='providerviewmodel',
            name='is_default',
        ),
        migrations.RemoveField(
            model_name='providerviewmodel',
            name='provider',
        ),
        migrations.AlterField(
            model_name='providerviewmodel',
            name='iconUrl',
            field=models.CharField(blank=True, help_text='URL/путь до иконки тайлового сервера в блоке "Источники данных"', max_length=200, null=True, verbose_name='URL/путь'),
        ),
        migrations.AlterField(
            model_name='providerviewmodel',
            name='type',
            field=models.CharField(choices=[('ImageryProvider', 'Тайловый слой'), ('TerrainProvider', 'Слой рельефа')], default='ImageryProvider', help_text='Тип тайлового слоя', max_length=50, verbose_name='Тип'),
        ),
        migrations.DeleteModel(
            name='CesiumProvider',
        ),
        migrations.DeleteModel(
            name='CesiumProviderFunc',
        ),
        migrations.AddField(
            model_name='providerviewmodel',
            name='tileProvider',
            field=models.ForeignKey(blank=True, help_text='Тайловый сервер', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tileProvider', related_query_name='tileProvider', to='cesium.tileprovider', verbose_name='Тайловый сервер'),
        ),
    ]
