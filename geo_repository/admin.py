from django.contrib.gis import admin
from .models import ZMR, ZMRGeometry
from geo_repository.mixins import LifeCycleUpdateMixin


class ZMRGeometryInline(admin.TabularInline):
    model = ZMRGeometry
    can_delete = False

    readonly_fields = ('date_start', 'date_end', 'is_relevant', 'geom')
    fields = ('is_relevant', 'date_start', 'date_end', 'geom')
    ordering = ('-is_relevant', '-date_end')
    extra = 0


@admin.register(ZMR)
class ZMRAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('-id',)

    fieldsets = (
        ('Зона', {
            'fields': ('name', 'description'),
        }),
    )
    inlines = [ZMRGeometryInline]


@admin.register(ZMRGeometry)
class ZMRGeometryAdmin(LifeCycleUpdateMixin, admin.ModelAdmin):
    list_display = ('id', 'zone', 'is_relevant')
    readonly_fields = ('zone',)
    list_filter = ('is_relevant', 'date_start', 'date_end')
    fieldsets = (
        ('', {
            'fields': ('zone',),
        }),
        ('Геометрия', {
            'fields': ('geom',),
        }),
    )
