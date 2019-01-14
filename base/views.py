from celery.result import AsyncResult
from django.http import JsonResponse
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy, gettext
from .tasks import read_result
from .forms import TrainingForm
from .models import Sequence, Profile
from . import models


class TrainingView(FormView):
	template_name = "base/training.html"
	form_class = TrainingForm
	paginate_by = 10

	def get_success_url(self):
		return self.success_url

	def form_valid(self, form):
		profile_pk = form.cleaned_data['Profile'].pk
		member_pk = form.cleaned_data['Member'].pk
		profile = Profile.objects.select_subclasses().get(pk=profile_pk)
		if profile.is_manual_profile():
			self.success_url = reverse('base:training')
			#ToDo add manual form
		else:
			task_id = read_result.delay(profile_pk, member_pk)
			self.success_url = reverse('base:readResult', kwargs={'task_id': task_id})
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
			'state': str(result.state),
			'details': str(result.info),
		}
		return JsonResponse(response_data)


class ProfileListView(ListView):
	model = Profile
	paginate_by = 10

	def get_queryset(self):
		return Profile.objects.all().order_by('name').select_subclasses()

	def get_context_data(self, *args, object_list=None, **kwargs):
		ctx = super(ProfileListView, self).get_context_data(*args, object_list=object_list, **kwargs)
		ctx['profile_list'] = [{'name': c.__name__, 'label': gettext("Add {}".format(c.type_name))}for c in Profile.__subclasses__()]
		return ctx


class ProfileDeleteView(SuccessMessageMixin, DeleteView):
	model = Profile
	success_message = gettext_lazy("Profile successfully deleted")
	success_url = reverse_lazy('base:list-profile')

	def get_context_data(self, **kwargs):
		ctx = super(ProfileDeleteView, self).get_context_data(**kwargs)
		ctx['cancel_url'] = reverse('base:list-profile')
		return ctx


class ProfileCreateView(SuccessMessageMixin, CreateView):
	model = Profile
	fields = '__all__'
	template_name = "base/profile_form.html"
	success_message = gettext_lazy("Profile successfully created")
	success_url = reverse_lazy('base:list-profile')

	def get_context_data(self, **kwargs):
		ctx = super(ProfileCreateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Add {}".format(self.model.type_name))
		return ctx


class ProfileUpdateView(SuccessMessageMixin, UpdateView):
	model = Profile
	fields = '__all__'
	template_name = "base/profile_form.html"
	success_message = gettext_lazy("Profile successfully updated")
	success_url = reverse_lazy('base:list-profile')

	def get_context_data(self, **kwargs):
		ctx = super(ProfileUpdateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Edit {}".format(self.model.type_name))
		return ctx


def get_create_profile_view(*args, **kwargs):
	if hasattr(models, kwargs['profile_name']):
		ProfileCreateView.model = getattr(models, kwargs['profile_name'])
	else:
		raise ValueError("Could not find profile class {}".format(kwargs['profile_name']))
	view = ProfileCreateView.as_view()
	return view(*args, **kwargs)


def get_update_profile_view(*args, **kwargs):
	if hasattr(models, kwargs['profile_name']):
		ProfileUpdateView.model = getattr(models, kwargs['profile_name'])
	else:
		raise ValueError("Could not find profile class {}".format(kwargs['profile_name']))
	view = ProfileUpdateView.as_view()
	return view(*args, **kwargs)
