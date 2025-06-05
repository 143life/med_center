from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = "guest", "Гость"
        USER = "user", "Пользователь"
        ADMIN = "admin", "Администратор"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
    )

    email = models.EmailField(
        "email address",
        unique=True,  # Email должен быть уникальным
        blank=False,  # Обязательное поле
        null=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    phone = models.CharField(
        "телефон",
        max_length=20,
        blank=True,  # Можно сделать обязательным (blank=False)
        null=True,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Номер телефона должен быть в формате: '+999999999'.",
            ),
        ],
    )

    # Автоматически даем доступ в админку для администраторов
    def save(self, *args, **kwargs):
        # Для суперпользователей всегда устанавливаем роль ADMIN
        if self.is_superuser:
            self.role = self.Role.ADMIN
            self.is_staff = True

        # Для обычных админов
        elif self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = False

        # Для админов, созданных в админке
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    def __str__(self):
        role_display = self.get_role_display()
        status = "Активен" if self.is_active else "Неактивен"
        return f"{self.get_full_name() or self.username} ({self.email}) - {role_display} [{status}]"  # noqa

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = [
            "-date_joined",
        ]  # Сортировка по дате регистрации (новые сверху)
        app_label = "account"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
