from django.urls import path
from .consumers import ReadResultConsumer

websocket_urlpatterns = [
	path('ws/read/', ReadResultConsumer)
]