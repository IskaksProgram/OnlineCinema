from django.db.models import fields
from rest_framework import serializers
from rest_framework.response import Response
from orders.models import *

class OrderSerializer(serializers.ModelSerializer):
    """
    Создает заказ и добавляет его в историю заказов.
    """
    class Meta:
        model = Order
        fields = "__all__"
    
    created_at = serializers.DateTimeField(
        read_only=True
    )
    status = serializers.CharField(
        read_only=True
    )


    def create(self, validated_data):
        request = self.context.get('request')
        print(request)
        user_email = request.user
        order = Order.objects.create(user=user_email, **validated_data)
        
        # Создает копию с урезанной информацией, добавляет её в историю заказов
        order_history = OrderHistory.objects.create(
            user=user_email,
            total_sum=validated_data.get('total_sum'))
        return order


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = "__all__"
