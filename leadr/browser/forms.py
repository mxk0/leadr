from django import forms
from django.contrib.auth.models import User
from leadr.browser.models import Entry

class RegistrationForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'spanhome'}))	
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'spanhome'}))

	class Meta():
		model = User
		fields = ['first_name']
		widgets = {
			'first_name':forms.TextInput(attrs={'placeholder':'Full name', 'class':'spanhome'}),
		}


class RegistrationModalForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'spanmodal'}))	
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'class':'spanmodal'}))

	class Meta():
		model = User
		fields = ['first_name']
		widgets = {
			'first_name':forms.TextInput(attrs={'placeholder':'Full name', 'class':'spanmodal'}),
		}


class LoginForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'spanhome'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class':'spanpwd'}))

	class Meta():
		model = User


class LoginModalForm(forms.ModelForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email', 'class':'spanmodal'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class':'spanmodalpwd'}))

	class Meta():
		model = User


class EntryForm(forms.Form):
	raw_address = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}))
	title = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}))
	tags = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}), required=False)





