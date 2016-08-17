from django.contrib import admin
from foll.models import Food, Party, FoodRating, UserInParty, User, TopRatedFood
# Register your models here.



class UserInPartyAdmin(admin.ModelAdmin):
    list_display  = ['invitation_id', 'user', 'party', 'invitation_accepted']

admin.site.register(UserInParty, UserInPartyAdmin)

class FoodAdmin(admin.ModelAdmin):
    list_display  = ['id', 'name', 'belong_to_party', 'price', 'avg_rating']

admin.site.register(Food, FoodAdmin)


class PartyAdmin(admin.ModelAdmin):
    list_display  = ['id' ,'name',  'location', 'location_lat', 'location_lng', 'date_time', 'max_size', 'max_budget']

admin.site.register(Party, PartyAdmin)

class TopRatedFoodAdmin(admin.ModelAdmin):
    list_display = ['top_rated_food_id']

admin.site.register(TopRatedFood, TopRatedFoodAdmin)

class FoodRatingAdmin(admin.ModelAdmin):
    list_display  = ['get_rated_by_id' , 'get_food_id', 'rated_by',  'food',  'rating']
    def get_rated_by_id(self, obj):
    	return obj.rated_by.id
    get_rated_by_id.short_description = 'Rater ID'
    get_rated_by_id.admin_order_field = 'rated_by__id'
    def get_food_id(self, obj):
    	return obj.food.id
    get_rated_by_id.short_description = 'Food ID'
    get_rated_by_id.admin_order_field = 'food__id' 
admin.site.register(FoodRating, FoodRatingAdmin)


