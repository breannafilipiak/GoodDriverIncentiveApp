from django.test import Client, RequestFactory, TestCase
from unittest import skip
from .models import Category, Product
# from django.contrib.auth.models import User
from django.http import HttpRequest 
from .views import products, product

# Create your tests here.

class Test_Model_Category(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(name = 'category_test', slug = 'category_test')

    def test_category_model_insertion(self):
        data = self.data1
        self.assertTrue(isinstance(data, Category))

    def test_category_model_return(self):
        data = self.data1
        self.assertEqual(str(data), 'category_test')

class Test_Model_Product(TestCase):

    def setUp(self):
        Category.objects.create(name = 'category_test', slug = 'category_test')
        self.data1 = Product.objects.create(category_id = 1, title = 'Test_Product_Title', 
                                            slug = 'Test_Product_Title', price = '20.00', 
                                            point_value = '20', quantity = '10', description = 'test product description')

    def test_product_model_insertion(self):
        data = self.data1
        self.assertTrue(isinstance(data, Product))

    def test_category_model_return(self):
        data = self.data1
        self.assertEqual(str(data), 'Test_Product_Title')

    class Test_Response(TestCase):
        def setUp(self):
            self.c = Client()
            self.factory = RequestFactory()
            User.objects.create(username = 'admin')
            Category.objects.create(name = 'response request', slug = 'response-request')
            Product.objects.create(category_id = 1, title = 'Response Request Test' , created_by_id = 1, 
                                    slug = 'response-request-test', price = '20.00')
        def test_hosts(self):
            response = self.c.get('/', HTTP_HOST = 'randomurl.com')
            self.assertEqual(response.status_code, 400)
            response = self.c.get('/', HTTP_HOST = '127.0.0.1')
            self.assertEqual(response.status_code, 200)