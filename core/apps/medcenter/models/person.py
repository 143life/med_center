from django.db import models
from core.apps.common.models import TimedBaseModel

class Person(TimedBaseModel):
    """модель для таблицы 'person' """

    first_name = models.CharField(
        'Имя',
        max_length=25
        )
    last_name = models.CharField(
        'Фамилия',
        max_length=25
        )
    patronymic = models.CharField(
        'Отчество',
        max_length=25
        )
    date_birth = models.DateField(
        'Дата рождения'
        )
    #is_visible = models.BooleanField('Виден ли в списке', default=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'
