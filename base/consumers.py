from channels.generic.websocket import WebsocketConsumer
from django.utils.translation import gettext
from json import loads as json_loads
from json import dumps as json_dumps

class ReadResultConsumer(WebsocketConsumer):
	def connect(self):
		self.accept()

	def disconnect(self, close_code):
		pass

	def receive(self, text_data):
		data = json_loads(text_data)
		print("Member: {}".format(data['member']))
		print("Profile: {}".format(data['profile']))
		print("Recieved something: {}\n".format(text_data))

		#Do read result

		data = dict()
		data['success'] = True
		data['message'] = gettext("Successfully read result")
		self.send(text_data=json_dumps(data))