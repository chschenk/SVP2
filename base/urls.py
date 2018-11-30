from django.urls import path
from .views import TrainingView, ReadTrainingResult, TaskStatusView

app_name = "base"
urlpatterns = [
	path('', TrainingView.as_view(), name="training"),
	path('readResult/<task_id>', ReadTrainingResult.as_view(), name="readResult"),
	path('getTaskStatus/<task_id>', TaskStatusView.as_view(), name="getTaskStatus")
]
