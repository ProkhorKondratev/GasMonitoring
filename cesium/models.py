from django.db import models
from sortedm2m.fields import SortedManyToManyField
from colorfield.fields import ColorField

# стандартные цвета для выбора
COLOR_PALETTES = [
    ('#FF0000', 'Красный'),
    ('#00FF00', 'Зеленый'),
    ('#0000FF', 'Синий'),
    ('#FFFF00', 'Желтый'),
]


def default_cartesian2():
    return {"x": 0.0, "y": 0.0}


def default_cartesian3():
    return {"x": 0.0, "y": 0.0, "z": 0.0}


def default_near_far_scalar():
    return {"near": 0.0, "nearValue": 0.0, "far": 1.0, "farValue": 0.0}


def default_near_far():
    return {"near": 0.0, "far": 10000000.0}


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


class CesiumAbstractGeometries(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
        help_text='Название объекта',
        null=True,
        blank=True,
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='По умолчанию',
        help_text='Устанавливает объект по умолчанию',
    )
    show = models.BooleanField(
        default=True,
        verbose_name='Отображение',
        help_text='Включает отображение объекта',
    )
    heightReference = models.IntegerField(
        default=0,
        verbose_name='Выравнивание по высоте',
        help_text='Выравнивание значка по высоте',
        choices=(
            (0, 'Без изменений'),
            (1, 'Прижать к поверхности Земли'),
            (2, 'Использовать высоту относительно точки на поверхности Земли'),
        )
    )
    scaleByDistance = models.JSONField(
        default=default_near_far_scalar,
        verbose_name='Масштабирование по расстоянию',
        help_text='Определяет масштабирование объекта в зависимости от расстояния до камеры',
    )
    translucencyByDistance = models.JSONField(
        default=default_near_far_scalar,
        verbose_name='Прозрачность по расстоянию',
        help_text='Определяет прозрачность объекта в зависимости от расстояния до камеры',
    )
    distanceDisplayCondition = models.JSONField(
        default=default_near_far,
        verbose_name='Отображение по расстоянию',
        help_text='Устанавливает диапазон, в котором объект будет отображаться',
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.is_default:
            self.__class__.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class CesiumAbstractObjects(CesiumAbstractGeometries):
    scale = models.FloatField(
        default=1.0,
        verbose_name='Масштабирование',
        help_text='Масштабирование значка',
        null=True,
        blank=True,
    )
    pixelOffset = models.JSONField(
        default=default_cartesian2,
        verbose_name='Смещение',
        help_text='Смещение объекта относительно координат в пикселях',
    )
    eyeOffset = models.JSONField(
        default=default_cartesian3,
        verbose_name='Смещение относительно камеры',
        help_text='Смещение объекта относительно камеры',
    )
    horizontalOrigin = models.IntegerField(
        default=0,
        verbose_name='Горизонтальное выравнивание',
        help_text='Горизонтальное выравнивание объекта',
        choices=(
            (0, 'По центру'),
            (1, 'Слева'),
            (2, 'Справа'),
        )
    )
    verticalOrigin = models.IntegerField(
        default=0,
        verbose_name='Вертикальное выравнивание',
        help_text='Вертикальное выравнивание объекта',
        choices=(
            (0, 'По центру'),
            (1, 'Снизу'),
            (3, 'Сверху'),
        )
    )
    pixelOffsetScaleByDistance = models.JSONField(
        default=default_near_far_scalar,
        verbose_name='Смещение по расстоянию',
        help_text='Определяет смещение объекта в зависимости от расстояния до камеры',
    )

    class Meta:
        abstract = True


class CesiumBillboard(CesiumAbstractObjects):
    image = models.FileField(
        verbose_name='Иконка типа',
        upload_to='bilboard_images',
        help_text='Иконка для визуализации типа объекта',
        default=None,
        null=True,
        blank=True,
    )
    color = ColorField(
        format='hexa',
        default='#FF000000',
        verbose_name='Цвет',
        help_text='Цвет значка',
        samples=COLOR_PALETTES
    )
    rotation = models.FloatField(
        default=0.0,
        verbose_name='Поворот',
        help_text='Поворот значка',
    )
    alignedAxis = models.JSONField(
        default=default_cartesian3,
        verbose_name='Ось выравнивания',
        help_text='Ось выравнивания значка',
    )
    width = models.IntegerField(
        default=64,
        verbose_name='Ширина',
        help_text='Ширина значка (в пикселях)',
    )
    height = models.IntegerField(
        default=64,
        verbose_name='Высота',
        help_text='Высота значка (в пикселях)',
    )

    class Meta:
        verbose_name = 'Стиль значка'
        verbose_name_plural = 'Стили значков'

    def __str__(self):
        return self.name if self.name else 'Стиль значка'


class CesiumLabel(CesiumAbstractObjects):
    text = models.CharField(
        default=None,
        max_length=255,
        verbose_name='Текст',
        help_text='Текст метки',
        null=True,
        blank=True,
    )
    font = models.CharField(
        default='30px sans-serif',
        max_length=255,
        verbose_name='Шрифт',
        help_text='Шрифт метки. Пример: 30px sans-serif',
    )
    style = models.IntegerField(
        default=2,
        verbose_name='Стиль',
        help_text='Стиль метки',
        choices=(
            (0, 'Заливка без обводки'),
            (1, 'Обводка без заливки'),
            (2, 'Заливка и обводка'),
        )
    )
    showBackground = models.BooleanField(
        default=False,
        verbose_name='Отображение фона',
        help_text='Включает отображение фона метки',
    )
    backgroundColor = ColorField(
        format='hexa',
        default='#FF000000',
        verbose_name='Цвет фона',
        help_text='Цвет фона метки',
        samples=COLOR_PALETTES,
        null=True,
        blank=True,
    )
    backgroundPadding = models.JSONField(
        default=default_cartesian2,
        verbose_name='Отступ фона',
        help_text='Отступ фона метки от текста',
    )
    fillColor = ColorField(
        format='hexa',
        default='#FF000000',
        verbose_name='Цвет заливки',
        help_text='Цвет заливки метки',
        samples=COLOR_PALETTES,
        null=True,
        blank=True,
    )
    outlineColor = ColorField(
        format='hexa',
        default='#FF000000',
        verbose_name='Цвет обводки',
        help_text='Цвет обводки метки',
        samples=COLOR_PALETTES,
        null=True,
        blank=True,
    )
    outlineWidth = models.FloatField(
        default=1.0,
        verbose_name='Ширина обводки',
        help_text='Ширина обводки метки (в пикселях)',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Стиль надписи'
        verbose_name_plural = 'Стили надписей'

    def __str__(self):
        return self.name if self.name else 'Стиль надписи'


class CesiumPoint(CesiumAbstractGeometries):
    pixelSize = models.FloatField(
        default=1.0,
        verbose_name='Размер',
        help_text='Размер точки (в пикселях)',
    )
    color = ColorField(
        format='hexa',
        default='#FF000000',
        verbose_name='Цвет',
        help_text='Цвет точки',
        samples=COLOR_PALETTES
    )
    outlineColor = ColorField(
        format='hexa',
        default='#FF000000',
        verbose_name='Цвет обводки',
        help_text='Цвет обводки точки',
        samples=COLOR_PALETTES
    )
    outlineWidth = models.FloatField(
        default=1.0,
        verbose_name='Ширина обводки',
        help_text='Ширина обводки точки',
    )

    class Meta:
        verbose_name = 'Стиль точки'
        verbose_name_plural = 'Стили точек'

    def __str__(self):
        return self.name if self.name else 'Стиль точки'


class CesiumPolylineMaterial(models.Model):
    name = models.CharField(
        max_length=50,
        default='Color',
        verbose_name='Название материала',
        help_text='Название материала',
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='По умолчанию',
        help_text='Использовать по умолчанию',
    )
    type = models.CharField(
        max_length=20,
        default='Color',
        verbose_name='Тип материала',
        help_text='Тип материала',
        choices=(
            ('Color', 'Цвет'),
            # ('PolylineArrow', 'Стрелка'),
            ('PolylineDash', 'Пунктир'),
            # ('PolylineGlow', 'Свечение'),
            # ('PolylineOutline', 'Контур'),
        ))
    color = ColorField(
        format="hexa",
        default='#FF000000',
        verbose_name='Цвет заливки',
        help_text='Позволяет установить цвет заливки линии',
        samples=COLOR_PALETTES,
    )
    gapColor = ColorField(
        format="hexa",
        default='#FF000000',
        verbose_name='Цвет промежутков линии',
        help_text='Позволяет установить цвет промежутков линии',
        samples=COLOR_PALETTES,
    )
    dashLength = models.IntegerField(
        default=16,
        verbose_name='Длина пунктира в пикселях',
        help_text='Позволяет установить длину пунктира в пикселях',
    )

    class Meta:
        verbose_name = 'Стиль текстуры линии'
        verbose_name_plural = 'Стили текстур линий'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            self.__class__.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class CesiumPolyline(CesiumAbstractGeometries):
    width = models.FloatField(
        default=1.0,
        verbose_name='Ширина',
        help_text='Ширина линии (в пикселях)',
    )
    material = models.ForeignKey(
        CesiumPolylineMaterial,
        on_delete=models.CASCADE,
        related_name='PolylineMaterial',
        related_query_name='PolylineMaterial',
        verbose_name='Материал',
        help_text='Стандартный материал линии',
        null=True,
        blank=True,
    )
    depthFailMaterial = models.ForeignKey(
        CesiumPolylineMaterial,
        on_delete=models.CASCADE,
        related_name='PolylineDepthFailMaterial',
        related_query_name='PolylineDepthFailMaterial',
        verbose_name='Материал под рельефом',
        help_text='Материал, использующийся для линии, когда она проходит под рельефом',
        null=True,
        blank=True,
    )
    clampToGround = models.BooleanField(
        default=False,
        verbose_name='Прижать к поверхности Земли',
        help_text='Прижать линию к поверхности Земли',
    )
    shadows = models.IntegerField(
        default=0,
        verbose_name='Тень',
        help_text='Тень линии',
        choices=(
            (0, 'Нет тени'),
            (1, 'Принимать и отбрасывать тень'),
            (2, 'Отбрасывать тень'),
            (3, 'Принимать тень'),
        )
    )
    zIndex = models.IntegerField(
        default=0,
        verbose_name='Z-индекс',
        help_text='Определяет индекс, используемый для упорядочивания линий при отображении. '
                  'Изображается только тогда, когда параметр ClampToGround установлен в true',
    )

    class Meta:
        verbose_name = 'Стиль линии'
        verbose_name_plural = 'Стили линий'

    def __str__(self):
        return self.name if self.name else 'Стиль линии'


class CesiumPolygonMaterial(models.Model):
    name = models.CharField(
        max_length=50,
        default='Color',
        verbose_name='Название материала',
        help_text='Название материала',
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name='По умолчанию',
        help_text='Использовать по умолчанию',
    )
    type = models.CharField(
        max_length=20,
        default='Color',
        verbose_name='Тип материала',
        help_text='Тип материала',
        choices=(
            ('Color', 'Цвет'),
            # ('Image', 'Изображение'),
            # ('Grid', 'Сетка'),
            # ('Stripe', 'Полосы'),
            # ('Checkerboard', 'Шахматы'),
            # ('Dot', 'Точки'),
            # ('Water', 'Вода'),
        ))
    color = ColorField(
        format="hexa",
        default='#FF0000',
        verbose_name='Цвет заливки',
        help_text='Позволяет установить цвет заливки полигона',
        samples=COLOR_PALETTES,
    )

    class Meta:
        verbose_name = 'Стиль текстуры полигона'
        verbose_name_plural = 'Стили текстур полигонов'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_default:
            self.__class__.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class CesiumPolygon(CesiumAbstractGeometries):
    height = models.FloatField(
        default=0.0,
        verbose_name='Высота',
        help_text='Высота полигона (в метрах) относительно поверхности Земли',
        null=True,
        blank=True,
    )
    extrudedHeight = models.FloatField(
        default=0.0,
        verbose_name='Высота полигона',
        help_text='Высота полигона в 3-х мерном пространстве (в метрах)',
        null=True,
        blank=True,
    )
    extrudedHeightReference = models.IntegerField(
        default=0,
        verbose_name='Поверхность высоты полигона',
        help_text='Определяет поверхность, относительно которой считается высота полигона в 3-х мерном пространстве',
        choices=(
            (0, 'Без изменений'),
            (1, 'Прижать к поверхности Земли'),
            (2, 'Использовать высоту относительно точки на поверхности Земли'),
        )
    )
    stRotation = models.FloatField(
        default=0.0,
        verbose_name='Поворот',
        help_text='Определяет поворот текстуры полигона против часовой стрелки с севера',
        null=True,
        blank=True,
    )
    fill = models.BooleanField(
        default=True,
        verbose_name='Заливка',
        help_text='Определяет, будет ли отображаться заливка полигона',
    )
    material = models.ForeignKey(
        CesiumPolygonMaterial,
        on_delete=models.CASCADE,
        related_name='PolygonMaterial',
        related_query_name='PolygonMaterial',
        verbose_name='Материал',
        help_text='Определяет материал, используемый для отображения заливки полигона',
        null=True,
        blank=True,
    )
    outline = models.BooleanField(
        default=False,
        verbose_name='Контур',
        help_text='Определяет, будет ли отображаться контур полигона',
    )
    outlineColor = ColorField(
        format="hexa",
        default='#FF000000',
        verbose_name='Цвет контура',
        help_text='Позволяет установить цвет контура полигона',
        samples=COLOR_PALETTES,
    )
    outlineWidth = models.FloatField(
        default=1.0,
        verbose_name='Ширина контура',
        help_text='Ширина контура полигона (в пикселях) - временно не работает по ошибке в CesiumJS',
    )
    closeTop = models.BooleanField(
        default=True,
        verbose_name='Закрыть верх',
        help_text='Если false, то оставляет открытой верхнюю часть полигона',
    )
    closeBottom = models.BooleanField(
        default=True,
        verbose_name='Закрыть низ',
        help_text='Если false, то оставляет открытой нижнюю часть полигона',
    )
    shadows = models.IntegerField(
        default=0,
        verbose_name='Тень',
        help_text='Тень полигона',
        choices=(
            (0, 'Нет тени'),
            (1, 'Принимать и отбрасывать тень'),
            (2, 'Отбрасывать тень'),
            (3, 'Принимать тень'),
        )
    )
    zIndex = models.IntegerField(
        default=0,
        verbose_name='Z-индекс',
        help_text='Определяет индекс, используемый для упорядочивания полигонов при отображении. '
                  'Применяется только тогда, когда параметры Height и ExtrudedHeight установлены не установлены',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Стиль полигона'
        verbose_name_plural = 'Стили полигонов'

    def __str__(self):
        return self.name if self.name else 'Стиль полигона'
