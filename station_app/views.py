from django.shortcuts import render
from django.shortcuts import render,redirect
from users_app.forms import UserAddForm

from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .forms import StationProfileForm
# Create your views here.
def details(request):
    return render(request,"station\details.html")


def stationsignup(request):
    form=UserAddForm()
    s_form=StationProfileForm()
    if request.method=="POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username is Already Exists")
                return redirect('stationsignup')
            if User.objects.filter(email=email).exists():
                messages.info(request,"This Emailid is Already Taken")
                return redirect('stationsignup')
            
            new_user = form.save()
            new_user.is_active = False
            new_user.save()
                
            group = Group.objects.get(name='station')
            new_user.groups.add(group) 

            s_form = StationProfileForm(request.POST,request.FILES)
            if s_form.is_valid():
                manager = s_form.save()
                manager.user = new_user
                manager.save()
                messages.success(request,"Registered as Station! Wait for Approval")
                return redirect('stationsignin')
            else:
                messages.success(request,"Couldn't perform  Signup")
        else:
           
            print(form.errors)
    return render(request,"station\signup.html",{"form":form,"s_form":s_form})



def stationsignin(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['password']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            messages.info(request,'Logged In Successfully')
            login(request, user1)
            group = request.user.groups.all()[0].name
            if(group == "station"):
                return redirect('details')
            else:
                messages.info(request,'Username or Password Incorrect')
                return redirect("stationsignout")
        
        else:
            messages.info(request,'Username or Password Incorrect')
            return redirect('stationsignin')
    return render(request,"station\signin.html")


def stationsignout(request):
    logout(request)
    return redirect('index')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Station
from .forms import StationForm

def add_station(request):
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_stations')
    else:
        form = StationForm()
    return render(request, 'station/add_station.html', {'form': form})

def view_stations(request):
    stations = Station.objects.all()
    return render(request, 'station/view_station.html', {'stations': stations})
def edit_station(request, station_id):
    station = get_object_or_404(Station, station_ID=station_id)
    if request.method == 'POST':
        form = StationForm(request.POST, request.FILES, instance=station)
        if form.is_valid():
            form.save()
            return redirect('view_stations')
    else:
        form = StationForm(instance=station)
    return render(request, 'station/edit_station.html', {'form': form})

def delete_station(request, station_id):
    station = get_object_or_404(Station, station_ID=station_id)
    if request.method == 'POST':
        station.delete()
        return redirect('view_stations')
    # For GET request, display a confirmation message
    return redirect('view_stations')