"""
Thread serializers
"""

# Standard library imports.

# Related third party imports.
from rest_framework import serializers

# Local application/library specific imports.
from .models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'

    def validate_participants(self, value):
        if len(value) > 2:
            raise serializers.ValidationError("A thread can have a maximum of 2 participants.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'sender',)
