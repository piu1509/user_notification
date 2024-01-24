from django.urls import path
from modules.notifications import views

app_name = 'notificaions'

urlpatterns = [
	path('notification_create/', views.NotificationCreate.as_view(), name='notification_create'),
	path('notification_list/', views.NotificationList.as_view(), name='notification_list'),
	path('notification_detail/<int:pk>', views.NotificationDetail.as_view(), name='notification_detail'),
	path('unread_notification_count/', views.UnreadNotificationCount.as_view(), name='unread_notification_count'),
]