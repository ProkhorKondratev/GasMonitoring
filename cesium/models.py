from django.db import models
from sortedm2m.fields import SortedManyToManyField


class TileProvider(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Название тайлового сервера',
    )
    type = models.CharField(
        max_length=50,
        default='UrlTemplateImageryProvider',
        verbose_name='Тип',
        help_text='Тип тайлового сервера',
        choices=(
            ('UrlTemplateImageryProvider', 'Тайловый сервер по URL (XYZ)'),
            ('SingleTileImageryProvider', 'Одиночное изображение'),
            ('TerrainProvider', 'Рельеф'),
        ),
    )
    url = models.URLField(
        max_length=200,
        verbose_name='URL',
        help_text='URL тайлового сервера. Пример: https://maps.google.com/maps/vt?lyrs=s,h&x={x}&y={y}&z={z}',
        unique=True,
    )
    credit = models.CharField(
        max_length=200,
        verbose_name='Авторство',
        help_text='Подпись источника данных тайлового сервера',
        null=True,
        blank=True,
    )
    minimumLevel = models.IntegerField(
        default=0,
        verbose_name='Минимальный уровень',
        help_text='Минимальный уровень тайлового сервера',
    )
    maximumLevel = models.IntegerField(
        default=None,
        verbose_name='Максимальный уровень',
        help_text='Максимальный уровень тайлового сервера',
        null=True,
        blank=True,
    )
    tileWidth = models.IntegerField(
        default=256,
        verbose_name='Ширина тайла',
        help_text='Ширина тайла в пикселях',
    )
    tileHeight = models.IntegerField(
        default=256,
        verbose_name='Высота тайла',
        help_text='Высота тайла в пикселях',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тайловый сервер'
        verbose_name_plural = 'Тайловые сервера'


class ProviderViewModel(models.Model):
    is_enabled = models.BooleanField(
        default=True,
        verbose_name='Доступен',
        help_text='Использовать/не использовать тайловый сервер',
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Название',
        help_text='Название слоя',
    )
    type = models.CharField(
        max_length=50,
        default='ImageryProvider',
        verbose_name='Тип',
        help_text='Тип тайлового слоя',
        choices=(
            ('ImageryProvider', 'Тайловый слой'),
            ('TerrainProvider', 'Слой рельефа'),
        ),
    )
    tooltip = models.CharField(
        max_length=200,
        verbose_name='Подсказка',
        help_text='Устанавливает текст для всплывающего окна при поднесении курсора к элементу',
    )
    iconUrl = models.CharField(
        max_length=200,
        verbose_name='URL/путь',
        help_text='URL/путь до иконки тайлового сервера в блоке "Источники данных"',
        null=True,
        blank=True,
    )
    category = models.CharField(
        max_length=50,
        verbose_name='Категория',
        help_text='Категория тайлового слоя',
        null=True,
        blank=True,
    )
    tileProvider = models.ForeignKey(
        TileProvider,
        on_delete=models.SET_NULL,
        verbose_name='Тайловый сервер',
        help_text='Тайловый сервер',
        related_name='tileProvider',
        related_query_name='tileProvider',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тайловый слой'
        verbose_name_plural = 'Тайловые слои'


class CesiumViewer(models.Model):
    is_default = models.BooleanField(
        default=False,
        verbose_name='По умолчанию',
        help_text='Использовать/не использовать этот Viewer по умолчанию',
    )
    name = models.CharField(
        max_length=50,
        default='Cesium Viewer',
        verbose_name='Название',
        help_text='Название Cesuim Viewer',
    )
    animation = models.BooleanField(
        default=True,
        verbose_name='Анимация',
        help_text='Включает панель анимации события во времени (Круглые часы)',
    )
    timeline = models.BooleanField(
        default=True,
        verbose_name='Лента времени',
        help_text='Включает ленту времени',
    )
    baseLayerPicker = models.BooleanField(
        default=True,
        verbose_name='Выбор базового слоя',
        help_text='Включает кнопку выбора слоев карты',
    )
    fullscreenButton = models.BooleanField(
        default=True,
        verbose_name='Полноэкранный режим',
        help_text='Включает кнопку полноэкранного режима',
    )
    geocoder = models.BooleanField(
        default=True,
        verbose_name='Геокодер',
        help_text='Включает функцию геокодирования (кнопка лупы)',
    )
    homeButton = models.BooleanField(
        default=True,
        verbose_name='Домой',
        help_text='Включает кнопку домой',
    )
    infoBox = models.BooleanField(
        default=True,
        verbose_name='Информационное окно',
        help_text='Включает информационное окно при нажатии на объект',
    )
    sceneModePicker = models.BooleanField(
        default=True,
        verbose_name='Режим сцены',
        help_text='Включает кнопку выбора режима отображения сцены',
    )
    selectionIndicator = models.BooleanField(
        default=True,
        verbose_name='Индикатор выбора',
        help_text='Включает индикатор фокуса при нажатии на объект',
    )
    navigationHelpButton = models.BooleanField(
        default=True,
        verbose_name='Помощь',
        help_text='Включает кнопку помощи по управлению картой',
    )
    navigationInstructionsInitiallyVisible = models.BooleanField(
        default=True,
        verbose_name='Инструкции',
        help_text='Показывает инструкции по навигации при загрузке страницы',
    )
    imageryProviderViewModels = SortedManyToManyField(
        ProviderViewModel,
        verbose_name='Провайдеры изображений',
        help_text='Позволяет установить провайдеры изображений',
        related_name='imageryProviderViewModels',
        related_query_name='imageryProviderViewModels',
        limit_choices_to={'type': 'ImageryProvider'},
        blank=True,
        sorted=True,
    )
    terrainProviderViewModels = SortedManyToManyField(
        ProviderViewModel,
        verbose_name='Провайдеры рельефа',
        help_text='Позволяет установить провайдеры рельефа',
        related_name='ProviderViewModel',
        related_query_name='ProviderViewModel',
        limit_choices_to={'type': 'TerrainProvider'},
        blank=True,
        sorted=True,
    )
    skyBox = models.BooleanField(
        default=True,
        verbose_name='Небо',
        help_text='Включает симуляцию неба',
    )
    skyAtmosphere = models.BooleanField(
        default=True,
        verbose_name='Атмосфера',
        help_text='Включает симуляцию атмосферы',
    )
    fullscreenElement = models.CharField(
        max_length=50,
        default='document.body',
        verbose_name='Элемент полноэкранного режима',
        help_text='Элемент HTML, в который будет помещаться карта при включении полноэкранного режима. '
                  'Пример: document.body',
    )
    targetFrameRate = models.IntegerField(
        default=60,
        verbose_name='Частота кадров',
        help_text='Устанавливает целевую частоту кадров при рендеринге карты',
    )
    showRenderLoopErrors = models.BooleanField(
        default=True,
        verbose_name='Ошибки рендеринга',
        help_text='При значении True показывает окно с сообщением об ошибках ренденринга',
    )
    useBrowserRecommendedResolution = models.BooleanField(
        default=True,
        verbose_name='Рекомендованное разрешение',
        help_text='Включает рекомендованное разрешение карты',
    )
    sceneMode = models.IntegerField(
        default=3,
        verbose_name='Режим сцены',
        help_text='Устанавливает режим сцены. 2.5D - перспективный режим, 2D - карта просматривается сверху вниз '
                  'в ортогональной проекции, 3D - Традиционный вид Земного шара',
        choices=(
            (1, '2.5D'),
            (2, '2D'),
            (3, '3D'),
        )
    )
    mapProjection = models.CharField(
        max_length=50,
        default='GeographicProjection',
        verbose_name='Проекция карты',
        help_text='Устанавливает проекцию карты',
        choices=(
            ('WebMercatorProjection', 'WebMercatorProjection'),
            ('GeographicProjection', 'GeographicProjection'),
        )
    )
    projectionPicker = models.BooleanField(
        default=False,
        verbose_name='Выбор отображения',
        help_text='Включает кнопку выбора отображения карты - перспективное или ортогональное',
    )
    globe = models.BooleanField(
        default=True,
        verbose_name='Глобус',
        help_text='Включает отображение поверхности Земли (Глобус в 3D, карта в 2D)',
    )
    showCredit = models.CharField(
        max_length=50,
        default='none',
        verbose_name='Авторство',
        help_text='Показывает авторство в нижней части окна карты',
        choices=(
            ('block', 'Показать'),
            ('none', 'Скрыть')
        )
    )

    class Meta:
        verbose_name = 'Карта (Cesium Viewer)'
        verbose_name_plural = '      Карты (Cesium Viewers)'

    def __str__(self):
        return f'{self.name} (по умолчанию)' if self.is_default else self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            CesiumViewer.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
