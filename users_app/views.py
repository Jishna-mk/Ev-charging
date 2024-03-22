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

def book_slot(request, station_id):
    station = get_object_or_404(Station, station_ID=station_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        start_time_str = request.POST.get('start_time')
        end_time_str = request.POST.get('end_time')
        phone_number = request.POST.get('phone_number')
        slots = request.POST.get('slots')  

        start_time = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.strptime(start_time_str, '%H:%M').time()))
        end_time = timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.strptime(end_time_str, '%H:%M').time()))

        if Booking.objects.filter(station=station, slots=slots,date=date, start_time__lt=end_time, end_time__gt=start_time).exists():
            error_message = 'This time slot is already booked. Please select another slot.'
            return render(request, 'viewdetails.html', {'station': station, 'error_message': error_message})
        
        booking = Booking(
            user=request.user,
            station=station,
            start_time=start_time,
            end_time=end_time,
            date=date,
            phone_number=phone_number,
            slots=slots  # Save the number of slots
        )
        booking.save()

        return redirect('booking_details')  # Redirect to the booking details page

    return render(request, 'users/user_booking.html', {'station': station})


def booking_details(request):
    return render(request,"users/booking_details.html")