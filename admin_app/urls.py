from django.urls import path
from .import views



urlpatterns=[
    path('', views.admin_signin, name='admin_signin'),
    path('dashboard/',views.dashboard,name="dashboard"),
   
    path('signout',views.admin_signout,name='admin_signout'),
   
    
]