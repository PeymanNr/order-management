import pytest
from django.contrib.auth import get_user_model
from order.models import Order
from datetime import datetime
from django.utils.timezone import make_aware
from zoneinfo import ZoneInfo

User = get_user_model()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username='admin_user', password='adminpass', role='admin')

@pytest.fixture
def customer1(db):
    return User.objects.create_user(username='cust1', password='custpass1', role='customer')

@pytest.fixture
def customer2(db):
    return User.objects.create_user(username='cust2', password='custpass2', role='customer')

@pytest.fixture
def order1(customer1):
    return Order.objects.create(
        user=customer1,
        product_name='Product A',
        quantity=1,
        price=10000,
        created_at=make_aware(datetime(2025, 7, 22), timezone=ZoneInfo('Asia/Tehran'))
    )

@pytest.fixture
def order2(customer2):
    return Order.objects.create(
        user=customer2,
        product_name='Product B',
        quantity=1,
        price=20000,
        created_at=make_aware(datetime(2025, 7, 23), timezone=ZoneInfo('Asia/Tehran'))
    )
