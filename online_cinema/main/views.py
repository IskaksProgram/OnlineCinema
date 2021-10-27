# products = main

from rest_framework import permissions
from main.serializers import *
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from main.models import CinemaProduct
from main.serializers import CinemaProductSerializer
from likes.mixins import LikedMixin
from rest_framework import filters as rest_filters
from django_filters import rest_framework as filters


class CinemaProductViewset(LikedMixin, viewsets.ModelViewSet):
    queryset = CinemaProduct.objects.all()
    serializer_class = CinemaProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter
    ]
    filterset_fields = ['price', 'salesman', 'genre']
    search_fields = ['title', 'description']

    def get_permissions(self, obj=None):
        if self.action in ['create', 'update', 'partical_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return []

class CinemaReviewViewset(viewsets.ModelViewSet):
    queryset = CinemaProductReview.objects.all()
    serializer_class = CinemaReviewSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]