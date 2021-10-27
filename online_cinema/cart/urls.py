from django.contrib import admin
from django.urls import path, include
from .views import CartItemViews

urlpatterns = [
    path('cart_items/', CartItemViews.as_view()),
    path('cart_items/<int:id>/', CartItemViews.as_view()),
]