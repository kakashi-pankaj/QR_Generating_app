from django.db import models

class QRCode(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='qrcodes/')
