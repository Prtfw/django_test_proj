from django.shortcuts import render, redirect
from .models import Tx
from .forms import TxForm, registerForm, editProfileForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.http import HttpResponseRedirect
from django.core.serializers.json import DjangoJSONEncoder


import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash



def home(request):

	if request.method == 'POST':
		form = TxForm(request.POST or None)

		if form.is_valid():
			form.save()
			all_items = Tx.objects.all
			messages.success(request, ('Item Has Been Added To List!'))
			return render(request, 'home.html', {'all_items': all_items})

	else:
		all_items = Tx.objects.all
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
	item.completed = True
	item.save()
	return redirect('home')

def uncross(request, list_id):
	item = Tx.objects.get(pk=list_id)
	item.completed = False
	item.save()
	return redirect('home')

def edit(request, list_id):
	if request.method == 'POST':
		item = Tx.objects.get(pk=list_id)

		form = TxForm(request.POST or None, instance=item)

		if form.is_valid():
			form.save()
			messages.success(request, ('Item Has Been Edited!'))
			return redirect('home')

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
