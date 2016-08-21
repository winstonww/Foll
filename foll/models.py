from django.db import models
from django.contrib.auth.models import User
from datetime import datetime   


# from django.dispatch.dispatcher import receiver
# from django_facebook.models import FacebookModel
# from django.db.models.signals import post_save
# from django_facebook.utils import get_user_model, get_profile_model
from partyfood import settings

# Create your models here.
class Party(models.Model):
	#has pk
	name = models.CharField(max_length = 30)
	# datetime = models.DateTimeField(auto_now = False, auto_now_add = False)
	location = models.CharField(max_length = 500)
	location_lat = models.DecimalField(default = 43.6629, decimal_places = 4, max_digits = 10)
	location_lng = models.DecimalField(default = 79.3957, decimal_places = 4, max_digits = 10)
	date_time = models.DateTimeField(auto_now_add=False)
	max_size = models.IntegerField()
	max_budget = models.IntegerField()
	# desc = models.CharField(max_length = 2000, default = "")
	def __str__(self):
		return "partyname: " + self.name + " , user id: " + str(self.id)

# class Friends(models.Model):
# 	#no pk
# 	user1 = models.ForeignKey(User)
# 	user2 = models.ForeignKey(User)
# 	status = models.IntegerField() #0 or 1
# 	date_of_friendship = DateField()
# 	desc = models.CharField(maxlength = 200) #A brief description 

# to get around the fact the facebook
class UserData(models.Model):
	facebook_name = models.CharField(max_length = 50)
	local_django_id = models.IntegerField()
	facebook_id = models.IntegerField()
	def __str__(self):
	   return self.facebook_name


class UserInParty(models.Model):
	#no pk
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "user")
	invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = "inviter", default=1)
	party = models.ForeignKey(Party)
	invite_message = models.CharField(max_length = 2000, null=True, blank=True)
	invitation_accepted = models.IntegerField(default = 0)
	date_accepted = models.DateTimeField(auto_now= True, blank=True)
	invitation_id = models.AutoField(primary_key=True)
	user_data = models.ForeignKey(UserData, default = 0)

	def __str__(self):
   		return  self.user.username + " invited " + self.invited_by.username + " to join "+ self.party.name




class Food(models.Model):
	#price = models.DecimalField(decimal_places=2, max_digits = 3)
	price = models.IntegerField(default = 0)
	name = models.CharField(max_length = 30)
	desc = models.CharField(max_length = 200, null=True, blank=True)
	brought_by = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
	belong_to_party = models.ForeignKey(Party, default = 1)
	date_added = models.DateTimeField(auto_now_add= True, blank=True)
	avg_rating = models.DecimalField(default = 0, decimal_places = 2, max_digits = 4)
	def __str__(self):
		return self.name





class FoodRating(models.Model):
	food = models.ForeignKey(Food)
	rated_by = models.ForeignKey(settings.AUTH_USER_MODEL, default = 1)
	rating = models.IntegerField(default = 0)
	def __str__(self):
	   return 'Food: ' + self.food.name + '   ||   Party: '+self.food.belong_to_party.name

class TopRatedFood(models.Model):
	top_rated_food_id = models.IntegerField(default = 0)







