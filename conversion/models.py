from django.db import models
from django.contrib.auth.models import User
import logging


logger = logging.getLogger()

class ConversionRequest(models.Model):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed')
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    output = models.FileField(upload_to='tts_outputs/', blank=True, null=True)



    def __str__(self):
        return f'{self.user.username} - {self.status}'
