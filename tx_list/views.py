from django.shortcuts import render, redirect
from .models import Tx
from .forms import TxForm, registerForm, editProfileForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
# from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse

import stripe

from paymt_app import settings
import time

stripe.api_key = settings.STRIPE_SECRET_KEY

import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash



def home(request):

	if request.method == 'POST':
		form = TxForm(request.POST or None)

		if form.is_valid():
			form.save()
			all_items = Tx.objects.all().order_by('-item')
			messages.success(request, ('Item Has Been Added To List!'))
			# return render(request, 'home.html', {'all_items': all_items})

	else:
		all_items = Tx.objects.all().order_by('-item')
		return render(request, 'home.html', {'all_items': all_items})

def profile(request):
	return render(request, 'profile.html', {})

def delete(request, list_id):
	item = Tx.objects.get(pk=list_id)
	item.delete()
	messages.success(request, ('Item Has Been Deleted!'))
	return redirect('home')

def cross_off(request, list_id):
	item = Tx.objects.get(pk=list_id)
	item.amt = True
	item.save()
	return redirect('home')

def uncross(request, list_id):
	item = Tx.objects.get(pk=list_id)
	item.amt = False
	item.save()
	return redirect('home')

def edit(request, list_id):
	if request.method == 'POST':
		item = Tx.objects.get(pk=list_id)
		print(request.POST)
		form = TxForm(request.POST or None, instance=item)

		if form.is_valid():
			form.save()
			messages.success(request, ('Item Has Been Edited!'))
			return redirect('home')
		return HttpResponseRedirect('/')


	else:
		item = Tx.objects.get(pk=list_id)
		return render(request, 'edit.html', {'item': item})


def user_login(request):
	context = {}
	user=None
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		print()
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ('You are logged in.'))
			print(user, username, password)
			return redirect('home')
		else:
			return redirect('login')
	context = {'meth': request.method, 'user': user}
	js_data = json.dumps(context,  cls=DjangoJSONEncoder)

	return render(request, 'auth/login.html', {'dj_data': js_data})

def user_logout(request):
	logout(request)
	messages.success(request, ('You are logged out.'))
	return redirect('login')

def user_register(request):
	form=registerForm()
	if request.method == 'POST':
		form=registerForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(request, username=username, password=password)
			login(request, user)
			messages.success(request, ('You are signed up.'))
			return redirect('profile')

	context={'form': form}
	return render(request, 'auth/register.html', context)

def edit_profile(request):
	form=editProfileForm(instance=request.user)
	if request.method == 'POST':
		form=editProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('Profile saved.'))
			return redirect('profile')
	context={'form': form}
	return render(request, 'auth/edit_profile.html', context)


def change_pswd(request):
	form=PasswordChangeForm(user=request.user)
	if request.method == 'POST':
		form=PasswordChangeForm(data=request.POST, user=request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request,form.user)
			messages.success(request, ('Password saved.'))
			return redirect('profile')
	context={'form': form}
	return render(request, 'auth/change_pswd.html', context)

def stripe_pay(request):

	# Token is created using Checkout or Elements!
	# Get the payment token ID submitted by the form:
	charge = None

	if request.method == 'POST':
		try:
			token = request.POST.getlist('stripeToken')[0]
			charge = stripe.Charge.create(
			    amount=999,
			    currency='usd',
			    description='',
			    source=token,
			)
			Tx.objects.create(item= int(time.time()), note=charge.description, amt=charge.amount)
			all_items = Tx.objects.all().order_by('-item')
			return render(request, 'home.html', {'all_items': all_items})
		except:
			messages.error(request, ('Payment failed!'))

	return render(request, 'stripe_pay.html', {'charge': charge, 'pubkey': 'pk_test_8aTHebG2tmwAfjbGSyHyqVA5'})


def profile_edit(request):
	print(request.user)
	return render(request, 'profile_edit.html', {'user': request.user})
