from django.db.models import Model, CharField, ForeignKey, DateTimeField, DecimalField, PositiveIntegerField, BooleanField, CASCADE, SET_NULL
from member.models import Member


class Profile(Model):
	name = CharField(max_length=30)
	config = CharField(max_length=128)

	def __str__(self):
		return self.name


class Sequence(Model):
	member = ForeignKey(Member, on_delete=CASCADE)
	next_sequence = ForeignKey('self', null=True, on_delete=SET_NULL)
	date = DateTimeField()
	profile = ForeignKey(Profile, on_delete=CASCADE)

	def sum(self):
		result = 0
		for shot in self.shot_set.all():
			if shot.valid:
				result = result + shot.value
		return result


class Shot(Model):
	value = DecimalField(max_digits=6, decimal_places=3)
	number = PositiveIntegerField()
	factor_value = DecimalField(max_digits=6, decimal_places=3)
	angle = DecimalField(max_digits=6, decimal_places=3)
	valid = BooleanField()
	sequence = ForeignKey(Sequence, on_delete=CASCADE)
