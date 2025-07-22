import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_admin_can_view_all_orders(client, admin_user, order1, order2):
    client.login(username='admin', password='adminpass')
    response = client.get(reverse('order-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

@pytest.mark.django_db
def test_customer_can_view_own_orders(client, customer1, order1, order2):
    client.login(username='cust1', password='custpass1')
    response = client.get(reverse('order-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['product_name'] == 'Product A'

@pytest.mark.django_db
def test_customer_cannot_view_others_orders(client, customer1, order2):
    client.login(username='cust1', password='custpass1')
    url = reverse('order-detail', kwargs={'pk': order2.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_customer_can_create_order(client, customer1):
    client.login(username='cust1', password='custpass1')
    data = {
        'product_name': 'New Product',
        'quantity': 1,
        'price': 5000
    }
    response = client.post(reverse('order-list'), data, content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['product_name'] == 'New Product'

@pytest.mark.django_db
def test_admin_can_update_order(client, admin_user, order1):
    client.login(username='admin', password='adminpass')
    url = reverse('order-detail', kwargs={'pk': order1.id})
    data = {'product_name': 'Updated', 'quantity': 2, 'price': 9000}
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['product_name'] == 'Updated'

@pytest.mark.django_db
def test_customer_cannot_update_others_order(client, customer1, order2):
    client.login(username='cust1', password='custpass1')
    url = reverse('order-detail', kwargs={'pk': order2.id})
    data = {'product_name': 'Hack', 'quantity': 1, 'price': 1}
    response = client.put(url, data, content_type='application/json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_admin_can_filter_orders_by_price(client, admin_user, order1, order2):
    client.login(username='admin', password='adminpass')
    url = reverse('order-list') + '?price=10000'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['product_name'] == 'Product A'

@pytest.mark.django_db
def test_admin_can_filter_orders_by_date(client, admin_user, order1, order2):
    client.login(username='admin', password='adminpass')
    url = reverse('order-list') + '?created_at=2025-07-22'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['product_name'] == 'Product B'