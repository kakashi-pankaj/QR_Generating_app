from django.test import TestCase, Client
from django.urls import reverse
from .models import QRCode

class QRCodeGeneratorTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qrgenerator/home.html')

    def test_qrcode_generation(self):
        response = self.client.post(reverse('home'), {'text': 'https://example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qrgenerator/home.html')
        qr_code = QRCode.objects.first()
        self.assertIsNotNone(qr_code)
        self.assertEqual(qr_code.text, 'https://example.com')

    def test_qrcode_display(self):
        qr_code = QRCode.objects.create(text='https://example.com')
        response = self.client.get(reverse('home'))
        self.assertContains(response, f'<img src="{qr_code.image.url}"', html=True)
