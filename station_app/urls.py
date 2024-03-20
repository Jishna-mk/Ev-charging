from django.urls import path
from .import views

urlpatterns=[
    path('stationsignup/',views.stationsignup,name="stationsignup"),
    path('stationsignin/',views.stationsignin,name="stationsignin"),
    path('stationsignout/',views.stationsignout,name="stationsignout"),
    path('deatils/',views.details,name="details"),
    
    path('add/', views.add_station, name='add_station'),
    path('view/', views.view_stations, name='view_stations'),
    path('edit/<int:station_id>/', views.edit_station, name='edit_station'),
    path('delete/<int:pk>/', views.delete_station, name='delete_station'),
    path('profiles/',views.station_profiles,name="station_profiles"),
]