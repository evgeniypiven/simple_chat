"""
Thread Models
"""

# Standard library imports.


# Related third party imports.
from django.db import models

# Local application/library specific imports.
from authentication.models import User


class Thread(models.Model):
    participants = models.ManyToManyField(User, limit_choices_to={'is_active': True})
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(Thread, related_name='messages', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
