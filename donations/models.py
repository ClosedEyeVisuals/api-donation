from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Collect(models.Model):
    """Модель, описывающая параметры сбора денежных средств."""
    class Reason(models.TextChoices):
        VACATION = 'vacation', 'Отпуск'
        WEDDING = 'wedding', 'Свадьба'
        HB = 'hb', 'День рождения'

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='fees',
        verbose_name='Владелец'
    )
    title = models.CharField(
        max_length=128,
        verbose_name='Название'
    )
    reason = models.CharField(
        max_length=64,
        choices=Reason.choices,
        verbose_name='Причина сбора'
    )
    description = models.TextField(
        'Описание сбора',
        blank=True,
        null=True
    )
    goal_value = models.PositiveIntegerField(
        'Сумма сбора'
    )
    current_value = models.IntegerField(
        'Собрано средств',
        default=0
    )
    image = models.ImageField(
        'Обложка',
        upload_to='collects/images/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        'Начало сбора',
        auto_now_add=True
    )
    finish_at = models.DateTimeField(
        'Конец сбора'
    )

    class Meta:
        verbose_name = 'Сбор'
        verbose_name_plural = 'сборы'
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Payment(models.Model):
    """Модель пожертвования."""
    collect = models.ForeignKey(
        Collect,
        on_delete=models.CASCADE,
        verbose_name='Сбор'
    )
    payment_date = models.DateTimeField(
        'Дата платежа',
        auto_now_add=True
    )
    total = models.PositiveIntegerField(
        'Сумма пожертвования'
    )
    payer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Плательщик'
    )

    class Meta:
        verbose_name = 'Пожертвование'
        verbose_name_plural = 'пожертвования'
        ordering = ('-payment_date', '-total')
        default_related_name = 'payments'

    def __str__(self):
        return f'{self.payment_date} - {self.total}'
