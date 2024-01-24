from django.shortcuts import render, redirect
from modules.friends.models import Friendrequest
from modules.friends.serializers import CreateRequestSerializer, ListRequestSerializer
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin
import requests
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class FriendrequestCreate(GenericAPIView, CreateModelMixin):
	"""
		Handles the process of sending a friend request.
	"""
	queryset = Friendrequest.objects.all()
	serializer_class = CreateRequestSerializer

	def post(self, request, *args, **kwargs):
		sent_list = "sent_list"+str(self.request.user.id)
		try:
			friend_request = Friendrequest.objects.get(Q(user__id=request.data['user'], friend__id=request.data['friend'])|Q(user__id=request.data['friend'], friend__id=request.data['user']))
			if friend_request:
				if friend_request.status==2:
					settings.SIGNAL_LOGIN_USER = self.request.user
					friend_request.pending()
					friend_request.save()
					if cache.has_key(sent_list):
						cache.delete(sent_list)
					return Response({"msg":"Request sent successfully."})
				return Response({"msg":"Request already sent."})
		except:
			if cache.has_key(sent_list):
				cache.delete(sent_list)
			response = self.create(request, *args, **kwargs)
			return response
			

class ListRequest(ListAPIView):
	"""
		Lists out all the friend requests.
	"""
	queryset = Friendrequest.objects.all()
	serializer_class = ListRequestSerializer
	
	def get_queryset(self):
		friendrequest_list = "friendrequest_list"+str(self.request.user.id)
		if cache.get(friendrequest_list):
			print('------------cache----------')
			list_friendrequests = cache.get(friendrequest_list)			
			return list_friendrequests
		else:
			print('------------db----------')
			friendrequests = Friendrequest.objects.filter(friend=self.request.user)
			cache.set(friendrequest_list, friendrequests)
			return friendrequests
	

class RequestDetail(GenericAPIView, RetrieveModelMixin):
	"""
		Details of a friend request.
	"""
	queryset = Friendrequest.objects.all()
	serializer_class = ListRequestSerializer

	def get(self, request, *args, **kwargs):
		friendrequest_detail = "friendrequest_detail_"+str(self.kwargs['pk'])
		print()
		if cache.get(friendrequest_detail):
			print('------------cache----------')
			friendrequest_data = cache.get(friendrequest_detail)
			return Response(friendrequest_data)
		else:
			print('------------db----------')
			response = self.retrieve(request, *args, **kwargs)
			cache.set(friendrequest_detail, response.data)
			return response
	

class FriendrequestAccept(GenericAPIView, ListModelMixin):
	"""
		Handles the process of accepting a friend request.
	"""
	queryset = Friendrequest.objects.all()

	def get(self, request, pk):
		instance = self.get_queryset().get(pk=pk)
		friendrequest_list = "friendrequest_list"+str(self.request.user.id)
		friendrequest_detail = "friendrequest_detail_"+str(pk)
		friend_list = "friend_list"+str(self.request.user.id)
		pending_list = "pending_list"+str(self.request.user.id)
		instance.accept()
		instance.save()
		if cache.has_key(friend_list):
			cache.delete(friend_list)
		if cache.has_key(pending_list):
			cache.delete(pending_list)
		return Response({"msg":"Request accepted."})


class DeclineRequest(GenericAPIView, ListModelMixin):
	"""
		Handles the process of declining a friend request.
	"""
	queryset = Friendrequest.objects.all()

	def get(self, request, pk):
		settings.SIGNAL_LOGIN_USER = self.request.user
		instance = self.get_queryset().get(pk=pk)
		friendrequest_detail = "friendrequest_detail_"+str(pk)
		sent_list = "sent_list"+str(self.request.user.id)
		pending_list = "pending_list"+str(self.request.user.id)		
		instance.decline()
		instance.save()
		if instance.user==self.request.user:
			if cache.has_key(sent_list):
				cache.delete(sent_list)
		if instance.friend==self.request.user:
			if cache.has_key(pending_list):
				cache.delete(pending_list)
		return Response({"msg":"Request cancelled/declined."})


class Friendrequests(GenericAPIView, ListModelMixin):
	queryset = Friendrequest.objects.all()
	serializer_class = ListRequestSerializer
	renderer_classes = [TemplateHTMLRenderer]
	template_name = "friends/list.html"

	def get(self, request, *args, **kwargs):
		friend_list = "friend_list"+str(self.request.user.id)
		pending_list = "pending_list"+str(self.request.user.id)
		sent_list = "sent_list"+str(self.request.user.id)

		if cache.get(friend_list):
			print("------cache friends------")
			friends = cache.get(friend_list)
		else:
			print("-----db friends-----")
			friends = self.get_queryset().filter(Q(user=self.request.user, status=1)|Q(friend=self.request.user, status=1))
			cache.set(friend_list, friends)
		if cache.get(pending_list):
			print("------cache pending-------")
			pending_requests = cache.get(pending_list)
		else:
			print("-----db pending-----")			
			pending_requests = self.get_queryset().filter(friend=self.request.user, status=0)
			cache.set(pending_list, pending_requests)
		if cache.get(sent_list):
			print("------cache sent-------")
			sent_requests = cache.get(sent_list)				
		else:
			print("-----db sent-----")			
			sent_requests = self.get_queryset().filter(user=self.request.user, status=0)
			response = self.list(request, *args, **kwargs)			 
			cache.set(sent_list, sent_requests)
		return Response({"friends":friends,"pending_requests":pending_requests, "sent_requests":sent_requests})
	
