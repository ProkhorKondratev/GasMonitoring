from django.contrib.gis import admin
from .models import ZMR, ZMRGeometry, OZ, OZGeometry
from geo_repository.mixins import LifeCycleUpdateMixin


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
        ('Зона', {
            'fields': ('is_show', 'name', 'description'),
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


class ZoneGeometryBaseAdmin(LifeCycleUpdateMixin, admin.ModelAdmin):
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


class ZMRGeometryInline(ZoneBaseInline):
    model = ZMRGeometry


class OZGeometryInline(ZoneBaseInline):
    model = OZGeometry


@admin.register(ZMR)
class ZMRAdmin(ZoneBaseAdmin):
    inlines = [ZMRGeometryInline]


@admin.register(OZ)
class OZAdmin(ZoneBaseAdmin):
    inlines = [OZGeometryInline]


@admin.register(ZMRGeometry)
class ZMRGeometryAdmin(ZoneGeometryBaseAdmin):
    pass


@admin.register(OZGeometry)
class OZGeometryAdmin(ZoneGeometryBaseAdmin):
    pass
