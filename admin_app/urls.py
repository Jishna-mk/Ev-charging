from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_signin, name='admin_signin'),
    path('admin_signout/', views.admin_signout, name='admin_signout'),  # Corrected with trailing slash
    path('dashboard/', views.dashboard, name='dashboard'),
    path('approvestation/<int:s_id>/', views.approvestation, name='approvestation'),
]
