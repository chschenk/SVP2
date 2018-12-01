from django.db.models import Model, ForeignKey, CharField, DateField, ManyToManyField, PositiveIntegerField, BooleanField, CASCADE, SET_NULL
from member.models import Member
from base.models import Sequence


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


class Group(Model):
	name = CharField(max_length=30)
	members = ManyToManyField(Member)
	competition = ForeignKey(Competition, on_delete=CASCADE)


class GroupPrice(Model):
	name = CharField(max_length=30)
	competition = ForeignKey(Competition, on_delete=CASCADE)
	winner = ForeignKey(Group, null=True, on_delete=SET_NULL)


class PriceRecord(Model):
	recordId = PositiveIntegerField()
	abandoned = BooleanField(default=False)
	member = ForeignKey(Member, on_delete=CASCADE)
	sequence = ForeignKey(Sequence, on_delete=CASCADE, null=True)
	price = ForeignKey(Price, on_delete=CASCADE)


class Weapon(Model):
	name = CharField(max_length=30)
	current_record = ForeignKey(PriceRecord, null=True, on_delete=SET_NULL)
