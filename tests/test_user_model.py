import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_admin_user(admin_user):
    assert admin_user.username == "admin"
    assert admin_user.check_password("adminpass")
    assert admin_user.role == User.Roles.ADMIN
    assert admin_user.is_admin() is True
    assert admin_user.is_customer() is False
    assert admin_user.is_staff is False
    assert admin_user.is_superuser is False


@pytest.mark.django_db
def test_create_customer_user(customer1):
    assert customer1.username == "cust1"
    assert customer1.check_password("custpass1")
    assert customer1.role == User.Roles.CUSTOMER
    assert customer1.is_customer() is True
    assert customer1.is_admin() is False
    assert customer1.is_staff is False
    assert customer1.is_superuser is False


@pytest.mark.django_db
def test_create_user_without_username_raises():
    with pytest.raises(ValueError):
        User.objects.create_user(username=None, password="pass")


@pytest.mark.django_db
def test_is_admin_and_is_customer_methods():
    admin = User.objects.create_user(
        username="admin2", password="pass", role=User.Roles.ADMIN
    )
    customer = User.objects.create_user(
        username="cust2", password="pass", role=User.Roles.CUSTOMER
    )

    assert admin.is_admin() is True
    assert admin.is_customer() is False

    assert customer.is_admin() is False
    assert customer.is_customer() is True
