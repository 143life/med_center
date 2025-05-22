from django.shortcuts import render
from django.views.generic import TemplateView


def home_view(request):
    return render(request, "medcenter/home.html")


class QueueDisplayView(TemplateView):
    template_name = "medcenter/queue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ws_url"] = f"ws://{self.request.get_host()}/ws/queue/"
        return context
