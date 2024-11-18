from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import random
import time
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
    
    def create_history_entry(self):
        ConversionRequestHistory.objects.create(conversion_request=self, text=self.text, status=self.status)

    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.create_history_entry()
        return instance
    
    def process_tts(self):
        logger.info('Processing TTS')
        self.status = ConversionRequest.IN_PROGRESS
        self.save()

        time.sleep(random.randint(3, 6))

        try:
            if random.randint(0,100) == 50:
                raise Exception("SuddenException")
            
            file_name = f'tts_output_{self.pk}.wav'
            dummy_file = ContentFile('dummy tts output file', name=file_name)
            self.output.save(file_name, dummy_file) # This will create a second "IN_PROGRESS" entry, add more verbose status_message later?

            self.status = ConversionRequest.COMPLETED
            self.save()
        except Exception as exc:
            logger.error(exc)
            self.status = ConversionRequest.FAILED
            self.save()
        


class ConversionRequestHistory(models.Model):
    conversion_request = models.ForeignKey(ConversionRequest,
                                           related_name='history', on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    status = models.CharField(max_length=15, choices=ConversionRequest.STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('id', )

    
    def __str__(self):
        return 'Conversion Request History'
