from django.db.models import Model, ForeignKey, CharField, DateField, ManyToManyField, PositiveIntegerField, BooleanField, CASCADE, SET_NULL, PROTECT
from member.models import Member
from base.models import Sequence, Profile


class Competition(Model):
	name = CharField(max_length=30)
	start_date = DateField(auto_now=True)
	end_date = DateField(null=True)

	def __str__(self):
		return self.name


class Award(Model):
	name = CharField(max_length=30)
	competition = ForeignKey(Competition, on_delete=CASCADE)
	winner = ForeignKey(Member, null=True, on_delete=SET_NULL)


class Price(Model):
	name = CharField(max_length=30)
	competition = ForeignKey(Competition, on_delete=CASCADE)
	winner = ForeignKey(Member, null=True, on_delete=SET_NULL)
	profile = ForeignKey(Profile, null=False, on_delete=PROTECT)

	def __str__(self):
		return self.name


class Group(Model):
	name = CharField(max_length=30)
	members = ManyToManyField(Member)
	competition = ForeignKey(Competition, on_delete=CASCADE)


class GroupPrice(Model):
	name = CharField(max_length=30)
	competition = ForeignKey(Competition, on_delete=CASCADE)
	winner = ForeignKey(Group, null=True, on_delete=SET_NULL)


class CompetitionRecord(Model):
	competition = ForeignKey(Competition, on_delete=CASCADE)
	record_number = PositiveIntegerField()
	member = ForeignKey(Member, on_delete=CASCADE)


class PriceRecord(Model):
	competition_record = ForeignKey(CompetitionRecord, on_delete=CASCADE)
	abandoned = BooleanField(default=False)
	sequence = ForeignKey(Sequence, on_delete=CASCADE, null=True)
	price = ForeignKey(Price, on_delete=CASCADE)


class Weapon(Model):
	name = CharField(max_length=30)
	current_record = ForeignKey(CompetitionRecord, null=True, on_delete=SET_NULL)

	def __str__(self):
		return self.name
