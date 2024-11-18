from django.test import TestCase
from django.utils.translation import override as translation_override
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import ConversionRequest




class ConversionRequestHistoryInline(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='1234')
        auth_response = self.client.post('/api/v1/auth/token/', {'username': 'test_user', 'password': '1234'})
        self.assertEqual(auth_response.status_code, 200)
        access_token = auth_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_create_conversion_request(self):
        response = self.client.post('/api/v1/conversion_requests/', {'text': 'Curabitur varius dolor vel pellentesque pharetra'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ConversionRequest.objects.count(), 1)

    @translation_override('en')
    def test_fail_create_invalid_conversion_request(self):
        response = self.client.post('/api/v1/conversion_requests/', {'text': 'Test'*100})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['text'][0], 'Ensure this field has no more than 300 characters.')

    def test_retrieve_conversion_requests(self):
        ConversionRequest.objects.create(user=self.user, text='Lorem ipsum dolor sit amet, consectetur adipiscing elit')
        ConversionRequest.objects.create(user=self.user, text='Donec fringilla dapibus velit nec fermentum')
        response = self.client.get('/api/v1/conversion_requests/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_fail_retrieve_other_user_conversion_requests(self):
        other_user = User.objects.create_user(username='other_test_user', password='4321')
        conversion_request = ConversionRequest.objects.create(user=other_user, text='Lorem ipsum dolor sit amet, consectetur adipiscing elit')
        response = self.client.get(f'/api/v1/conversion_requests/{conversion_request.id}/')
        self.assertEqual(response.status_code, 404)


    def test_update_conversion_request(self):
        response = self.client.post('/api/v1/conversion_requests/', {'text': 'Donec vel lorem et erat laoreet consequat'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['text'], 'Donec vel lorem et erat laoreet consequat')

        response_id = response.data['id']
        response = self.client.put(f'/api/v1/conversion_requests/{response_id}/', {'text': 'Morbi tristique accumsan dictum'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['text'], 'Morbi tristique accumsan dictum')

    def test_delete_conversion_request(self):
        conversion_request = ConversionRequest.objects.create(user=self.user, text='Lorem ipsum dolor sit amet, consectetur adipiscing elit')
        response = self.client.delete(f'/api/v1/conversion_requests/{conversion_request.id}/')
        self.assertEqual(response.status_code, 204)
