from django.shortcuts import render, redirect
from django.http import HttpResponse
from foll.forms import PartyForm, FoodForm, UserSignUpForm, LoginForm, PartyInvitationForm, PartyInvitationFormAlternative
from foll.models import Party, Food, FoodRating, UserInParty, TopRatedFood, UserData
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.http import Http404
from partyfood import settings

# Serializer API

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from foll.models import UserInParty
from foll.serializers import UserInPartySerializer, FoodRatingSerializer


#from utils.py
from foll.utils import find_average_rating, TopFood

#django_facebook
from open_facebook import OpenFacebook
from django_facebook.api import require_facebook_graph, FacebookUserConverter
from django.contrib.auth import get_user_model

from open_facebook.api import FacebookAuthorization
#autocomplete
from dal import autocomplete


def index(request):
	if request.user.is_authenticated() == False:
		return redirect("signup")
		# return HttpResponse("damnnn doug")
	context_instance = RequestContext(request)

	User = get_user_model()
	new_user_data = UserData.objects.all().filter(local_django_id = request.user.id)
	query_access_token = request.POST.get(
        'access_token',
        request.GET.get('access_token'))

	FacebookAuthorization.extend_access_token(query_access_token)
	try:
		graph = require_facebook_graph(request)
	except:
		logout(request)
		# return HttpResponse("omg")
		return redirect("signup")

	my_info = graph.get('me')

	if not new_user_data:
		new_user = UserData()
		new_user.local_django_id = request.user.id
		new_user.facebook_id = my_info['id']
		new_user.facebook_name = my_info['name']
		new_user.save()

	if (request.method == 'POST') and 'submit_party' in request.POST:
		party_form = PartyForm(request.POST)
		if party_form.is_valid():
			new_party_info = party_form.save(commit = False) #if commit = false, only model info will be created , not saved
			new_party_info.location_lat = request.POST['lat']
			new_party_info.location_lng = request.POST['lng']
			new_party_info.save()
			new_user_in_party = UserInParty()
			new_user_in_party.user = request.user
			new_user_in_party.invited_by = request.user
			new_user_in_party.invitation_accepted = 1
			new_user_in_party.party = new_party_info
			new_user_in_party.save()
			return party_details(request, new_party_info.id)
		else:
			return HttpResponse(party_form.errors)
			print (party_form.errors)
	else:
		party_form = PartyForm()
		invitation_form = PartyInvitationForm()

	party_info = []


	#retrieve info from facebook
	# graph = OpenFacebook(access_token)
	

	converter = FacebookUserConverter(graph)
	my_friends = converter.get_friends()
	# my_friends = User.objects.all()


	my_party = UserInParty.objects.all().filter(user = request.user, invitation_accepted = 1)
	for friend_party_pair in my_party:
		party_info.append(friend_party_pair.party)
	party_num = len(party_info)

	party_invitations = []
	party_invitations = UserInParty.objects.all().filter(user = request.user, invitation_accepted = 0)
	invitation_num = len(party_invitations)
	food_newsfeed = Food.objects.none()
	friends_in_party_newsfeed = UserInParty.objects.none()
	# Update the news feed, take the top 5 most recent
	for party in party_info:
		party_food_newsfeed = Food.objects.all().filter(belong_to_party = party).order_by('-date_added')
		food_newsfeed = food_newsfeed | party_food_newsfeed
		party_friends_in_party_newsfeed = UserInParty.objects.all().filter(party = party, invitation_accepted = 1).order_by('-date_accepted')
		friends_in_party_newsfeed = friends_in_party_newsfeed | party_friends_in_party_newsfeed
	food_newsfeed = food_newsfeed[:5]
	friends_in_party_newsfeed = friends_in_party_newsfeed[:5]
	food_newsfeed_num = len(food_newsfeed)
	members_newsfeed_num = len(friends_in_party_newsfeed)

	#update food to bring, code to be updated
	all_top_rated_food = TopRatedFood.objects.all()
	top_rated_food_ids = []
	for topfood in all_top_rated_food:
		top_rated_food_ids.append(topfood.top_rated_food_id)
	food_to_bring = Food.objects.all().filter(id__in = top_rated_food_ids, brought_by = request.user)




	context = {"party_form": party_form, "party_info": party_info, "party_invitations": party_invitations,
	"invitation_num": invitation_num, "party_num": party_num, "food_newsfeed": food_newsfeed,
	"friends_in_party_newsfeed": friends_in_party_newsfeed, "food_newsfeed_num": food_newsfeed_num,
	"members_newsfeed_num": members_newsfeed_num , "food_to_bring": food_to_bring, "food_to_bring_length": len(food_to_bring)
	, "my_info": my_info, "my_friends":my_friends}


	return render(request, 'foll/intro.html', context, context_instance)










