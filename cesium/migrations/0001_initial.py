# Generated by Django 4.2.4 on 2023-08-10 06:33

from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CesiumProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название провайдера', max_length=50, verbose_name='Название')),
                ('create_new', models.BooleanField(default=True, help_text='Создать новый объект', verbose_name='Создать новый объект Cesium')),
                ('params', models.JSONField(blank=True, default='{}', help_text='Параметры функции провайдера в формате JSON', null=True, verbose_name='Параметры функции в формате JSON')),
            ],
            options={
                'verbose_name': 'Провайдер тайлов/реьлефа',
                'verbose_name_plural': '        Провайдеры тайлов и рельефа',
            },
        ),
        migrations.CreateModel(
            name='CesiumProviderFunc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('func', models.CharField(default='SingleTileImageryProvider', help_text='Функция Cesium', max_length=50, verbose_name='Функция Cesium')),
                ('desc', models.CharField(help_text='Описание функции', max_length=100, verbose_name='Описание функции')),
            ],
            options={
                'verbose_name': 'Функция провайдера тайлов и рельефа',
                'verbose_name_plural': '         Функции провайдера тайлов и рельефа',
            },
        ),
        migrations.CreateModel(
            name='ProviderViewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_default', models.BooleanField(db_column='is_default', default=False, help_text='По умолчанию', verbose_name='По умолчанию')),
                ('is_enabled', models.BooleanField(default=True, help_text='Использовать/не использовать тайловый сервер', verbose_name='Доступен')),
                ('name', models.CharField(help_text='Название слоя', max_length=50, verbose_name='Название')),
                ('type', models.CharField(choices=[('ImageryProvider', 'Слой изображений'), ('TerrainProvider', 'Слой рельефа')], default='ImageryProvider', help_text='Тип тайлового слоя', max_length=50, verbose_name='Тип')),
                ('tooltip', models.CharField(help_text='Устанавливает текст для всплывающего окна при поднесении курсора к элементу', max_length=200, verbose_name='Подсказка')),
                ('iconUrl', models.CharField(blank=True, help_text='URL/путь до иконки тайлового сервера в блоке "Источники данных"', max_length=200, null=True, verbose_name='URL/путь')),
                ('category', models.CharField(blank=True, help_text='Категория тайлового слоя', max_length=50, null=True, verbose_name='Категория')),
                ('provider', models.ForeignKey(blank=True, help_text='Провайдер тайлов и рельефа', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cesiumProvider', related_query_name='cesiumProvider', to='cesium.cesiumprovider', verbose_name='Провайдер тайлов и рельефа')),
            ],
            options={
                'verbose_name': 'Тайловый слой',
                'verbose_name_plural': '       Слои изображений и рельефа',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='CesiumViewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_default', models.BooleanField(default=False, help_text='Использовать/не использовать этот Viewer по умолчанию', verbose_name='По умолчанию')),
                ('name', models.CharField(default='Cesium Viewer', help_text='Название Cesuim Viewer', max_length=50, verbose_name='Название')),
                ('animation', models.BooleanField(default=True, help_text='Включает панель анимации события во времени (Круглые часы)', verbose_name='Анимация')),
                ('timeline', models.BooleanField(default=True, help_text='Включает ленту времени', verbose_name='Лента времени')),
                ('baseLayerPicker', models.BooleanField(default=True, help_text='Включает кнопку выбора слоев карты', verbose_name='Выбор базового слоя')),
                ('fullscreenButton', models.BooleanField(default=True, help_text='Включает кнопку полноэкранного режима', verbose_name='Полноэкранный режим')),
                ('geocoder', models.BooleanField(default=True, help_text='Включает функцию геокодирования (кнопка лупы)', verbose_name='Геокодер')),
                ('homeButton', models.BooleanField(default=True, help_text='Включает кнопку домой', verbose_name='Домой')),
                ('infoBox', models.BooleanField(default=True, help_text='Включает информационное окно при нажатии на объект', verbose_name='Информационное окно')),
                ('sceneModePicker', models.BooleanField(default=True, help_text='Включает кнопку выбора режима отображения сцены', verbose_name='Режим сцены')),
                ('selectionIndicator', models.BooleanField(default=True, help_text='Включает индикатор фокуса при нажатии на объект', verbose_name='Индикатор выбора')),
                ('navigationHelpButton', models.BooleanField(default=True, help_text='Включает кнопку помощи по управлению картой', verbose_name='Помощь')),
                ('navigationInstructionsInitiallyVisible', models.BooleanField(default=True, help_text='Показывает инструкции по навигации при загрузке страницы', verbose_name='Инструкции')),
                ('skyBox', models.BooleanField(default=True, help_text='Включает симуляцию неба', verbose_name='Небо')),
                ('skyAtmosphere', models.BooleanField(default=True, help_text='Включает симуляцию атмосферы', verbose_name='Атмосфера')),
                ('fullscreenElement', models.CharField(default='document.body', help_text='Элемент HTML, в который будет помещаться карта при включении полноэкранного режима. Пример: document.body', max_length=50, verbose_name='Элемент полноэкранного режима')),
                ('targetFrameRate', models.IntegerField(default=60, help_text='Устанавливает целевую частоту кадров при рендеринге карты', verbose_name='Частота кадров')),
                ('showRenderLoopErrors', models.BooleanField(default=True, help_text='При значении True показывает окно с сообщением об ошибках ренденринга', verbose_name='Ошибки рендеринга')),
                ('useBrowserRecommendedResolution', models.BooleanField(default=True, help_text='Включает рекомендованное разрешение карты', verbose_name='Рекомендованное разрешение')),
                ('sceneMode', models.IntegerField(choices=[(1, '2.5D'), (2, '2D'), (3, '3D')], default=3, help_text='Устанавливает режим сцены. 2.5D - перспективный режим, 2D - карта просматривается сверху вниз в ортогональной проекции, 3D - Традиционный вид Земного шара', verbose_name='Режим сцены')),
                ('mapProjection', models.CharField(choices=[('WebMercatorProjection', 'WebMercatorProjection'), ('GeographicProjection', 'GeographicProjection')], default='GeographicProjection', help_text='Устанавливает проекцию карты', max_length=50, verbose_name='Проекция карты')),
                ('projectionPicker', models.BooleanField(default=False, help_text='Включает кнопку выбора отображения карты - перспективное или ортогональное', verbose_name='Выбор отображения')),
                ('globe', models.BooleanField(default=True, help_text='Включает отображение поверхности Земли (Глобус в 3D, карта в 2D)', verbose_name='Глобус')),
                ('showCredit', models.CharField(choices=[('block', 'Показать'), ('none', 'Скрыть')], default='none', help_text='Показывает авторство в нижней части окна карты', max_length=50, verbose_name='Авторство')),
                ('imageryProviderViewModels', sortedm2m.fields.SortedManyToManyField(blank=True, help_text='Позволяет установить провайдеры изображений', limit_choices_to={'type': 'ImageryProvider'}, related_name='imageryProviderViewModels', related_query_name='imageryProviderViewModels', to='cesium.providerviewmodel', verbose_name='Провайдеры изображений')),
                ('terrainProviderViewModels', sortedm2m.fields.SortedManyToManyField(blank=True, help_text='Позволяет установить провайдеры рельефа', limit_choices_to={'type': 'TerrainProvider'}, related_name='terrainProviderViewModels', related_query_name='terrainProviderViewModels', to='cesium.providerviewmodel', verbose_name='Провайдеры рельефа')),
            ],
            options={
                'verbose_name': 'Карта (Cesium Viewer)',
                'verbose_name_plural': '      Карты (Cesium Viewers)',
            },
        ),
        migrations.AddField(
            model_name='cesiumprovider',
            name='func',
            field=models.ForeignKey(blank=True, help_text='Функция Cesium', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tileTerrainProvider', to='cesium.cesiumproviderfunc', verbose_name='Функция Cesium'),
        ),
    ]
