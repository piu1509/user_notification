from rest_framework import serializers
from modules.notifications.models import Notification


class CreateNotificationSerializer(serializers.ModelSerializer):
	"""
		Serializer class for creating a new notification.
	"""
	class Meta:
		model = Notification
		fields = ['sender','receiver','message']


class ListNotificationSerializer(serializers.ModelSerializer):
	"""
		Serializer class for listing out all the notifications.
	"""
	class Meta:
		model = Notification
		fields = ['gid','slug','sender','receiver','message','is_read','read_date','date_created']