def party_details(request, party_id):
	if request.user.is_authenticated() == False:
		return redirect('signup') # return to signup page if user is not authenticated

	try: # if user is logged in but is not in the party stated in the url, redirect to error page
		temp_party =  Party.objects.get(pk = party_id)
		users_in_party = UserInParty.objects.get(user = request.user, party = temp_party )
	except ObjectDoesNotExist:
   		return redirect('index')

	if (request.method == 'POST') and 'submit_food' in request.POST:
		food_form = FoodForm(request.POST)
		invitation_form = PartyInvitationFormAlternative()
		food_form.helper.form_action = reverse('party_details', args= [party_id])
		invitation_form.helper.form_action = reverse('party_details', args= [party_id])
		if food_form.is_valid():
			new_food_info = food_form.save(commit = False)
			new_food_info.brought_by = request.user
			new_food_info.belong_to_party = Party.objects.get(pk = party_id)
			new_food_info.save()
			new_food_in_party = FoodRating()
			new_food_in_party.food = new_food_info
			temp = food_form.cleaned_data['rating'] #conventional way of getting datum from form
			new_food_in_party.rating = temp
			new_food_in_party.save()

	elif (request.method == 'POST') and 'submit_invitation' in request.POST:
		invitation_form = PartyInvitationFormAlternative(request.POST)
		food_form = FoodForm()
		food_form.helper.form_action = reverse('party_details', args= [party_id])
		invitation_form.helper.form_action = reverse('party_details', args= [party_id])
		if invitation_form.is_valid():

			raw_data = invitation_form.save(commit = False)
			new_invitation_user_data = UserData.objects.get(facebook_name = raw_data.faceook_name)

			new_invitation = UserInParty.objects.create()
			User = get_user_model()
			new_invitation.user = User.objects.get( id = new_invitation_user_data.local_django_id)
			new_invitation.invited_by = request.user
			new_invitation.party = Party.objects.get(pk = party_id)
			new_invitation.invitation_accepted = 0
			new_invitation.date_accepted = datetime.now()
			new_invitation.save()
		else:
			return index(request)

	else:
		food_form = FoodForm()
		food_form.helper.form_action = reverse('party_details', args= [party_id]) # which view function to be redirected to
		invitation_form = PartyInvitationFormAlternative()
		invitation_form.helper.form_action = reverse('party_details', args= [party_id])

	this_party = Party.objects.get(pk = party_id)
	partyfood_list = Food.objects.all().filter(belong_to_party = this_party)
	food_list_ids = []
	for partyfood in partyfood_list:
		food_list_ids.append(partyfood.id)
		partyfood.avg_rating = find_average_rating(partyfood.id)
		partyfood.save()


	partyfood_list_empty = True if len(partyfood_list) == 0 else False
	users_in_this_party = UserInParty.objects.all().filter(party = temp_party)



	TopRatedFood.objects.all().filter(top_rated_food_id__in = food_list_ids).delete()
	top_rated_food_class = TopFood()
	best_food_ids = top_rated_food_class.top_rated_food_under_price_constraints(party_id)
	for best_id in best_food_ids:
		TopRatedFood.objects.create(top_rated_food_id = best_id)
	best_food_list = Food.objects.filter(id__in = best_food_ids)
	best_food_list_length = len(best_food_ids)



	# TopRatedFood.objects.all().filter(top_rated_food_id__in = food_list_ids).delete()
	# top_rated_food_class = TopFood()
	# best_food_list_length = top_rated_food_class.top_rated_food_under_price_constraints(party_id)
	# best_food_ids = []
	# for best_id in best_food_ids:
	# 	TopRatedFood.objects.create(top_rated_food_id = best_id)
	# best_food_list = Food.objects.filter(id__in = best_food_ids)


	# For sidebar notification only
	party_invitations = UserInParty.objects.all().filter(user = request.user, invitation_accepted = 0)
	invitation_num = len(party_invitations)
	party_info = []
	my_party = UserInParty.objects.all().filter(user = request.user, invitation_accepted = 1)
	for friend_party_pair in my_party:
		party_info.append(friend_party_pair.party)
	party_num = len(party_info)
	# Update the news feed, take the top 5 most recent
	for party in party_info:
		food_newsfeed = Food.objects.all().filter(belong_to_party = party).order_by('-date_added')[:5]
		friends_in_party_newsfeed = UserInParty.objects.all().filter(party = party, invitation_accepted = 1).order_by('-date_accepted')[:5]
	food_newsfeed_num = len(food_newsfeed)
	members_newsfeed_num = len(friends_in_party_newsfeed)


	context = {'food_form': food_form, 'party': this_party, 'partyfood_list' : partyfood_list,
	'party_food_list_num': len(partyfood_list), 'invitation_form': invitation_form,
	"partyfood_list_empty": partyfood_list_empty,"users_in_this_party": users_in_this_party,
	"best_food_list": best_food_list, "best_food_ids": best_food_ids,"invitation_num": invitation_num,
	"party_num": party_num, "food_newsfeed_num": food_newsfeed_num, "members_newsfeed_num": members_newsfeed_num,
	"best_food_list_length": best_food_list_length }

	return render(request, 'foll/party_details.html', context)







