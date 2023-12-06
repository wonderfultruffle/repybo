from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_pw = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_pw)
            login(request, user)
            return redirect("pybo:index")
    else:
        form = SignUpForm()

    return render(request, "common/signup.html", {"form": form})

