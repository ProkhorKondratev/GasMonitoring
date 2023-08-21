# Generated by Django 4.2.4 on 2023-08-19 18:02

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo_repository', '0005_protectedobject_protectedobjectgeometry_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protectedobjectgeometry',
            name='geom',
            field=django.contrib.gis.db.models.fields.GeometryCollectionField(blank=True, help_text='Геометрия охраняемого объекта', null=True, srid=4326, verbose_name='Геометрия'),
        ),
    ]
