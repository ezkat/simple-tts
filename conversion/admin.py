from django.contrib import admin
from .models import ConversionRequest


@admin.register(ConversionRequest)
class ConversionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')
    
    fields = (
        'status',
        'user',
        'text',
        'output'
    )
