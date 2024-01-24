from modules.friends.models import Friendrequest
from rest_framework import serializers


class CreateRequestSerializer(serializers.ModelSerializer):
	"""
		Serializer class for sending a friend request.
	"""
	class Meta:
		model = Friendrequest
		fields = ['user', 'friend']
		

class ListRequestSerializer(serializers.ModelSerializer):
	"""
		Serializer class for listing out all requests.
	"""
	class Meta:
		model = Friendrequest
		fields = ['gid','slug','user','friend','status','date_created']




