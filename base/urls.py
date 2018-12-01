from django.urls import path
from .views import TrainingView, ReadTrainingResult, TaskStatusView, ProfileListView, ProfileDeleteView
from .views import get_create_profile_view, get_update_profile_view

app_name = "base"
urlpatterns = [
	path('', TrainingView.as_view(), name="training"),
	path('readResult/<task_id>', ReadTrainingResult.as_view(), name="readResult"),
	path('getTaskStatus/<task_id>', TaskStatusView.as_view(), name="getTaskStatus"),
	path('profile/', ProfileListView.as_view(), name="list-profile"),
	path('profile/create/<profile_name>', get_create_profile_view, name="create-profile"),
	path('profile/edit/<profile_name>/<int:pk>', get_update_profile_view, name="edit-profile"),
	path('profile/delete/<int:pk>', ProfileDeleteView.as_view(), name="delete-profile"),
]
