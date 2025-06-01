from django.db import models


class TimedBaseModel(models.Model):
    """Абстрактный класс для всех моделей"""

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        """Сделать класс абстрактным, чтобы он не создавался, как модель"""

        abstract = True
