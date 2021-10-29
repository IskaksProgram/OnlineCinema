from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from main.views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import include, url



router = DefaultRouter()
router.register('cinema', CinemaProductViewset)
router.register('cinema_comments', CinemaReviewViewset)
router.register('cinema_favorite', CinemaReviewViewset2)

schema_view = get_schema_view(
   openapi.Info(
      title="Online_cinema Api",
      default_version='v1',
      description="Cinema-selling site \n100% Legal(no)",
      terms_of_service="https://www.google.com/policies/terms/",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include("accounts.urls")),
    path('api/v1/', include("orders.urls")),
    path('api/v1/', include("cart.urls")),

    # drf-yasg
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)