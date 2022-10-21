from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import forms
from .forms import CustomUserCreationForm


# Create your views here.
def register(request):
    """
    Function login logout register user
    :param request:
    :return:
    """
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('index')
    context = {'form': form}
    return render(request, 'registration/register.html', context)
