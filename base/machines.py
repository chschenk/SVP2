from random import random, randint
from time import sleep


class EvaluationMachine:

	def read_result(self):
		raise NotImplementedError()


class DisagRMMachine(EvaluationMachine):

	def read_result(self, profile=""):
		if len(profile) == 0:
			raise ValueError("Profile string may not be empty")
		return list()


class DisagRMTestMachine(EvaluationMachine):

	def read_result(self, profile=""):
		result = list()
		for i in range(1, 11):
			shot = dict()
			shot['ShotNumber'] = i
			shot['Rings'] = randint(0, 10)
			shot['FactorValue'] = randint(0, 500)
			shot['Angle'] = random() * 360
			shot['Validity'] = True

			sleep(2)

			result.append(shot)
		return result
