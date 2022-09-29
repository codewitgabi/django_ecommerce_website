from django.shortcuts import render, redirect
from .models import User
from .forms import UserCreationForm


def signup(request):
	form = UserCreationForm()
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("accounts:login")
	context = {"form": form}
	return render(request, "accounts/signup.html", context)