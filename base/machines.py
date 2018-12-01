from random import random, randint
from time import sleep
from multiprocessing import Process
from serial import Serial, PARITY_NONE, STOPBITS_ONE
from SVP2.settings import SVP_DISAG_SERIAL_PORT


class EvaluationMachine:

	def read_result(self, profile):
		raise NotImplementedError()


ACK = 0x06
ENQ = 0x05
STX = 0x02
CR = 0x0D


class DisagRMMachine(EvaluationMachine):

	timeout = 30
	_serial = None

	def read_result(self, profile):
		if hasattr(profile, "disagprofile"):
			profile = getattr(profile, "disagprofile")
		else:
			raise AttributeError("Profile not compatible with this machine")
		proc = Process(target=self._read_result, args=(profile.get_profile(),))
		proc.start()
		proc.join(timeout=self.timeout)
		if proc.exitcode is None:
			proc.terminate()
			return False

	def _read_reply(self):
		checksum = 0
		reply = self._serial.read_until(terminator=CR)
		for c in reply:
			checksum = checksum ^ ord(c)
		if checksum < 32:
			checksum += 32
		if checksum != reply[-1]:
			raise Exception("Error reading: Invalid checksum")
		self._serial.write(ACK)
		return reply

	def _get_result_from_reply(self, reply):
		values = reply.encode('ASCII').split(';')
		shot = dict()
		shot['ShotNumber'] = int(values.split('=')[1])
		shot['Rings'] = float(values[1])
		shot['FactorValue'] = float(values[2])
		shot['Angle'] = float(values[3])
		shot['Validity'] = values[4] == "G"
		return shot

	def _get_profile_string(self, profile):
		checksum = 0
		for c in profile:
			checksum = checksum ^ ord(c)
		return profile + chr(checksum) + CR

	def _read_result(self, profile):
		result = list()
		try:
			self._serial = Serial(port=SVP_DISAG_SERIAL_PORT, baudrate=38400, parity=PARITY_NONE, stopbits=STOPBITS_ONE)
			self._serial.write(ENQ)
			read = 0
			while read != STX:
				read = self._serial.read(1)
				self._serial.write(self._get_profile_string(profile))
			retries = 0
			read = 0
			while read != ACK and retries < 3:
				read = self._serial.read(1)
				retries = retries + 1
			if retries == 3:
				raise Exception("Machine does not accept profile")
			reply = ""
			while reply != "WSE":
				reply = self._read_reply()
				if reply.startsWith("SCH"):
					result.append(self._get_result_from_reply(reply))
			self._result_read = result
			self._successful = True
			return
		except:
			self._serial.close()
			self._result_read = result
			self._successful = False
			return


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
