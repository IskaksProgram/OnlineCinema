from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from cart.serializers import CartItemSerializer
from .models import CartItem
from django.shortcuts import get_object_or_404

class CartItemViews(APIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request, id=None):
        if id:
            item = CartItem.objects.get(id=id)
            serializer = CartItemSerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

        items = CartItem.objects.all()
        serializer = CartItemSerializer(items, many=True)

        # Для отображения общей цены
        total_price = []
        for item in serializer.data:
            total_price.append(item['total_sum'])
        new_serializer_data = list(serializer.data)
        new_serializer_data.append({'total_price': sum(total_price)})
        return Response({"status": "success", "data": new_serializer_data}, status=status.HTTP_200_OK)
    

    def patch(self, request, id=None):
        item = CartItem.objects.get(id=id)
        serializer = CartItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        else:
            return Response({"status": "error", "data": serializer.errors})
        
    
    def delete(self, request, id=None):
        # для полной очистки
        if id == None:
            CartItem.objects.all().delete()
        
        # для удаления одного товара
        item = get_object_or_404(CartItem, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})
    

