from django.contrib import messages
from django.contrib.auth import (
    login,
    logout,
)
from django.contrib.auth.views import LoginView
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import (
    LoginForm,
    SignUpForm,
)


class LoginView(LoginView):
    form_class = LoginForm
    template_name = "account/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Добро пожаловать, {self.request.user.email}!",
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка входа. Проверьте email и пароль.")
        return super().form_invalid(form)


def logout_view(request):
    logout(request)
    return render(request, "account/logout.html")  # Используем наш шаблон


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "account/signup.html"
    success_url = reverse_lazy(
        "account:profile",
    )  # Используем reverse_lazy вместо жесткого URL

    def form_valid(self, form):
        # Сохраняем пользователя
        user = form.save()  # Это создает и сохраняет пользователя

        # Логиним пользователя
        login(
            self.request,
            user,
            backend="core.apps.account.backends.EmailAuthBackend",
        )

        # Возвращаем стандартный response
        return super().form_valid(form)


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("account:login")
    return render(request, "account/profile.html")
