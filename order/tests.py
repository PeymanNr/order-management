from rest_framework.test import APITestCase
from django.urls import reverse
from order.models import Order
from datetime import datetime
from django.utils.timezone import make_aware, timezone
from django.contrib.auth import get_user_model
from rest_framework import status
from zoneinfo import ZoneInfo

User = get_user_model()

class OrderAPITestCase(APITestCase):

    def setUp(self):
        self.admin=User.objects.create_user(username='admin_user',
                                            password='adminpass', role='admin')
        self.customer1=User.objects.create_user(username='cust1',
                                                password='custpass1',
                                                role='customer')
        self.customer2=User.objects.create_user(username='cust2',
                                                password='custpass2',
                                                role='customer')

        self.order1=Order.objects.create(
            user=self.customer1,
            product_name='Product A',
            quantity=1,
            price=10000,
            created_at=make_aware(datetime(2025, 7, 22),
                                  timezone=ZoneInfo('Asia/Tehran'))
        )

        self.order2=Order.objects.create(
            user=self.customer2,
            product_name='Product B',
            quantity=1,
            price=20000,
            created_at=make_aware(datetime(2025, 7, 23),
                                  timezone=ZoneInfo('Asia/Tehran'))
        )



    def test_admin_can_view_all_orders(self):
        self.client.login(username='admin_user', password='adminpass')
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_customer_can_view_own_orders(self):
        self.client.login(username='cust1', password='custpass1')
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product_name'], 'Product A')

    def test_customer_cannot_view_others_orders(self):
        self.client.login(username='cust1', password='custpass1')
        url = reverse('order-detail', kwargs={'pk': self.order2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_can_create_order(self):
        self.client.login(username='cust1', password='custpass1')
        data = {
            'product_name': 'New Product',
            'quantity': 1,
            'price': 5000
        }
        response = self.client.post(reverse('order-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.customer1.id)

    def test_admin_can_update_order(self):
        self.client.login(username='admin_user', password='adminpass')
        url = reverse('order-detail', kwargs={'pk': self.order1.id})
        data = {
            'product_name': 'Updated Product',
            'quantity': 1,
            'price': 9999
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], 'Updated Product')

    def test_customer_can_update_own_order(self):
        self.client.login(username='cust1', password='custpass1')
        url = reverse('order-detail', kwargs={'pk': self.order1.id})
        data = {
            'product_name': 'Customer Update',
            'quantity': 1,
            'price': 8888
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_cannot_update_others_order(self):
        self.client.login(username='cust1', password='custpass1')
        url = reverse('order-detail', kwargs={'pk': self.order2.id})
        data = {
            'product_name': 'Hack Attempt',
            'quantity': 1,
            'price': 1
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_order(self):
        self.client.login(username='admin_user', password='adminpass')
        url = reverse('order-detail', kwargs={'pk': self.order2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_customer_can_delete_own_order(self):
        self.client.login(username='cust1', password='custpass1')
        url = reverse('order-detail', kwargs={'pk': self.order1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_customer_cannot_delete_others_order(self):
        self.client.login(username='cust1', password='custpass1')
        url = reverse('order-detail', kwargs={'pk': self.order2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_filter_orders_by_price(self):
        self.client.login(username='admin_user', password='adminpass')
        response = self.client.get(reverse('order-list') + '?price=10000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product_name'], 'Product A')

    def test_admin_can_filter_orders_by_date(self):
        self.client.login(username='admin_user', password='adminpass')
        response=self.client.get(
            reverse('order-list') + '?created_at=2025-07-22')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['product_name'], 'Product B')