def signup(request):

	if request.user.is_authenticated():
		return redirect('index')

	signup_form = UserSignUpForm()
	user_login_form = LoginForm()
	no_user_flag = False
	context = {'signup_form': signup_form, 'user_login_form': user_login_form, "no_user_flag" : no_user_flag}

	if (request.method == 'POST') and 'submit_signup' in request.POST:
		signup_form = UserSignUpForm(request.POST)
		if signup_form.is_valid():
			user_signup = signup_form.save(commit = False)
			username = signup_form.cleaned_data['username']
			password = signup_form.cleaned_data['password']
			email = signup_form.cleaned_data['email']
			user_signup.username = username
			user_signup.set_password(password)
			user_signup.email = email
			user_signup.save()
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				no_user_flag = False
				return redirect('index')
			else:
				no_user_flag = True
				return redirect('index')

	elif (request.method == 'POST') and 'submit_login' in request.POST:
		user_login_form = LoginForm(request.POST)
		if user_login_form.is_valid():
			username = user_login_form.cleaned_data['username']
			password = user_login_form.cleaned_data['password']
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				no_user_flag = False
				return redirect('index')
			else:
				no_user_flag = True

	context = {'signup_form': signup_form, 'user_login_form': user_login_form, "no_user_flag" : no_user_flag}
	return render(request, 'foll/signup.html', context)



def delete_food(request, food_id):
	# delete the food along with its rating record
	
	food_to_be_deleted = Food.objects.get(id = food_id)
	party = food_to_be_deleted.belong_to_party
	ratings_to_be_deleted = FoodRating.objects.all().filter(food = food_to_be_deleted)
	food_to_be_deleted.delete()
	ratings_to_be_deleted.delete()
	return redirect(party_details, party_id = pary.id)




def signout(request):
	logout(request)
	return redirect("signup")



class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)



@csrf_exempt
def userInPartyAPI(request):


	if request.method == 'GET':
		partys_of_user = UserInParty.objects.all().filter(user = request.user)
		serializer = UserInPartySerializer(partys_of_user, many = True)
		return JSONResponse(serializer.data)
	elif reuqest.method == 'POST':
		raw_data = JSONParser.parse(request)
		serializer = UserInPartySerializer(data = raw_data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data , status = 201 )
		return JSONResponse(serializer.errors, status = 400)



@csrf_exempt
def process_invitiation(request, invitation_id):

	user_in_party_status = UserInParty.objects.get(invitation_id = invitation_id)

	if request.method == 'GET':
		user_in_party_status.invitation_accepted = 1
		user_in_party_status.save()
		serializer = UserInPartySerializer(user_in_party_status)
		return JSONResponse(serializer.data)
	if request.method == 'POST':
		user_in_party_status.invitation_accepted = 1
		user_in_party_status.save()
		serializer = UserInPartySerializer(user_in_party_status)
		return JSONResponse(serializer.data)
	elif request.method == 'DELETE':
		user_in_party_status.delete()
		return HttpResponse(status=204)



@csrf_exempt
def process_food_rating(request):

	if request.method == 'GET':
		# all_food_rating = FoodRating.objects.all().filter(rated_by = request.user)
		# serializer = FoodRatingSerializer(all_food_rating, many = True)
		all_food_rating = FoodRating.objects.all()
		serializer = FoodRatingSerializer(all_food_rating)
		return JSONResponse(serializer.data)
	elif request.method == 'POST':

		for key in request.POST:
			try:
				new_rating = FoodRating.objects.get(food__id = key, rated_by = request.user)

			except ObjectDoesNotExist:
				new_rating = FoodRating()
				new_rating.rated_by = request.user

			new_rating.rating = request.POST[key]
			new_rating.save()

		return JSONResponse("successful")

	elif request.method == 'DELETE':
		user_in_party_status.delete()
		return HttpResponse(status=204)

# @csrf_exempt

class UserAutoComplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# if not self.request.user.is_authenticated():
		# 	return
		# User = get_user_model()
		# my_info = graph.get('me')
		# converter = FacebookUserConverter(graph)
		# my_friends = converter.get_friends()
		# my_friends_facebook_id = []
		# for friend in my_Friends:
		# 	if friend["id"] == None:
		# 		continue
		# 	else:
		# 		my_friends_facebook_id.append(friend["id"])
		# users = User.objects.all().filter(facebook_id__in = my_friends_facebook_id)
		users = UserData.objects.all()
		return users


# retreive data from form
#1. food_form.save(commit = False)
# 2. food_form.cleaned_data['rating']

# retrieve instances from model:
# 1. retrieve instances with foreign key -- .objecst.filter()
# 2. objects.all()

# accesss instance attributes
# party.name

# url
# regular expression sends some arguments say link.id
# view function should take in parameter (request, link.id)

#request
# carries information from an IP address