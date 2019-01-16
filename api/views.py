from django.shortcuts import render
from django.http import HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from competition.models import Weapon
from base.models import MonitorQueueElement, Shot, Sequence
from member.models import Member, Club


class ReleaseWeapon(APIView):

	def get(self, request, pk):
		weapon = Weapon.objects.get(pk=pk)
		weapon.current_record = None
		weapon.save()
		return Response({"message": "Successfully released weapon"})


class ClubSerializer(ModelSerializer):
	class Meta:
		model = Club
		fields = ['name']


class MemberSerializer(ModelSerializer):
	club = ClubSerializer(read_only=True)

	class Meta:
		model = Member
		fields = ('first_name', 'last_name', 'nick_name', 'birthday', 'club')


class ShotSerializer(ModelSerializer):
	class Meta:
		model = Shot
		fields = ('value', 'number')


class SequenceSerializer(ModelSerializer):
	shot_set = ShotSerializer(many=True, read_only=True)
	member = MemberSerializer(read_only=True)

	class Meta:
		model = Sequence
		fields = ('member', 'profile', 'shot_set')


class MonitorQueueElementSerializer(ModelSerializer):
	sequence = SequenceSerializer(read_only=True)

	class Meta:
		model = MonitorQueueElement
		fields = ('monitor_setting', 'sequence')


class MonitorQueueElementView(APIView):

	def get(self, request):
		element = MonitorQueueElement.objects.all().order_by('-queued').last()
		if element is None:
			return HttpResponseNotFound("No element in queue")
		data = MonitorQueueElementSerializer(element).data
		element.delete()

		return Response(data)
