from django.contrib.gis import admin
from .models import ZMR, ZMRGeometry, OZ, OZGeometry, ProtectedObject, ProtectedObjectGeometry
from geo_repository.mixins import LifeCycleUpdateMixin
from django.contrib.gis.forms import OSMWidget


class CustomGeoWidget(OSMWidget):
    map_srid = 4326
    display_raw = True
    supports_3d = False


class ZoneBaseInline(admin.TabularInline):
    can_delete = False

    readonly_fields = ('date_start', 'date_end', 'is_relevant', 'geom')
    fields = ('is_relevant', 'date_start', 'date_end', 'geom')
    ordering = ('-is_relevant', '-date_end')
    extra = 0


class ZoneBaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_show', 'name')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('-id',)

    list_editable = [
        'is_show'
    ]

    fieldsets = (
        ('Параметры', {
            'fields': ('is_show', 'name', 'description'),
        }),
        ('Охраняемый объект', {
            'fields': ('protected_object', ),
        }),
    )

    actions = ['show_all', 'hide_all']

    # снять галочки в поле показывать
    @admin.action(description='Показать все')
    def show_all(self, request, queryset):
        self.model.objects.all().update(is_show=True)

    # снять галочки в поле показывать
    @admin.action(description='Скрыть все')
    def hide_all(self, request, queryset):
        self.model.objects.all().update(is_show=False)


class ZoneGeometryBaseAdmin(LifeCycleUpdateMixin, admin.GISModelAdmin):
    gis_widget = CustomGeoWidget

    list_display = ('id', 'parent_object', 'is_relevant')
    list_display_links = ('id', 'parent_object',)
    readonly_fields = ('parent_object',)
    list_filter = ('is_relevant', 'date_start', 'date_end')
    fieldsets = (
        ('Охраняемый объект', {
            'fields': ('parent_object',),
        }),
        ('Геометрия', {
            'fields': ('geom',),
        }),
    )


class ZMRGeometryInline(ZoneBaseInline):
    model = ZMRGeometry


class OZGeometryInline(ZoneBaseInline):
    model = OZGeometry


class ProtectedObjectGeometryInline(ZoneBaseInline):
    model = ProtectedObjectGeometry


@admin.register(ZMR)
class ZMRAdmin(ZoneBaseAdmin):
    inlines = [ZMRGeometryInline]


@admin.register(OZ)
class OZAdmin(ZoneBaseAdmin):
    inlines = [OZGeometryInline]


@admin.register(ProtectedObject)
class ProtectedObjectAdmin(ZoneBaseAdmin):
    inlines = [ProtectedObjectGeometryInline]
    fieldsets = (
        ('Параметры', {
            'fields': ('is_show', 'name', 'description'),
        }),
    )


@admin.register(ZMRGeometry)
class ZMRGeometryAdmin(ZoneGeometryBaseAdmin):
    pass


@admin.register(OZGeometry)
class OZGeometryAdmin(ZoneGeometryBaseAdmin):
    pass


@admin.register(ProtectedObjectGeometry)
class ProtectedObjectGeometryAdmin(ZoneGeometryBaseAdmin):
    pass
