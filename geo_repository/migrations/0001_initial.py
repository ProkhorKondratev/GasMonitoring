# Generated by Django 4.2.4 on 2023-08-10 09:55

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ZMR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название зоны', max_length=254, verbose_name='Название')),
                ('description', models.TextField(blank=True, help_text='Описание зоны', null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Зона',
                'verbose_name_plural': 'Зоны',
            },
        ),
        migrations.CreateModel(
            name='ZMRGeometry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_relevant', models.BooleanField(default=True, help_text='Актуальность геометрии зоны', verbose_name='Актуальна')),
                ('date_start', models.DateTimeField(auto_now_add=True, help_text='Дата начала действия геометрии', null=True, verbose_name='Дата начала')),
                ('date_end', models.DateTimeField(blank=True, help_text='Дата окончания действия геометрии', null=True, verbose_name='Дата окончания')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, help_text='Геометрия зоны', null=True, srid=4326, verbose_name='Геометрия')),
                ('zone', models.ForeignKey(blank=True, help_text='Зона', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zone_geometry', related_query_name='zone_geometry', to='geo_repository.zmr', verbose_name='Зона')),
            ],
            options={
                'verbose_name': 'Геометрия зоны',
                'verbose_name_plural': 'Геометрии зон',
            },
        ),
    ]