from django.shortcuts import render,redirect

from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

from datetime import timedelta
from django.utils import timezone
# Create your views here.


def admin_signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            request .session["username"]=username
            request .session["password"]=password
            login(request,user)
            return redirect("dashboard")
        else:
            
            messages.info(request,"username or password incorrect")
            return redirect("admin_signin")

    return render(request,"admin/adminlogin.html")

def admin_signout(request):
    logout(request)
    return redirect("admin_signin")  

def dashboard(request):
    return render(request,"dashboard.html")
