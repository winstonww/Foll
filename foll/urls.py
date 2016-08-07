from django.conf.urls import url
from . import views
from foll.viewsets import FoodRatingAPIViewSet
from rest_framework import renderers
from django.conf.urls import url, include
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'process_food_rating', FoodRatingAPIViewSet, base_name='process_food_rating')



urlpatterns = [
		url(r'^$' ,views.signup, name = 'signup'),
		url(r'^home$' ,views.index, name = 'index'),
		url(r'^(?P<party_id>[0-9]+)$', views.party_details, name = 'party_details'),
		url(r'^delete/(?P<food_id>[0-9]+)$)', views.delete_food, name = 'delete_food'),
		url(r'^signout$', views.signout, name = 'signout'),
		url(r'^api/process_invitation/(?P<invitation_id>[0-9]+)$', views.process_invitiation, name = 'process_invitation'),
		url(r'^api/user_in_party/$', views.userInPartyAPI, name = 'userInPartyAPI'),

		# url(r'^api/', include(router.urls, namespace='api')),
		url(r'^api/process_food_rating/$', views.process_food_rating, name = 'process_food_rating'),
]
