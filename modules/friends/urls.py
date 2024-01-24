from django.urls import path
from modules.friends import views

app_name = 'friends'

urlpatterns = [
	path('friendrequest_create/', views.FriendrequestCreate.as_view(), name='friendrequest_create'),
	path('friend_requests/', views.ListRequest.as_view(), name='friend_requests'),
	path('friendrequest_detail/<int:pk>', views.RequestDetail.as_view(), name='friendrequest_detail'),
	path('friendrequest_accept/<int:pk>', views.FriendrequestAccept.as_view(), name='friendrequest_accept'),
	path('decline_request/<int:pk>', views.DeclineRequest.as_view(), name='decline_request'),

	path('list/', views.Friendrequests.as_view(), name='list'),
]