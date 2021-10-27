from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import permissions

from orders.models import *
from orders.serializers import *

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

    def get_serializer_context(self):
        return {
            "request": self.request
        }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class OrderHistoryView(ListAPIView):
    queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return OrderHistory.objects.filter(user=user)