from django_filters import rest_framework as filters
from order.models import Order


class OrderFilter(filters.FilterSet):
    created_at = filters.DateFilter(field_name='created_at',
                                     lookup_expr='date')


    class Meta:
        model = Order
        fields = ['price', 'created_at']