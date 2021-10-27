from .views import OrderHistoryView, OrderViewset
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('orderitems', OrderItemViewset)
router.register('orders', OrderViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("orderhistory/", OrderHistoryView.as_view()),
]