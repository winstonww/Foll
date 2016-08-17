from django.forms import ModelForm
from django.db import models
from foll.models import Food, Party, UserInParty
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.models import User

from crispy_forms.bootstrap import InlineField, StrictButton
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, Field
from datetimewidget.widgets import DateTimeWidget

#autocomplete
# from dal import autocomplete

class FoodForm(ModelForm):
	rating = forms.IntegerField(label = "rating:", min_value=1, max_value=50)
	def __init__(self, *args, **kwargs):
		super(FoodForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-exampleForm'
		self.helper.form_class = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.form_action = 'party_details'
		self.helper.add_input(Submit('submit_food', 'Submit Food'))
	class Meta:
		model = Food
		fields = ['price', 'name', 'desc', 'rating']





class PartyForm(ModelForm):
	date_time = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3),  required = True)
	max_budget = forms.IntegerField(required = True)
	max_size = forms.IntegerField(required = True)
	location = forms.CharField(required = True)
	name = forms.CharField(required = True)
	def __init__(self, *args, **kwargs):
		super(PartyForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'partyform'
		self.helper.form_method = 'post'
		self.helper.form_action = 'index'
		self.helper.layout = Layout(
								Div(
								  Field('name', id="party_name", css_class="party_name", title="Party Name"),
						 	      Field('location', template = "foll/location_form.html"),
						 	      Field('date_time', id="party_date_time",  title="Date and Time"),
						 	      Field('max_size', id="party_max_size",  title="Estimated Number of Participants"),
						 	      Field('max_budget', id="party_max_budget",  title="Total Budget")
						 	    )
							)
		self.fields['max_budget'].label = "Max Budget (round to the nearest integer)"
		self.helper.add_input(Submit('submit_party', 'Submit'))
	class Meta:
		model = Party
		fields = ['name',  'location', 'date_time', 'max_size', 'max_budget']
		widgets = {'datetime': DateTimeWidget(attrs={'id':"party_date_time"}, usel10n = True, bootstrap_version=3)}


class UserSignUpForm(ModelForm):
	password = forms.CharField(widget = forms.PasswordInput)
	class Meta:
		model = User
		fields  = ['username', 'email', 'password']
	def __init__(self, *args, **kwargs):
		super(UserSignUpForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-exampleForm'
		# self.helper.form_class = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.form_action = 'signup'
		self.helper.add_input(Submit('submit_signup', 'Register'))





class LoginForm(forms.Form):
	username = forms.CharField(max_length = 30)
	password = forms.CharField(widget = forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_class = 'form-inline navbar-form navbar-right'
		self.helper.field_template = 'bootstrap3/layout/inline_field.html'
		self.helper.layout = Layout(
    					'username',
   						'password',

    					Submit('submit_login', 'Sign In', css_class='btn btn-secondary'),
						)
		self.helper.form_method = 'post'
		self.helper.form_action = 'signup' #SHOULD LINK TO SIGNUP TO COMPLETE LOGIN PROCEDURE
		





class PartyInvitationForm(ModelForm):
	# invite_message = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = UserInParty
		fields = ['user', 'invite_message']
		# widgets = {
		# 	'user': autocomplete.ModelSelect2(url = 'user-autocomplete')
		# }


	def __init__(self, *args, **kwargs):
		super(PartyInvitationForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_id = 'id-exampleForm'
		self.helper.form_class = 'blueForms'
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit_invitation', 'Send Inivtation'))
		