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
]