
import re
from main.models import CinemaProduct
from rest_framework import serializers
from .models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(max_length=200)
    product_price = serializers.FloatField()
    product_quantity = serializers.IntegerField(required=False, default=1)

    
    class Meta:
        model = CartItem
        fields = ('__all__')
    
    def to_representation(self, instance):
        representation = super(
            CartItemSerializer, self
        ).to_representation(instance)
        
        total_item_price = 0
        total_item_price += representation['product_price'] * representation['product_quantity']
        representation['total_sum'] = int(total_item_price)
    
        return representation
    
    
