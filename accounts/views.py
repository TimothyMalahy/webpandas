from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from .forms import *



def Signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user, created = User.objects.get_or_create(username = username)
            if created == True:
                pass
                # TODO - Error username already exists please use a different one or try to login
            else:
                user.set_unusable_password()
                user.save()
            # user = authenticate(username=username, password=raw_password)
            # user.set_unusable_password()
            # user.save()
            # login(request, user)
            return redirect('core:home')
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})