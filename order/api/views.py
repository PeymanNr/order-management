from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.permissions import IsOwnerOrAdmin
from order.api.serializers import OrderSerializer
from order.models import Order
from order.filters import OrderFilter
from order.strategies import get_query_strategy


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user orders.

    Permissions:
        - Authenticated users only.
        - Only admins or owners can access individual orders.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter
    ordering_fields = ["price", "created_at"]

    def get_queryset(self):
        """
        Return a queryset using a dynamic strategy
        based on the current user's role.
        """

        strategy = get_query_strategy(self.request.user)
        return strategy.get_queryset(self.request.user)

    def get_object(self):
        """
        Retrieve a specific order instance.

        Raises:
            PermissionDenied: If the user is not allowed to access the order.
        """

        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        user = self.request.user
        if not user.is_admin() and order.user != user:
            raise PermissionDenied("You do not have permission to access this order.")
        return order

    def perform_create(self, serializer):
        """
        Save a new order instance linked to the current user.
        """

        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an order instance.

        Only admins can delete others' orders.
        """

        obj = self.get_object()
        user = request.user
        if not user.is_admin() and obj.user != user:
            return Response(
                {"detail": "Only admins can delete orders they do not own."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().destroy(request, *args, **kwargs)
