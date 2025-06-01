from django.db import connections
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from redis import Redis
from redis.exceptions import RedisError


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
