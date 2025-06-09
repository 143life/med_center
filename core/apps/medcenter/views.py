from django.contrib.auth.decorators import user_passes_test
from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.shortcuts import (
    get_object_or_404,
    render,
)
from django.views.generic import TemplateView

from redis import Redis
from redis.exceptions import RedisError

from .models import Ticket


def home_view(request):
    return render(request, "medcenter/home.html")


class QueueDisplayView(TemplateView):
    template_name = "medcenter/queue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Используем тот же протокол, что и в запросе (http->ws, https->wss)
        protocol = "ws"
        if self.request.is_secure():
            protocol = "wss"
        context["ws_url"] = f"{protocol}://{self.request.get_host()}/ws/queue/"
        return context


def health_check(request):
    """
    Проверка здоровья основных компонентов системы:
    - База данных
    - Redis
    - Диск
    """
    health_status = {
        "status": "healthy",
        "components": {"database": True, "redis": True, "disk": True},
    }

    # Проверка базы данных
    try:
        connections["default"].cursor()
    except OperationalError:
        health_status["components"]["database"] = False
        health_status["status"] = "unhealthy"

    # Проверка Redis
    try:
        redis_client = Redis(host="redis", port=6379, socket_connect_timeout=2)
        redis_client.ping()
    except RedisError:
        health_status["components"]["redis"] = False
        health_status["status"] = "unhealthy"

    # Проверка доступности диска для записи
    try:
        with open("/app/logs/health_check.tmp", "w") as f:
            f.write("health check")
    except OSError:
        health_status["components"]["disk"] = False
        health_status["status"] = "unhealthy"

    status_code = 200 if health_status["status"] == "healthy" else 503
    return JsonResponse(health_status, status=status_code)


def is_staff(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff)
def ticket_progress_view(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    appointments = ticket.appointment_set.filter(completed=True).order_by(
        "updated_at",
    )

    progress_data = []
    total_duration_seconds = 0
    previous_time = ticket.datetime

    for appointment in appointments:
        duration_seconds = (
            appointment.updated_at - previous_time
        ).total_seconds()

        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)

        duration_formatted_parts = []
        if hours > 0:
            duration_formatted_parts.append(f"{hours} ч")
        if minutes > 0 or (hours == 0 and minutes == 0):
            duration_formatted_parts.append(f"{minutes} мин")

        progress_data.append(
            {
                "specialization": appointment.specialization.title,
                "end_time": appointment.updated_at,
                "duration_formatted": " ".join(duration_formatted_parts),
            },
        )
        previous_time = appointment.updated_at

    if appointments:
        total_duration_seconds = (
            appointments.last().updated_at - ticket.datetime
        ).total_seconds()

    total_hours = int(total_duration_seconds // 3600)
    total_minutes = int((total_duration_seconds % 3600) // 60)
    total_duration_formatted_parts = []
    if total_hours > 0:
        total_duration_formatted_parts.append(f"{total_hours} ч")
    if total_minutes > 0 or (total_hours == 0 and total_minutes == 0):
        total_duration_formatted_parts.append(f"{total_minutes} мин")

    context = {
        "ticket": ticket,
        "progress_data": progress_data,
        "total_duration_formatted": " ".join(total_duration_formatted_parts),
        "title": f"Процесс по талону №{ticket.number}",
    }

    return render(
        request,
        "medcenter/ticket_progress.html",
        context,
    )
