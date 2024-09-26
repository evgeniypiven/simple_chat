"""
Thread admin
"""

# Standard library imports.

# Related third party imports.
from django.contrib import admin

# Local application/library specific imports.
from .models import Thread, Message
from .forms import ThreadForm


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    form = ThreadForm
    list_display = ('id', 'created', 'updated')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'text', 'thread', 'created', 'is_read')
