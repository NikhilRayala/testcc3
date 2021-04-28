from django.urls import path
from . import views

urlpatterns = [
	path(r'api/posts/', views.posts, name="posts"),
    path(r'api/ping/', views.ping, name="ping")

]
