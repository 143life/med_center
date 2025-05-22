from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        GUEST = "guest", "Гость"
        USER = "user", "Пользователь"
        ADMIN = "admin", "Администратор"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
    )

    # Автоматически даем доступ в админку для администраторов
    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)
