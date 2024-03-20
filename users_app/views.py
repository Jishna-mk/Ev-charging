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