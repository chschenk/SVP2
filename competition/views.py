from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView, RedirectView
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Max
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy, gettext
from django.core.paginator import Paginator
from django.utils import timezone
from base.models import Sequence, Member
from .models import Competition, Price, Award, GroupPrice, Weapon, CompetitionRecord
from .forms import MemberForm


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


class CompetitionUpdateView(SuccessMessageMixin, UpdateView):
	model = Competition
	success_message = gettext_lazy("Competition successfully updated!")
	success_url = ""
	fields = ['name']

	def get_context_data(self, **kwargs):
		ctx = super(CompetitionUpdateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Edit competition")
		ctx['mode'] = "edit"
		return ctx


class PriceCreateView(SuccessMessageMixin, CreateView):
	model = Price
	success_message = gettext_lazy("Price successfully created")
	fields = ['name']

	def form_valid(self, form):
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


class WeaponListView(ListView):
	model = Weapon
	paginate_by = 10
	queryset = Weapon.objects.all().order_by("name")


class WeaponCreateView(SuccessMessageMixin, CreateView):
	model = Weapon
	fields = ['name']
	success_url = reverse_lazy("competition:list-weapon")
	success_message = gettext_lazy("Weapon successfully created")

	def get_context_data(self, **kwargs):
		ctx = super(WeaponCreateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Add weapon")
		return ctx


class WeaponDeleteView(SuccessMessageMixin, DeleteView):
	model = Weapon
	success_url = reverse_lazy("competition:list-weapon")
	success_message = gettext_lazy("Weapon successfully deleted")

	def get_context_data(self, **kwargs):
		ctx = super(WeaponDeleteView, self).get_context_data(**kwargs)
		ctx['cancel_url'] = self.success_url
		return ctx


class WeaponUpdateView(SuccessMessageMixin, UpdateView):
	model = Weapon
	fields = ['name']
	success_url = reverse_lazy("competition:list-weapon")
	success_message = gettext_lazy("Weapon successfully updated")

	def get_context_data(self, **kwargs):
		ctx = super(WeaponUpdateView, self).get_context_data(**kwargs)
		ctx['title'] = gettext("Edit weapon")
		return ctx


class CompetitionPerformView(FormView):
	template_name = "competition/perform.html"
	task_id = None
	paginate_by = 10
	form_class = MemberForm

	def get_success_url(self):
		return reverse('competition:perform-competition', kwargs={'pk': self.kwargs['pk']})

	def form_valid(self, form):
		competition = Competition.objects.get(pk=self.kwargs['pk'])
		weapon = form.cleaned_data['Weapon']
		member = form.cleaned_data['Member']
		try:
			competition_record = CompetitionRecord.objects.get(competition=competition, member=member)
		except CompetitionRecord.DoesNotExist:
			competition_record = None
		if competition_record is None:
			competition_record = CompetitionRecord()
			competition_record.competition = competition
			competition_record.member = member
			record_number = 0
			if CompetitionRecord.objects.filter(competition=competition).count() > 0:
				record_number = CompetitionRecord.objects.filter(competition=competition).aggregate(Max('record_number'))['record_number__max']
			competition_record.record_number = record_number + 1
			competition_record.save()
		weapon.current_record = competition_record
		weapon.save()
		return super(CompetitionPerformView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		ctx = super(CompetitionPerformView, self).get_context_data(**kwargs)
		weapons = list()
		for w in Weapon.objects.all():
			weapon = dict()
			weapon['name'] = w.name
			weapon['id'] = w.pk
			weapon['form'] = MemberForm(initial={'Weapon': w})
			weapon['current_record'] = w.current_record
			weapons.append(weapon)
		ctx['weapons'] = weapons
		ctx['competition'] = Competition.objects.get(pk=self.kwargs['pk'])
		page = self.request.GET.get('page')
		sequences = Sequence.objects.filter(date__date=timezone.now().date()).order_by('date')
		paginator = Paginator(sequences, self.paginate_by)
		try:
			page_obj = paginator.page(page)
		except:
			page_obj = paginator.page(paginator.num_pages)
		ctx['page_obj'] = page_obj
		return ctx


class ReleaseWeaponView(RedirectView):

	def get(self, request, *args, **kwargs):
		weapon = Weapon.objects.get(pk=self.kwargs['weapon_pk'])
		weapon.current_record = None
		weapon.save()
		return super(ReleaseWeaponView, self).get(request, *args, **kwargs)

	def get_redirect_url(self, *args, **kwargs):
		print(self.kwargs['pk'])
		return reverse('competition:perform-competition', self.kwargs['pk'])
