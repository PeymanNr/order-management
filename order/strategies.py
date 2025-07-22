from order.models import Order


class OrderQueryStrategy:
    def get_queryset(self, user):
        raise NotImplementedError


class AdminOrderQueryStrategy(OrderQueryStrategy):
    def get_queryset(self, user):
        return Order.objects.all()


class CustomerOrderQueryStrategy(OrderQueryStrategy):
    def get_queryset(self, user):
        return Order.objects.filter(user=user)


def get_query_strategy(user):
    if user.is_admin():
        return AdminOrderQueryStrategy()
    return CustomerOrderQueryStrategy()
