from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name="index"),
    path('signup/',views.signup,name="signup"),
    path('signin/',views.signin,name="signin"),
    path('viewpage/',views.viewpage,name="viewpage"),
    path('build-profile/', views.build_profile, name='build_profile'),
    path('station_profile/', views.station_profile, name='station_profile'),
    path('view-profile/<str:username>/', views.view_profile, name='view_profile'),
    path('view_details/<int:station_ID>/',views.view_details,name="view_details"),
    path('book-slot/<int:station_id>/', views.book_slot, name='book_slot'),
    path('booking-details/', views.booking_details, name='booking_details'),
    path('send_message/<int:id>', views.send_message, name="send_message"),
    path('view_messages/', views.view_messages, name="view_messages"),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

]