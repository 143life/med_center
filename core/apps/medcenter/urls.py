from django.urls import path

from .views import (
    health_check,
    home_view,
    QueueDisplayView,
)


urlpatterns = [
    path("", home_view, name="home"),
    path(
        "queue/",
        QueueDisplayView.as_view(),
        name="queue",
    ),  # Основная страница
    path("health/", health_check, name="health_check"),
]
