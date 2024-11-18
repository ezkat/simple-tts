import html
import re

from rest_framework import serializers
from .models import ConversionRequest, ConversionRequestHistory


class ConversionRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionRequestHistory
        fields = ('text', 'status', 'timestamp')


class ConversionRequestSerializer(serializers.ModelSerializer):
    history = ConversionRequestHistorySerializer(many=True, read_only=True)
    class Meta:
        model = ConversionRequest
        fields = ('id', 'text', 'status', 'history', 'output')
        read_only_fields = ('id', 'status', 'history', 'output')

    def validate_text(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Text cannot be empty or just whitespace.")
        
        value = html.escape(value)
        value = re.sub(r'[^\x20-\x7E]', '', value) # Remove non-printable characters.

        if len(value) > 300:
            raise serializers.ValidationError("Text is too long.")
        
        return value
