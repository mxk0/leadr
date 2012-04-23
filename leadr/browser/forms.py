from django import forms
from django.contrib.auth.models import User
from leadr.browser.models import Entry

class RegistrationForm(forms.ModelForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email - used for account notifications only.', 'class':'spanhome'}))	
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


class EntryForm(forms.ModelForm):
	raw_address = forms.CharField(widget=forms.TextInput(attrs={'class':'span3_form'}))
	title = forms.CharField(widget=forms.TextInput(attrs={'class':'span3_form'}), required=False)
	tags = forms.CharField(widget=forms.TextInput(attrs={'class':'span3_form'}), required=False)

	class Meta():
		model = Entry


class EditForm(forms.ModelForm):
	raw_address = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}))
	title = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}), required=False)
	tags = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}), required=False)

	class Meta():
		model = Entry

	# uid = forms.CharField(widget=forms.TextInput(attrs={'class':'span5'}))

	# def __init__(self, id):
	# 	super(EditForm, self).__init__()
	# 	e = Entry.objects.get(id=id)
	# 	self.fields['uid'].widget.placeholder = e.id





