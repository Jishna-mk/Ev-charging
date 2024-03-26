from django.shortcuts import render,redirect
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout

from datetime import timedelta
from station_app.models import StationProfile
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


from station_app.models import Station,StationProfile
from users_app.models import Booking  ,UserProfile  

def dashboard(request):
    station = StationProfile.objects.all().order_by("-id")
    total_station = Station.objects.all().count()
    total_users = UserProfile.objects.all().count()
    total_book = Booking.objects.all().count()
    return render(request, "admin/dashboard.html", {"station": station, "total_station": total_station, "total_users": total_users, "total_book": total_book})



def all_bookings(request):
    user_bookings = Booking.objects.select_related('station').all()
    return render(request, "admin/booking.html", {'user_bookings': user_bookings})



def approvestation(request,s_id):
    station = User.objects.get(id = s_id)
    station.is_active = True
    station.save()
    messages.success(request,"Approved as Station")
    return redirect("dashboard")

def removestation(request, s_id):
    try:
        station = get_object_or_404(User, id=s_id)

        # Access related profile using the default related name (user_set)
        station_profile_set = station.stationprofile_set.all()

        # Assuming there is only one related profile, you can delete it
        if station_profile_set:
            station_profile_set[0].delete()

        # Delete the User instance
        station.delete()

        messages.success(request, "Removed Station")
    except Exception as e:
        # Print the exception for debugging
        print(f"Error removing station: {str(e)}")
        messages.error(request, "Error removing station")

    return redirect("dashboard")