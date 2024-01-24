from django.shortcuts import render
from django.views import View

class HomeView(View):
	"""
		Home page view.
	"""
	def get(self, request, *args, **kwargs):
		return render(request, 'home.html')


class AboutView(View):
	"""
		About us page.
	"""
	def get(self, request, *args, **kwargs):
		return render(request, 'page/about-us.html')


class ContactView(View):
	"""
		Contact us page.
	"""
	def get(self, request, *args, **kwargs):
		return render(request, 'page/contact-us.html')