# Generated by Django 4.2.4 on 2023-08-20 07:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo_repository', '0006_alter_protectedobjectgeometry_geom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ozgeometry',
            name='parent_object',
            field=models.ForeignKey(blank=True, help_text='Охранная зона объекта', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='oz_geometry', related_query_name='oz_geometry', to='geo_repository.oz', verbose_name='Охранная зона'),
        ),
        migrations.AlterField(
            model_name='protectedobjectgeometry',
            name='parent_object',
            field=models.ForeignKey(blank=True, help_text='Охраняемый объект', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='protected_object_geometry', related_query_name='protected_object_geometry', to='geo_repository.protectedobject', verbose_name='Охраняемый объект'),
        ),
        migrations.AlterField(
            model_name='zmrgeometry',
            name='parent_object',
            field=models.ForeignKey(blank=True, help_text='Зона минимальных расстояний объекта', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zmr_geometry', related_query_name='zmr_geometry', to='geo_repository.zmr', verbose_name='Зона'),
        ),
    ]
