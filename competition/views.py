from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy, gettext
from .models import Competition, Price, Award, GroupPrice


class CompetitionListView(ListView):
	model = Competition
	paginate_by = 10
	queryset = Competition.objects.all().order_by('start_date')


class CompetitionDeleteView(SuccessMessageMixin, DeleteView):
	model = Competition
	success_url = reverse_lazy("competition:list-competition")
	success_message = gettext_lazy("Competition successfully deleted!")

	def get_context_data(self, **kwargs):
		ctx = super(CompetitionDeleteView, self).get_context_data(**kwargs)
		ctx['cancel_url'] = reverse('competition:list-competition')
		return ctx


class CompetitionCreateView(SuccessMessageMixin, CreateView):
	model = Competition
	success_message = gettext_lazy("Competition successfully created!")
	fields = ['name']

	def form_valid(self, form):
		form.instance.save()
		self.success_url = reverse(form.data['redirect'], args=[form.instance.pk])
		return super(CompetitionCreateView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		ctx = super(CompetitionCreateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Add competition")
		ctx['mode'] = "create"
		return ctx


class PriceCreateView(SuccessMessageMixin, CreateView):
	model = Price
	success_message = gettext_lazy("Price successfully created")
	fields = ['name']

	def form_valid(self, form):
		print(self.kwargs.get("competition_pk"))
		competition = Competition.objects.get(pk=self.kwargs.get("competition_pk"))
		form.instance.competition = competition
		self.success_url = reverse(form.data['redirect'], args=[competition.pk])
		return super(PriceCreateView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		ctx = super(PriceCreateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Add price")
		ctx['mode'] = "create"
		return ctx


class GroupPriceCreateView(SuccessMessageMixin, CreateView):
	model = GroupPrice
	success_message = gettext_lazy("Group price successfully created")
	fields = ['name']

	def form_valid(self, form):
		print(self.kwargs.get("competition_pk"))
		competition = Competition.objects.get(pk=self.kwargs.get("competition_pk"))
		form.instance.competition = competition
		self.success_url = reverse(form.data['redirect'], args=[competition.pk])
		return super(GroupPriceCreateView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		ctx = super(GroupPriceCreateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Add group price")
		ctx['mode'] = "create"
		return ctx


class AwardCreateView(SuccessMessageMixin, CreateView):
	model = Award
	success_message = gettext_lazy("Award successfully created")
	fields = ['name']

	def form_valid(self, form):
		print(self.kwargs.get("competition_pk"))
		competition = Competition.objects.get(pk=self.kwargs.get("competition_pk"))
		form.instance.competition = competition
		self.success_url = reverse(form.data['redirect'], args=[competition.pk])
		return super(AwardCreateView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		ctx = super(AwardCreateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Add award")
		ctx['mode'] = "create"
		return ctx


class CompetitionDetailView(DetailView):
	model = Competition
