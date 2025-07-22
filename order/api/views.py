from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.permissions import IsOwnerOrAdmin
from order.api.serializers import OrderSerializer
from order.models import Order



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['price', 'created_at']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_admin():
            return Response(
                {'detail': 'Only admins can delete orders.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)