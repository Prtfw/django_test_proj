from django import forms
from .models import Tx
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class TxForm(forms.ModelForm):
	class Meta:
		model = Tx
		fields= ["item", "completed"]



class registerForm(UserCreationForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
	first = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'class': 'form-control'}))
	last = forms.CharField(max_length =50, widget=forms.TextInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields= ["username", "password1", "password2", "first_name", 'first_name', 'email', ]

	def __init__(self, *args, **kwargs):
		super(registerForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'



class editProfileForm(UserChangeForm):
	class Meta:
		model = User
		fields= ["username", "first_name", 'last_name', 'email', 'password']

	def __init__(self, *args, **kwargs):
		super(editProfileForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
