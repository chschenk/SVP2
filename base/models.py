from django.db.models import Model, CharField, ForeignKey, DateTimeField, DecimalField, PositiveIntegerField
from django.db.models import BooleanField, CASCADE, SET_NULL
from django.utils.translation import gettext_lazy
from django.forms import Form
from model_utils.managers import InheritanceManager
from member.models import Member


class Profile(Model):
	name = CharField(max_length=30)
	manual_profile = None
	type_name = None
	extra_form = None
	objects = InheritanceManager()

	def get_type(self):
		return None

	def is_manual_profile(self):
		return False

	def __str__(self):
		return self.name


class DisagProfile(Profile):
	type_name = gettext_lazy("DISAG Profile")
	manual_profile = False
	sch_choices = (
		("LG10", "LG 10er-Band"),
		("LG5", "LG 5er-Band"),
		("LGES", "LG Einzelscheibe"),
		("LP", "LP"),
		("ZS", "Zimmerstutzen 15m"),
		("LS1", "Laufende Scheibe; ein Spiegel"),
		("LS2", "Laufende Scheibe; doppel Spiegel"),
		("KK5", "50m Scheibe"),
		("GK10", "100m - Scheibe für Groß und Kleinkaliber"),
		("GK5", "Kombischeibe 5-kreisig mit weißem Scheibenspiegel"),
		("LPSF", "LP Schnellfeuer"),
		("SCHFE", "Schnellfeuer- und Duell Scheibe."),
		("USE1", "Benutzerdefiniert 1"),
		("USE2", "Benutzerdefiniert 2"),
	)
	ria_choices = (
		("GR", "Ganze Ringe"),
		("ZR", "Zehntel Ringe"),
		("KR", "Keine Ringe"),
	)
	kal_choices = (
		("22", "22"),
		("6MM", "6MM"),
		("6.5MM", "6.5MM"),
		("7MM", "7MM"),
		("30", "30"),
		("303", "303"),
		("8MM", "8MM"),
		("32", "32"),
		("33", "33"),
		("9MM", "9MM"),
		("357", "357"),
		("36", "36"),
		("38", "38"),
		("40", "40"),
		("44", "44"),
		("45", "45"),
		("50", "50"),
		("52", "52"),
		("54", "54"),
		("58", "58"),
	)
	rib_choices = (
		("RB", "Ringberührungsmethode"),
		("MI", "Schußlochmittelpunkt für Vorderlader."),
	)
	tea_choices = (
		("KT", "Keine Teilerwertung"),
		("ZT", "Teilerwertung mit zehntel Teiler"),
		("HT", "Teilerwertung mit hundertstel Teiler"),
	)
	sch = CharField(max_length=5, null=False, choices=sch_choices, verbose_name="Scheibentype")
	ria = CharField(max_length=2, null=False, choices=ria_choices, verbose_name="Ringauswertung")
	kal = CharField(max_length=5, null=True, choices=kal_choices, verbose_name="Kalibereinstellung", blank=True)
	rib = CharField(max_length=2, null=False, choices=rib_choices, verbose_name="Ringberechnung")
	tea = CharField(max_length=2, null=False, choices=tea_choices, verbose_name="Teilerauswertung")
	teg = PositiveIntegerField(null=True, verbose_name="Teilergrenze", blank=True)
	ssc = PositiveIntegerField(null=True, verbose_name="Schußzahl pro Scheibe", blank=True)
	seg = PositiveIntegerField(null=True, verbose_name="Schußzahl Gesamt", blank=True)
	szi = PositiveIntegerField(null=True, verbose_name="Schußzahl pro Zwischensumme", blank=True)
	ksd = BooleanField(default=False, verbose_name="Kein Scheibenaufdruck")
	tem = BooleanField(default=False, verbose_name="Teiler auf der Scheibe nur markieren")

	def get_profile(self, drt=None):
		config = list()
		config.append("SCH={}".format(self.sch))
		config.append("RIA={}".format(self.ria))
		if self.kal is not None:
			config.append("KAL={}".format(self.kal))
		config.append("RIB={}".format(self.rib))
		config.append("TEA={}".format(self.tea))
		if self.teg is not None:
			config.append("TEG={}".format(self.teg))
		if self.ssc is not None:
			config.append("SSC={}".format(self.ssc))
		if self.seg is not None:
			config.append("SEG={}".format(self.seg))
		if self.szi is not None:
			config.append("SZI={}".format(self.szi))
		if self.ksd:
			config.append("KSD")
		if self.tem is not None:
			config.append("TEM")
		if drt:
			config.append("DRT={}".format(drt))
		return ";".join(config)

	def get_type(self):
		return self.__class__.__name__


class FunProfileForm(Form):

	def __init__(self, profile):
		for i in range(1, profile + 1):
			self.fields.append(PositiveIntegerField(verbose_name="Schuss {}".format(i)))


class FunProfile(Profile):
	type_name = gettext_lazy("Fun card profile")
	seg = PositiveIntegerField(null=True, verbose_name="Schußzahl Gesamt")
	manual_profile = True
	extra_form = FunProfileForm

	def get_profile(self):
		return self.seg

	def get_type(self):
		return self.__class__.__name__

	def is_manual_profile(self):
		return True


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
