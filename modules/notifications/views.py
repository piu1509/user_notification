from django.shortcuts import render
from modules.notifications.models import Notification
from modules.notifications.serializers import ListNotificationSerializer, CreateNotificationSerializer
from rest_framework.generics import ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class NotificationCreate(CreateModelMixin,GenericAPIView):
	"""
		Handles the process of sending a notification.
	"""
	queryset = Notification.objects.all()
	serializer_class = CreateNotificationSerializer

	def post(self,request,*args,**kwargs):
		return self.create(request, *args, **kwargs)


class NotificationList(ListAPIView):
	"""
		Handles process of listing out all the notifications.
	"""
	queryset = Notification.objects.all()
	serializer_class = ListNotificationSerializer

	def get_queryset(self):
		notification_list = "notification_list"+str(self.request.user.id)
		if cache.get(notification_list):
			print('------------cache----------')
			list_notifications = cache.get(notification_list)
			return list_notifications
		else:
			print('------------db----------')
			notifications = Notification.objects.filter(receiver=self.request.user)
			cache.set(notification_list, notifications)
			return notifications


class NotificationDetail(GenericAPIView, RetrieveModelMixin):
	"""
		Displays the details of a notification.
	"""
	queryset = Notification.objects.all()
	serializer_class = ListNotificationSerializer

	def get(self,request,*args, **kwargs):
		notification_detail = "notification_detail_"+str(self.kwargs['pk'])
		if cache.get(notification_detail):
			print('------------cache----------')
			notification_data = cache.get(notification_detail)
			return Response(notification_data)
		else:
			print('------------db----------')
			response = self.retrieve(request, *args, **kwargs)
			cache.set(notification_detail, response.data)
			return response


class UnreadNotificationCount(APIView):
	"""
		Counts the total number of unread notifications.
	"""
	queryset = Notification.objects.all()

	def get(self, request):
		count = Notification.objects.filter(receiver=request.user, is_count=False).count()
		return Response({'count':count})












