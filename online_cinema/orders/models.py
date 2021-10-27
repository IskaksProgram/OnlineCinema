from django.db import models
from django.contrib.auth import get_user_model
from model_utils.choices import Choices
from model_utils.fields import StatusField
from main.models import CreatedatModel

User = get_user_model()

class Order(CreatedatModel):
    """
    Класс для создания заказа
    """
    STATUS = Choices(
        "Готовится к отправке", "Находится в пути",
        "Ожидает клиента на почте", "Доставлен"
    )

    total_sum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT,
        related_name='orders', null=True
    )
    
    order_status = StatusField()

    class Meta:
        ordering = ['-created_at']
        db_table = 'order'
    
    def __str__(self) -> str:
        return f"Закакз №{self.id} от {self.created_at.strftime('%d-%m-%Y %H:%M')}"


class OrderHistory(CreatedatModel):
    """
    Создается в сериализаторе вместе с Order, 
    но хранит в себе меньше информации и не удаляется 
    после выполнения заказа.
    """
    total_sum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT,
        related_name='order', null=True
    )

    class Meta:
        ordering = ['-created_at']
        db_table = 'order_history'
    
    def __str__(self) -> str:
        return f"Закакз №{self.id} от {self.created_at.strftime('%d-%m-%Y %H:%M')}"