from django.db.models import Model, CharField, DateField, ForeignKey, CASCADE

class Club(Model):
	name = CharField(max_length=30)

	def __str__(self):
		return self.name

class Member(Model):
	first_name = CharField(max_length=30)
	last_name = CharField(max_length=30)
	nick_name = CharField(max_length=10)
	birthday = DateField(null=True)
	club = ForeignKey(Club, on_delete=CASCADE)

	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)

