from django.contrib.auth import (
    login,
    logout,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.views.generic import CreateView

from .forms import (
    LoginForm,
    SignUpForm,
)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "account/logout.html")  # Используем наш шаблон


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "account/signup.html"
    success_url = "/profile/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "account/profile.html")
