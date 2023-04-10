from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("login_user")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

    # return render (request, "register.html", {"register_form": NewUserForm()})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username , password=password)
            if user is not None:
                login(request , user)
                return redirect("home_page")
            else:
                return redirect("login_user")
        else:
            return redirect("login_user")
    form = AuthenticationForm()
    return render(request=request , template_name="login.html",context={"login_form":form})

def logout_user(request):
    logout(request)
    return redirect("login_user") 