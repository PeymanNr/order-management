import unittest
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelUnitTest(TestCase):

    def test_create_admin_user(self):
        admin = User.objects.create_user(username='adminuser', password='adminpass', role=User.Roles.ADMIN)
        self.assertEqual(admin.username, 'adminuser')
        self.assertTrue(admin.check_password('adminpass'))
        self.assertEqual(admin.role, User.Roles.ADMIN)
        self.assertTrue(admin.is_admin())
        self.assertFalse(admin.is_customer())
        self.assertFalse(admin.is_staff)
        self.assertFalse(admin.is_superuser)

    def test_create_customer_user(self):
        customer = User.objects.create_user(username='customer1', password='custpass', role=User.Roles.CUSTOMER)
        self.assertEqual(customer.username, 'customer1')
        self.assertTrue(customer.check_password('custpass'))
        self.assertEqual(customer.role, User.Roles.CUSTOMER)
        self.assertTrue(customer.is_customer())
        self.assertFalse(customer.is_admin())
        self.assertFalse(customer.is_staff)
        self.assertFalse(customer.is_superuser)

    def test_create_user_without_username_raises(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(username=None, password='pass')

    def test_is_admin_and_is_customer_methods(self):
        admin = User.objects.create_user(username='admin2', password='pass', role=User.Roles.ADMIN)
        customer = User.objects.create_user(username='cust2', password='pass', role=User.Roles.CUSTOMER)

        self.assertTrue(admin.is_admin())
        self.assertFalse(admin.is_customer())

        self.assertFalse(customer.is_admin())
        self.assertTrue(customer.is_customer())

if __name__ == '__main__':
    unittest.main()
