from dal.autocomplete import Select2QuerySetView, Select2GroupListView
from datetime import datetime
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms.widgets import SelectDateWidget
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy, gettext
from .models import Club, Member


class ClubCreateView(SuccessMessageMixin, CreateView):
	model = Club
	fields = ['name']
	success_message = gettext_lazy("Club successfully created")
	success_url = reverse_lazy('member:list-club')

	def get_context_data(self, **kwargs):
		kwargs['title'] = gettext("Create club")
		return super(ClubCreateView, self).get_context_data(**kwargs)


class ClubListView(ListView):
	model = Club
	paginate_by = 10


class ClubDeleteView(SuccessMessageMixin, DeleteView):
	model = Club
	success_url = reverse_lazy("member:list-club")
	success_message = gettext_lazy("Club successfully deleted")

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		super(ClubDeleteView, self).delete(request, *args, **kwargs)


class ClubDetailView(DetailView):
	model = Club
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(ClubDetailView, self).get_context_data()
		page = self.request.GET.get('page')
		members = self.object.member_set.all()
		paginator = Paginator(members, self.paginate_by)
		try:
			page_obj = paginator.page(page)
		except:
			page_obj = paginator.page(1)
		context['page_obj'] = page_obj
		return context


class ClubUpdateView(SuccessMessageMixin, UpdateView):
	model = Club
	fields = ['name']
	success_url = reverse_lazy("member:list-club")
	success_message = gettext_lazy("Club successfully updated")

	def get_context_data(self, **kwargs):
		kwargs['title'] = gettext("Edit club")
		return super(ClubUpdateView, self).get_context_data(**kwargs)


class ClubAutocompleteView(Select2QuerySetView):

	def get_queryset(self):
		qs = Club.objects.all()
		if self.q:
			qs = qs.filter(name__istartswith=self.q)
		return qs.order_by('name')


class MemberCreateView(SuccessMessageMixin, CreateView):
	model = Member
	fields = ['club', 'first_name', 'last_name', 'nick_name', 'birthday']
	success_message = gettext_lazy("Member successfully created")
	success_url = reverse_lazy('member:list-club')

	def get_initial(self):
		club_pk = self.kwargs.get('club_pk', None)
		if club_pk is not None:
			return {'club': club_pk}
		return {}

	def get_context_data(self, **kwargs):
		kwargs['title'] = gettext("Create member")
		return super(MemberCreateView, self).get_context_data(**kwargs)

	def get_form(self, form_class=None):
		form = super(MemberCreateView, self).get_form()
		years = range(datetime.now().year - 100, datetime.now().year)
		form.fields['birthday'].widget = SelectDateWidget(years=list(years))
		return form


class MemberDetailView(DetailView):
	model = Member


class MemberUpdateView(SuccessMessageMixin, UpdateView):
	model = Member
	fields = ['club', 'first_name', 'last_name', 'nick_name', 'birthday']
	success_message = gettext_lazy("Member successfully updated")
	success_url = reverse_lazy('member:list-club')

	def get_context_data(self, **kwargs):
		kwargs['title'] = gettext("Edit member")
		return super(MemberUpdateView, self).get_context_data(**kwargs)

	def get_form(self, form_class=None):
		form = super(MemberUpdateView, self).get_form()
		years = range(datetime.now().year - 100, datetime.now().year)
		form.fields['birthday'].widget = SelectDateWidget(years=list(years))
		return form


class MemberDeleteView(DeleteView):
	model = Member
	success_url = reverse_lazy("member:list-club")
	success_message = gettext_lazy("Member successfully deleted")

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, self.success_message)
		return super(MemberDeleteView, self).delete(request, *args, **kwargs)


class MemberAutocompleteView(Select2QuerySetView):

	def get_queryset(self):
		qs = Member.objects.all()

		club = self.forwarded.get('Club', None)
		if club:
			qs = Member.objects.filter(club=club)
		if self.q:
			qs = qs.filter(Q(first_name__icontains=self.q) | Q(last_name__icontains=self.q))
		return qs.order_by('first_name', 'last_name')
