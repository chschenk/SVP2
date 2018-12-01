from random import random, randint
from time import sleep


class EvaluationMachine:

	def read_result(self, profile):
		raise NotImplementedError()


class DisagRMMachine(EvaluationMachine):

	def read_result(self, profile):
		if self.__name__ not in profile.machines:
			raise ValueError("Profile not compatible with this machine")
		return list()


class DisagRMTestMachine(EvaluationMachine):

	def read_result(self, profile):
		if hasattr(profile, "disagprofile"):
			profile = getattr(profile, "disagprofile")
		else:
			raise AttributeError("Profile not compatible with this machine")
		result = list()
		for i in range(1, profile.seg + 1):
			shot = dict()
			shot['ShotNumber'] = i
			shot['Rings'] = randint(0, 10)
			shot['FactorValue'] = randint(0, 500)
			shot['Angle'] = random() * 360
			shot['Validity'] = True

			sleep(2)

			result.append(shot)
		return result
