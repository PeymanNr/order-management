from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.permissions import IsOwnerOrAdmin
from order.api.serializers import OrderSerializer
from order.models import Order
from order.utils import OrderFilter


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_admin():
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)


    def get_object(self):
        obj=get_object_or_404(Order, pk=self.kwargs['pk'])
        user=self.request.user
        if not user.is_admin() and obj.user != user:
            raise PermissionDenied(
                "You do not have permission to access this order.")
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj=self.get_object()
        user=request.user
        if not user.is_admin() and obj.user != user:
            return Response(
                {'detail': 'Only admins can delete orders they do not own.'},
                status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)