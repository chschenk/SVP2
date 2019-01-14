from dal import autocomplete
from django.forms import Form, HiddenInput
from django.forms import ModelChoiceField
from member.models import Member, Club
from .models import Weapon


class MemberForm(Form):
	Club = ModelChoiceField(queryset=Club.objects.all().order_by('name'),
							widget=autocomplete.ModelSelect2(url="member:autocomplete-club"), required=False)
	Member = ModelChoiceField(queryset=Member.objects.all().order_by('first_name', 'last_name'),
							  widget=autocomplete.ModelSelect2(url="member:autocomplete-member", forward=['Club']))
	Weapon = ModelChoiceField(queryset=Weapon.objects.all(), widget=HiddenInput)