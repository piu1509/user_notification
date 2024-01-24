from rest_framework.test import APITestCase
from rest_framework import status
from modules.notifications.models import Notification
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.

class NotificationTestView(APITestCase):

	#Tests the notification list end point.
	def test_notificationlist(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		user1 = User.objects.create_user('username1', 'Pas$w0rd')
		notification = Notification.objects.create(sender=user, receiver=user1,message="Notification")
		list_url = '/notifications/notification_list/'
		response = self.client.get(list_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	#Tests the create notification end point.
	def test_notification_create(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		user1 = User.objects.create_user('username1', 'Pas$w0rd')
		post_url = '/notifications/notification_create/'
		data = {
		"sender":user.id,
		"receiver":user1.id,
		"message":"created",
		}
		response = self.client.post(post_url,data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	#Tests the notification detail end point.
	def test_notification_detail(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		user1 = User.objects.create_user('username1', 'Pas$w0rd')
		notification = Notification.objects.create(sender=user, receiver=user1, message='Notification')
		detail_url = "/notifications/notification_detail/"+str(notification.id)
		response = self.client.get(detail_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	#Tests the new notification count end point.
	def test_notification_count(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		url = "/notifications/unread_notification_count/"
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)







	