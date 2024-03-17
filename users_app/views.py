from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserAddForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def index(request):
    return render(request,"index.html")

def signup(request):
    if request.method == "POST":
        print("Form submitted:", request.POST)
    form = UserAddForm(request.POST)
    if form.is_valid():
        user = form.save()
        group = Group.objects.get(name='users')
        user.groups.add(group)
        login(request, user)
        messages.info(request, "User Created")
        return redirect('signin')
    else:
        print("Form errors:", form.errors)

    return render(request, "users/signup.html", {"form": form})


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("viewpage")
        else:
            messages.error(request, "Username or password incorrect")
    

    return render(request, "users/login.html")

def viewpage(request):
    return render(request,"users/viewpage.html")