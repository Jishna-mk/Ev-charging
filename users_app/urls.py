from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name="index"),
    path('signin/',views.signin,name="signin"),
    path('signin/',views.signin,name="signin"),
    path('viewpage/',views.viewpage,name="viewpage"),
]