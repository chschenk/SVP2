from django.urls import path
from .views import TrainingView

app_name = "base"
urlpatterns = [
	path('', TrainingView.as_view(), name="training"),
]
