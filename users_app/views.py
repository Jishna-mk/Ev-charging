from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserAddForm,UserProfileForm
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from station_app.models import Station
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from station_app.models import StationProfile
from django.http import JsonResponse


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
        messages.info(request, "New User Created")
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
    
    stations = Station.objects.all()
    return render(request, 'users/viewpage.html', {'stations': stations})
    


@login_required
def build_profile(request):
    try:
        # Try to get the existing profile for the current user
        profile = UserProfile.objects.get(user=request.user)
        messages.warning(request, "Profile already exists. You can edit it.")
        return redirect('view_profile', username=request.user.username)
    except UserProfile.DoesNotExist:
        # If the profile doesn't exist, proceed with creating a new one
        pass

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile Created Successfully!")
            return redirect('view_profile', username=request.user.username)
    else:
        form = UserProfileForm()

    return render(request, 'users/build_profile.html', {'form': form})

@login_required
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'users/view_profile.html', {'user': user, 'profile': profile})

def station_profile(request):
    # Fetch all StationProfile objects
    station_profiles = StationProfile.objects.all()

    # Add additional functionality here if needed, such as filtering
    # station_profiles = StationProfile.objects.filter(some_criteria)

    return render(request, 'users/station_profile.html', {'station_profiles': station_profiles})

def view_details(request,station_ID):
    station=get_object_or_404(Station,pk=station_ID)

    return render(request,"users/viewdetails.html",{'station':station})

from django.utils import timezone
from .models import Booking
from .forms import BookingForm

# views.py
from django.http import JsonResponse
from django.forms import ValidationError

from django.utils import timezone



def book_slot(request, station_id):
    station = get_object_or_404(Station, station_ID=station_id)
    available_slots = range(1, station.slots + 1)
    booked_slots = station.bookings.values_list('slot_number', flat=True)
    error_message = None
    
    if request.method == 'POST':
        form = BookingForm(request.POST, available_slots=available_slots, booked_slots=booked_slots)
        if form.is_valid():
            date = form.cleaned_data['date']
            start_time_str = form.cleaned_data['start_time']
            end_time_str = form.cleaned_data['end_time']
            phone_number = form.cleaned_data['phone_number']
            timezone_offset = form.cleaned_data['timezone_offset']

            # Convert start_time and end_time to datetime objects with correct timezone
            start_time = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.strptime(start_time_str, '%H:%M').time()))
            end_time = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.strptime(end_time_str, '%H:%M').time()))

            # Check if the selected time slot is already booked
            if station.bookings.filter(date=date, start_time__lt=end_time, end_time__gt=start_time).exists():
                error_message = 'This time slot is already booked. Please select another slot.'
            else:
                # Create a Booking instance
                booking = form.save(commit=False)
                booking.station = station
                booking.start_time = start_time
                booking.end_time = end_time
                booking.save()

                return redirect('booking_details')
    else:
        form = BookingForm(available_slots=available_slots, booked_slots=booked_slots)

    return render(request, 'users/booking.html', {'form': form, 'station': station, 'available_slots': available_slots, 'booked_slots': booked_slots, 'error_message': error_message})

def booking_details(request):
    # Adjust as needed to display booking details
    return render(request, "users/booking_details.html")