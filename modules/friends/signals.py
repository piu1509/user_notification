import requests
from django.db.models.signals import post_save
from modules.friends.models import Friendrequest
from django.conf import settings

def save_post(sender, instance,created, **kwargs):
	url = 'http://localhost:8000/notifications/notification_create/'
	if settings.SIGNAL_LOGIN_USER==instance.user:
		user = instance.friend
	else:
		user = instance.user
	if created:
		data = {
		'sender': int(instance.user.id),
		'receiver': int(instance.friend.id),
		'message': 'Sent friend requests',
		}
	elif instance.status==1:
		data = {
		'sender': int(instance.friend.id),
		'receiver': int(instance.user.id),
		'message': 'Accepted friend requests',
		}
	elif instance.status==2:
		data = {
		'sender': int(settings.SIGNAL_LOGIN_USER.id),
		'receiver': int(user.id),
		'message': 'Cancelled friend request',
		}
	elif instance.status==0:
		data = {
		'sender': int(settings.SIGNAL_LOGIN_USER.id),
		'receiver': int(user.id),
		'message': 'Sent friend requests',
		}

	res = requests.post(url,json=data)
	settings.SIGNAL_LOGIN_USER = ''

post_save.connect(save_post, sender=Friendrequest)



