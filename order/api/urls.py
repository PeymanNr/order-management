from rest_framework import routers
from order.api.views import OrderViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'', OrderViewSet, basename='order')


urlpatterns = [
    path('', include(router.urls)),
]