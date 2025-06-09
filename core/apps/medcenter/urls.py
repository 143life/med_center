from django.urls import path

from .views import (
    health_check,
    home_view,
    QueueDisplayView,
    ticket_progress_view,
)


app_name = "medcenter"

urlpatterns = [
    path("", home_view, name="home"),
    path(
        "queue/",
        QueueDisplayView.as_view(),
        name="queue",
    ),  # Основная страница
    path("health/", health_check, name="health_check"),
    path(
        "ticket-progress/<int:ticket_id>/",
        ticket_progress_view,
        name="ticket_progress",
    ),
]
