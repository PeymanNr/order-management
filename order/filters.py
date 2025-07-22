from django_filters import rest_framework as filters
from order.models import Order


class OrderFilter(filters.FilterSet):
    created_at = filters.DateFilter(field_name='created_at', lookup_expr='date')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    product_name = filters.CharFilter(field_name='product_name', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['price', 'created_at']