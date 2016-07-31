from rest_framework import serializers
from foll.models import UserInParty, FoodRating

class UserInPartySerializer(serializers.ModelSerializer):
	class Meta:
		model = UserInParty

class FoodRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = FoodRating
		fields = ('food' , 'rating')

