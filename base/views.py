from .forms import TrainingForm
from django.views.generic.edit import FormView


class TrainingView(FormView):
	template_name = "base/training.html"
	form_class = TrainingForm