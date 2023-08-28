from django.views.decorators.cache import cache_control
from django.shortcuts import redirect
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from geo_repository.tiles import open_tiles
MONTH_SECONDS = 60 * 60 * 24 * 30


@cache_control(max_age=MONTH_SECONDS)
def tiles(request, tiles_type, database_id, z, x, y):
    with (open_tiles(tiles_type, database_id)) as geo_tiles:
        data = geo_tiles.tile(z, x, y)
        if data:
            response = HttpResponse(
                content=data,
                status=200,
            )
            if tiles_type == 'mbtls':
                response["Content-Type"] = "image/png"
            elif tiles_type == 'gpkg':
                response["Content-Type"] = "image/jpg"
            elif tiles_type == 'relt':
                response["Content-Type"] = "image/png"
            else:
                raise ImproperlyConfigured("Set the correct database type.")
            return response
        else:
            return redirect('/static/empty_tile.png')
