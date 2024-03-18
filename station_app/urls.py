from django.urls import path
from .import views

urlpatterns=[
    path('stationsignup/',views.stationsignup,name="stationsignup"),
    path('stationsignin/',views.stationsignin,name="stationsignin"),
    path('stationsignout/',views.stationsignout,name="stationsignout"),
    path('deatils/',views.details,name="details"),
]