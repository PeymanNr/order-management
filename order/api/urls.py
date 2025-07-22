from rest_framework import routers
from django.urls import path, include
from order.api.views import OrderViewSet

router = routers.DefaultRouter()
router.register(r'', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]