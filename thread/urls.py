"""
Thread API Urls
"""

# Standard library imports.
from django.urls import path

# Related third party imports.

# Local application/library specific imports.
from .views import (
    ThreadCreateListView,
    ThreadDeleteView,
    MessageCreateListView,
    MessageReadUpdateView,
    UnreadCountView
)

urlpatterns = [
    path('threads/', ThreadCreateListView.as_view(), name='thread-list-create'),
    path('threads/delete/<int:pk>/', ThreadDeleteView.as_view(), name='thread-delete'),
    path('threads/<int:thread_id>/messages/', MessageCreateListView.as_view(), name='message-list-create'),
    path('messages/<int:pk>/mark_as_read/', MessageReadUpdateView.as_view(), name='message-mark-as-read'),
    path('unread_count/', UnreadCountView.as_view(), name='unread-count'),
]
