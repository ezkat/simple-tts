from django.contrib import admin
from django_admin_inline_paginator.admin import TabularInlinePaginated
from .models import ConversionRequest, ConversionRequestHistory



class ConversionRequestHistoryInline(TabularInlinePaginated):
    per_page = 5
    model = ConversionRequestHistory
    extra = 0
    fields = (
        'timestamp',
        'status',
        'text'
    )
    ordering = ('-timestamp', )
    readonly_fields = fields
    can_delete = False

    def has_add_permission(self, *args, **kwargs):
        return False

@admin.register(ConversionRequest)
class ConversionRequestAdmin(admin.ModelAdmin):
    inlines = (
        ConversionRequestHistoryInline,
    )

    list_display = ('user', 'status', 'timestamp')
    
    fields = (
        'status',
        'user',
        'text',
        'output'
    )


    def timestamp(self, obj):
        return obj.history.last().timestamp
