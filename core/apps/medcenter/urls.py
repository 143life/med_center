from django.urls import path

from .views import (
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
]
