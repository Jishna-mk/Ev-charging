from django.shortcuts import render
from django.shortcuts import render,redirect
from users_app.forms import UserAddForm

from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

from django.contrib.auth.decorators import login_required
from datetime import timedelta
from .forms import StationProfileForm
from .models import StationProfile
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
                return redirect('view_stations')
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

def delete_station(request,pk):
    station =Station.objects.get(station_ID=pk)
    station.delete()
    messages.info(request,"station details deleted")
    return redirect('view_stations')
   

def station_profiles(request):
    station_profile=get_object_or_404( StationProfile,user=request.user)
    return render(request,'station/profile.html',{'station_profile':station_profile})   

from users_app.models import Booking
from django.core.exceptions import ObjectDoesNotExist


# @login_required
# def bookings(request):
#     user_bookings = Booking.objects.select_related('station').all()
#     return render(request, "station/booking.html", {'user_bookings': user_bookings})
@login_required
def bookings(request):
    # Retrieve all bookings with related station information
    user_bookings = Booking.objects.select_related('station').all()
    
    # Group bookings by station names
    grouped_bookings = {}
    for booking in user_bookings:
        station_name = booking.station.station_name
        if station_name not in grouped_bookings:
            grouped_bookings[station_name] = []
        grouped_bookings[station_name].append(booking)

    return render(request, "station/booking.html", {'grouped_bookings': grouped_bookings})
# @login_required
# def bookings(request):
#     # Retrieve the current user's bookings
#     user = request.user
#     user_bookings = Booking.objects.select_related('station').filter(user=user)
    
#     # Group bookings by station names
#     grouped_bookings = {}
#     for booking in user_bookings:
#         station_name = booking.station.station_name
#         if station_name not in grouped_bookings:
#             grouped_bookings[station_name] = []
#         grouped_bookings[station_name].append(booking)

#     return render(request, "station/booking.html", {'grouped_bookings': grouped_bookings})


# @login_required
# def bookings(request):
#     # Get the current user's station profile
#     station_profile = get_object_or_404(StationProfile, user=request.user)
    
#     # Get the station associated with the user's station profile
#     station = station_profile.station
    
#     # Filter bookings related to the station
#     user_bookings = Booking.objects.select_related('station').filter(station=station)
    
#     return render(request, "station/booking.html", {'user_bookings': user_bookings})

from users_app.models import Message

def send_message_to_user(request):
    if request.method == "POST":
        station= get_object_or_404(StationProfile, user=request.user)
        user_id = request.POST.get("user_id")  # Assuming you have a hidden input with user_id in your form
        user = get_object_or_404(User, id=user_id)
        message_text = request.POST["message"]

        # Create a new message with reply set to False for new messages to users
        Message.objects.create(message=message_text, station=station, user=user, reply=False)

        messages.info(request, "Message Sent")
        return redirect("view_company_messages")

    # Handle GET requests or other cases
    return redirect("view_company_messages")


def view_company_messages(request):
    station = get_object_or_404(StationProfile, user=request.user)
    user_messages = Message.objects.filter(station=station, reply=False)
    reply_messages = Message.objects.filter(station=station, reply=True)
    user_messages_count = user_messages.count()
    reply_messages_count = reply_messages.count()
    return render(request, "station/view-messages.html", {
        "user_messages": user_messages,
        "reply_messages": reply_messages,
        "user_messages_count": user_messages_count,
        "reply_messages_count": reply_messages_count
    })

def reply_message(request, id):
    if request.method == "POST":
        station = get_object_or_404(StationProfile, user=request.user)
        user = get_object_or_404(User, id=id)
        message_text = request.POST["message"]

        # Create a new message with reply set to True for user's sent messages
        Message.objects.create(message=message_text, station=station, user=user, reply=True)

        messages.info(request, "Message Sent")
        return redirect("view_company_messages")        
# from users_app.models import UserProfile
# def send_message_to_user(request):
#     if request.method == "POST":
#         station_profile = get_object_or_404(UserProfile, user=request.user)
#         message_text = request.POST.get("message")
#         user_id = request.POST.get("user_id")
#         user_profile = get_object_or_404(UserProfile, id=user_id)

#         # Create a new message with reply set to False for new messages to users
#         Message.objects.create(message=message_text, station=station_profile.station, user=user_profile.user, reply=False)

#         messages.info(request, "Message Sent")
#         return redirect("view_company_messages")

#     # Handle GET requests or other cases
#     return redirect("view_company_messages")

# def view_company_messages(request):
#     station_profile = get_object_or_404(UserProfile, user=request.user)
#     user_messages = Message.objects.filter(station=station_profile.station, reply=False)
#     reply_messages = Message.objects.filter(station=station_profile.station, reply=True)
#     user_messages_count = user_messages.count()
#     reply_messages_count = reply_messages.count()
#     return render(request, "company/view-messages.html", {
#         "user_messages": user_messages,
#         "reply_messages": reply_messages,
#         "user_messages_count": user_messages_count,
#         "reply_messages_count": reply_messages_count
#     })

# def reply_message(request, id):
#     if request.method == "POST":
#         station_profile = get_object_or_404(UserProfile, user=request.user)
#         user_profile = get_object_or_404(UserProfile, id=id)
#         message_text = request.POST["message"]

#         # Create a new message with reply set to True for user's sent messages
#         Message.objects.create(message=message_text, station=station_profile.station, user=user_profile.user, reply=True)

#         messages.info(request, "Message Sent")
#         return redirect("view_company_messages")