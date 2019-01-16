from django.utils import timezone
from SVP2.settings import SVP_MACHINE
from base.machines import EvaluationMachine
from base.models import Member, Profile, Sequence, Shot
from .models import CompetitionRecord, PriceRecord, Price, Weapon
from SVP2.celery import app


@app.task(max_retries=1, time_limit=60)
def read_competition_result(price_pk, weapon_pk):
	machine = None
	weapon = Weapon.objects.get(pk=weapon_pk)
	competition_record = CompetitionRecord.objects.get(pk=weapon.current_record.pk)
	price = Price.objects.get(pk=price_pk)
	profile = Profile.objects.select_subclasses().get(pk=price.profile.pk)
	price_record = PriceRecord()
	for cls in EvaluationMachine.__subclasses__():
		if cls.__name__ == SVP_MACHINE:
			machine = cls()
	if machine is None:
		raise Exception("Wrong configured setting SVP_MACHINE: Could not find evaluation machine {}!".format(SVP_MACHINE))
	result = machine.read_result(profile)
	price_record.competition_record = competition_record
	price_record.price = price

	seq = Sequence()
	seq.profile = profile
	seq.date = timezone.now()
	seq.member = competition_record.member
	seq.save()
	price_record.sequence = seq
	price_record.save()
	for s in result:
		shot = Shot()
		shot.angle = s['Angle']
		shot.factor_value = s['FactorValue']
		shot.number = s['ShotNumber']
		shot.value = s['Rings']
		shot.valid = s['Validity']
		shot.sequence = seq
		shot.save()
	weapon.current_record = None
	weapon.save()
	return True
