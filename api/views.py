from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from competition.models import Weapon


class ReleaseWeapon(APIView):

	def get(self, request, pk):
		weapon = Weapon.objects.get(pk=pk)
		weapon.current_record = None
		weapon.save()
		return Response({"message": "Successfully released weapon"})
