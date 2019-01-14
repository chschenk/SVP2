from django.utils import timezone
from SVP2.settings import SVP_MACHINE
from .machines import EvaluationMachine
from .models import Member, Profile, Sequence, Shot
from SVP2.celery import app


@app.task(max_retries=1, time_limit=60)
def read_result(profile_pk, member_pk):
	machine = None
	member = Member.objects.get(pk=member_pk)
	profile = Profile.objects.select_subclasses().get(pk=profile_pk)
	for cls in EvaluationMachine.__subclasses__():
		if cls.__name__ == SVP_MACHINE:
			machine = cls()
	if machine is None:
		raise Exception("Wrong configured setting SVP_MACHINE: Could not find evaluation machine {}!".format(SVP_MACHINE))
	result = machine.read_result(profile)
	seq = Sequence()
	seq.profile = profile
	seq.date = timezone.now()
	seq.member = member
	seq.save()
	for s in result:
		shot = Shot()
		shot.angle = s['Angle']
		shot.factor_value = s['FactorValue']
		shot.number = s['ShotNumber']
		shot.value = s['Rings']
		shot.valid = s['Validity']
		shot.sequence = seq
		shot.save()
	return True
