from django.views.generic import CreateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy
from .models import Competition, Price, Award

class CompetitionCreateView(SuccessMessageMixin, CreateView):
	model = Competition
	success_message = gettext_lazy("Competition successfully created!")
	fields = ['name']

class PriceCreateView(SuccessMessageMixin, CreateView):
	model = Price
	success_message = gettext_lazy("Price successfully created")
	fields = ['name']

class AwardCreateView(SuccessMessageMixin, CreateView):
	model = Award
	success_message = gettext_lazy("Award successfully created")
	fields = ['name']

class CompetitionDetailView(DetailView):
	model = Competition