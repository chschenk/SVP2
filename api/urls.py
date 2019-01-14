from django.urls import path
from .views import ReleaseWeapon

app_name = "api"
urlpatterns = [
	path('release_weapon/<int:pk>', ReleaseWeapon.as_view(), name='release-weapon'),
]



