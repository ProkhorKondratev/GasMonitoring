from django.views.generic import TemplateView


class MapView(TemplateView):
    template_name = "cesium_map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Карта Cesium"
        print(context)

        return context
