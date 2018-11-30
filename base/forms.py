from dal import autocomplete
from django.forms.forms import Form
from django.forms import ModelChoiceField
from member.models import Member, Club
from .models import Profile

class TrainingForm(Form):
	Profile = ModelChoiceField(queryset=Profile.objects.all())
	Club = ModelChoiceField(queryset=Club.objects.all(),
							widget=autocomplete.ModelSelect2(url="member:autocomplete-club"), required=False)
	Member = ModelChoiceField(queryset=Member.objects.all(),
							  widget=autocomplete.ModelSelect2(url="member:autocomplete-member", forward=['Club']))
