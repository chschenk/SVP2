from celery.result import AsyncResult
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View
from .tasks import read_result
from .forms import TrainingForm
from .models import Sequence


class TrainingView(FormView):
	template_name = "base/training.html"
	form_class = TrainingForm
	task_id = None
	paginate_by = 10

	def get_success_url(self):
		return reverse('base:readResult', kwargs={'task_id': self.task_id})

	def form_valid(self, form):
		print(form.cleaned_data)
		profile_pk = form.cleaned_data['Profile'].pk
		member_pk = form.cleaned_data['Member'].pk
		self.task_id = read_result.delay(profile_pk, member_pk)
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		ctx = super(TrainingView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		sequences = Sequence.objects.filter(date__date=datetime.now().date()).order_by('date')
		paginator = Paginator(sequences, self.paginate_by)
		try:
			page_obj = paginator.page(page)
		except:
			page_obj = paginator.page(paginator.num_pages)
		ctx['page_obj'] = page_obj
		return ctx


class ReadTrainingResult(TemplateView):
	template_name = "base/read_result.html"

	def get_context_data(self, **kwargs):
		ctx = super(ReadTrainingResult, self).get_context_data(**kwargs)
		ctx['task_id'] = kwargs['task_id']
		return ctx


class TaskStatusView(View):

	def get(self, request, task_id):
		result = AsyncResult(task_id)
		response_data = {
			'state': result.state,
			'details': result.info,
		}
		return JsonResponse(response_data)
