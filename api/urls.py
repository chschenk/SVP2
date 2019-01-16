from django.urls import path
from .views import ReleaseWeapon, MonitorQueueElementView

app_name = "api"
urlpatterns = [
	path('release_weapon/<int:pk>', ReleaseWeapon.as_view(), name='release-weapon'),
	path('monitor/queue', MonitorQueueElementView.as_view(), name='monitor-queue'),
]



