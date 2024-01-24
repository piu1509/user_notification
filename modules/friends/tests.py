from rest_framework.test import APITestCase
from rest_framework import status
from modules.friends.models import Friendrequest
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.

class FriendrequestTestView(APITestCase):

	# Tests the friend request list end point.
	def test_friendrequest_list(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		user1 = User.objects.create_user('username1', 'Pas$w0rd')
		friendrequest = Friendrequest.objects.create(user=user, friend=user1)
		list_url = '/friends/friend_requests/'
		response = self.client.get(list_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	#Tests the create endpoint of friend request.
	def test_friendrequest_create(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		user1 = User.objects.create_user('username1', 'Pas$w0rd')
		post_url = '/friends/friendrequest_create/'
		data = {
		"user":user.id,
		"friend":user1.id,
		}
		response = self.client.post(post_url,data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	#Tests the friend request detail end point.
	def test_friendrequest_detail(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		user1 = User.objects.create_user('username1', 'Pas$w0rd')
		friendrequest = Friendrequest.objects.create(user=user, friend=user1)
		detail_url = "/friends/friendrequest_detail/"+str(friendrequest.id)
		response = self.client.get(detail_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	#Tests the accept friend request end point.
	def test_friendrequest_accept(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		user1 = User.objects.create_user('username1', 'Pas$w0rd')
		friendrequest = Friendrequest.objects.create(user=user, friend=user1)
		accept_url = "/friends/friendrequest_accept/"+str(friendrequest.id)
		response = self.client.get(accept_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	#Tests the decline friend request end point.
	def test_friendrequest_decline(self):
		user = User.objects.create_user('username', 'Pas$w0rd')
		self.client.login(username='username', password='Pas$w0rd')
		user1 = User.objects.create_user('username1', 'Pas$w0rd')
		friendrequest = Friendrequest.objects.create(user=user, friend=user1)
		decline_url = "/friends/decline_request/"+str(friendrequest.id)
		response = self.client.get(decline_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)







