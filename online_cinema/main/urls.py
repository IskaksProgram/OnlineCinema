from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import CinemaProductViewset

router = DefaultRouter()
# router.register(r'main', CinemaProduct)
router.register(r'main', CinemaProductViewset)

urlpatterns = router.urls
