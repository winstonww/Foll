# viewset API
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from foll.serializers import FoodRatingSerializer
from foll.models import FoodRating
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from foll.views import JSONResponse
# facebook API

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework.decorators import detail_route, list_route






class FoodRatingAPIViewSet(viewsets.ModelViewSet):

	serializer_class = FoodRatingSerializer

	def get_queryset(self):
		queryset = FoodRating.objects.all()
		#if you need to get subscription by name
		name = self.request.query_params.get('name', None)
		if name is not None:
			queryset = queryset.filter(name=name)
		return queryset 

	






# @csrf_exempt
# def process_food_rating(request, food_id):
# 	try:
# 		m_food = Food.objects.get(id = food_id)
# 	except ObjectDoesNotExist:
# 		raise Http404("food does not exist")
# 	if request.method == 'GET':
# 		# all_food_rating = FoodRating.objects.all().filter(rated_by = request.user)
# 		# serializer = FoodRatingSerializer(all_food_rating, many = True)
# 		all_food_rating = FoodRating.objects.get(food__id = food_id)
# 		serializer = FoodRatingSerializer(all_food_rating)
# 		return JSONResponse(serializer.data)
# 	elif request.method == 'POST':
# 		serializer = FoodRatingSerializer(data = request.data)
# 		if serializer.is_valid():
# 			try:
# 				original_rating = FoodRating.object.get(rated_by = request.user, food = m_food)
# 			except ObjectDoesNotExist:
# 				serializer.save()
# 				return JSONResponse(serializer.data , status = 201)
# 			original_rating.rating = serializer.validated_data.rating
# 			return JSONResponse("successful")
# 	elif request.method == 'DELETE':
# 		user_in_party_status.delete()
# 		return HttpResponse(status=204)