from . import views
from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie

urlpatterns = [
	url(r'^$', views.index, name='index'),
	# url(r'^find$', ensure_csrf_cookie(views.find), name='find'),
	url(r'^find$', views.find, name='find'),
]

