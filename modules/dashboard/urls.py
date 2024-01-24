from django.urls import path
from modules.dashboard import views


app_name = 'dashboard'

urlpatterns = [
	path('', views.HomeView.as_view(), name='home'),
	path('about_us/', views.AboutView.as_view(), name='about_us'),
	path('contact_us/', views.ContactView.as_view(), name='contact_us'),
]