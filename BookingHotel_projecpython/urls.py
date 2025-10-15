"""
URL configuration for BookingHotel_projecpython project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project/urls.py
from django.contrib import admin
from django.urls import path, include
from main_app import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.hotel_list, name='home'),           
    path('hotels/', views.hotel_list, name='hotel_list'),
     path("hotel/add/", views.hotel_create, name="hotel_create"),
    path('hotel/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('register/', views.register_view, name='register_view'),
    path("login/user/", views.user_login_view, name="user_login_view"),
    path("login/hotel/", views.hotel_login_view, name="hotel_login_view"),   
     path('logout/', views.logout_view, name='logout_view'),
        path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('hotel/<int:hotel_id>/admin/', views.hotel_detail_Admin, name='hotel_detail_Admin'),
 path('hotel/<int:hotel_id>/edit/', views.hotel_edit, name='hotel_edit'), 
    path('hotel/<int:hotel_id>/room/add/', views.room_create, name='room_create'),
  path('hotel/<int:hotel_id>/room/<int:room_id>/createBooking/', views.create_booking, name='create_booking'),
path('hotel/<int:hotel_id>/review/add/', views.review_create, name='review_create'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)