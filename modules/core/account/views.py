from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView


class Login(LoginView):
	"""
	Handles the login process.
	"""
	template_name = 'account/registration/login.html'


class Logout(LogoutView):
	"""
	Handles the logout process.
	"""
	template_name = 'account/registration/logout.html'