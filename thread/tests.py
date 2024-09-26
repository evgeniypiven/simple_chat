"""
Thread tests
"""

# Standard library imports.

# Related third party imports.
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User

# Local application/library specific imports.
from .models import Thread, Message


class ThreadTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(email='test@test.com', username='user1', password='pass')
        self.user2 = User.objects.create_user(email='test2@test.com', username='user2', password='pass')
        self.token = self.user1.token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_thread(self):
        url = '/thread/threads/'
        data = {
            "participants": [self.user1.id, self.user2.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Thread.objects.count(), 1)

    def test_get_threads(self):
        thread = Thread.objects.create()
        thread.participants.add(self.user1, self.user2)

        url = '/thread/threads/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_thread(self):
        thread = Thread.objects.create()
        thread.participants.add(self.user1, self.user2)

        url = f'/thread/threads/delete/{thread.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Thread.objects.count(), 0)


class MessageTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(email='test@test.com', username='user1', password='pass')
        self.user2 = User.objects.create_user(email='test2@test.com', username='user2', password='pass')
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)
        self.token = self.user1.token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_message(self):
        url = f'/thread/threads/{self.thread.id}/messages/'
        data = {
            "text": "Hello!",
            "sender": self.user1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)

    def test_get_messages(self):
        Message.objects.create(thread=self.thread, sender=self.user1, text="Hello!")
        url = f'/thread/threads/{self.thread.id}/messages/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_message_as_read(self):
        message = Message.objects.create(thread=self.thread, sender=self.user1, text="Hello!")
        url = f'/thread/messages/{message.id}/mark_as_read/'
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        message.refresh_from_db()
        self.assertTrue(message.is_read)


class UnreadCountTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(email='test@test.com', username='user1', password='pass')
        self.token = self.user1.token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_unread_count(self):
        thread = Thread.objects.create()
        thread.participants.add(self.user1)
        Message.objects.create(sender=self.user1, thread=thread, text="Hello!", is_read=False)

        url = '/thread/unread_count/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)

    def test_unread_count_no_unread_messages(self):
        url = '/thread/unread_count/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 0)
