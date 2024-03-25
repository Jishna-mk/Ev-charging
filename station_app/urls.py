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
    path('bookings/', views.bookings, name='bookings'),
    path('view_company_messages/', views.view_company_messages, name="view_company_messages"),
    path('reply_message/<int:id>', views.reply_message, name="reply_message"),
    path('send_message_to_user/', views.send_message_to_user, name='send_message_to_user'),
]