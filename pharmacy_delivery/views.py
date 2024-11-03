from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)