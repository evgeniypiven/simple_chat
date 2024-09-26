"""
Thread API Views
"""

# Standard library imports.

# Related third party imports.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

# Local application/library specific imports.
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer


class ThreadCreateListView(generics.ListCreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Retrieve threads for the currently authenticated user
        return Thread.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if a thread already exists with the given participants
            participants = serializer.validated_data.get('participants')
            existing_threads = Thread.objects.filter(participants__in=participants).distinct()
            if existing_threads.exists():
                return Response(ThreadSerializer(existing_threads, many=True).data, status=status.HTTP_200_OK)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadDeleteView(generics.DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        thread = self.get_object()
        thread.delete()
        return Response('Thread was successfully deleted', status=status.HTTP_204_NO_CONTENT)


class MessageCreateListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        return Message.objects.filter(thread_id=thread_id)

    def create(self, request, *args, **kwargs):
        thread_id = self.kwargs['thread_id']
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(thread_id=thread_id, sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageReadUpdateView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response('Message was marked as read', status=status.HTTP_204_NO_CONTENT)


class UnreadCountView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        count = Message.objects.filter(sender=request.user, is_read=False).count()
        return Response({"unread_count": count})
