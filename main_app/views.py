
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  
from .models import Hotel, Room, Booking, Review
from .forms import BookingForm, ReviewForm, HotelForm, RoomForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout,authenticate
from django.contrib import messages
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django import forms

# View all hotels
def hotel_list(request):
    hotels = Hotel.objects.all()
    return render(request, "hotels.html", {"hotels": hotels})

def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.all()  
    return render(request, 'hotel_detail.html', {'hotel': hotel, 'rooms': rooms})


 
   
# View room deta ils
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, "room_detail.html", {"room": room})

# Search rooms
def room_search(request):
    city = request.GET.get('city')
    check_in = request.GET.get('check_in')
    rooms = Room.objects.filter(hotel__city__icontains=city, is_available=True)
    return render(request, "room_search.html", {"rooms": rooms})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, "Account created successfully!")
            return redirect("hotel_list")
    else:
        form = UserCreationForm()
    return render(request, "createAccount.html", {"form": form})

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User  
def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('hotel_list')
        else:
            messages.error(request, 'Incorrect username or password')

    return render(request, 'login_user.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect("user_login_view")


from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking, Room
from .forms import BookingForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Hotel, Room, Booking

from .models import Hotel, Room, Booking
from .forms import BookingForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Room, Booking
from django.contrib.auth import get_user_model


from django.contrib.auth import get_user

def create_booking(request, hotel_id, room_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            # تحويل SimpleLazyObject إلى User instance
            booking.user = get_user(request)
            booking.room = room
            booking.save()
            return redirect('my_bookings')
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {
        'form': form,
        'hotel': hotel,
        'room': room
    })

def hotel_login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            hotel = Hotel.objects.get(email=email, password=password)
            request.session["hotel_id"] = hotel.id
            messages.success(request, f"Welcome back, {hotel.name}!")
            return redirect("hotel_detail_Admin", hotel_id=hotel.id)
        except Hotel.DoesNotExist:
            messages.error(request, "Invalid email or password")
    
    return render(request, "login_hotel.html")

# Cancel booking
@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect("my_bookings")

def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')  
    return render(request, "myBooking.html", {"bookings": bookings})

# Leave review
@login_required
def review_create(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.room = room
            review.save()
            return redirect("room_detail", room_id=room.id)
    else:
        form = ReviewForm()
    return render(request, "review_form.html", {"form": form, "room": room})



#-----admain CRUD ----


def hotel_create(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
              hotel = form.save()
              return redirect('hotel_detail_Admin', hotel_id=hotel.id)
    else:
        form = HotelForm()
    return render(request, 'registerHotel.html', {'form': form})

def hotel_detail_Admin(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = hotel.rooms.all()  
    return render(request, 'hotel_detailAdmin.html', {'hotel': hotel, 'rooms': rooms})

def hotel_edit(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            return redirect('hotel_detail_Admin', hotel_id=hotel.id)
    else:
        form = HotelForm(instance=hotel)
    return render(request, 'hotel_edit.html', {'form': form, 'hotel': hotel})


def hotel_delete(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    hotel.delete()
    return redirect('hotel_list')


# ---- ROOM CRUD ----

def admin_required(user):
    return user.is_staff

def room_create(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect('hotel_detail_Admin', hotel_id=hotel.id)
    else:
        form = RoomForm()
    return render(request, 'room_create.html', {'form': form, 'hotel': hotel})


def room_edit(request, id):
    room = get_object_or_404(Room, id=id)
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return redirect('hotel_list')
    return render(request, 'main_app/room_form.html', {'form': form})

def room_delete(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    return redirect('hotel_list')


# ---- BOOKINGS ADMIN ----
def booking_list_admin(request):
    bookings = Booking.objects.select_related('room', 'room__hotel').all()
    return render(request, 'main_app/bookings_admin.html', {'bookings': bookings})

def booking_confirm(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.is_confirmed = True
    booking.save()
    return redirect('booking_list_admin')


# ---- REVIEWS ADMIN ----
def review_list_admin(request):
    reviews = Review.objects.select_related('hotel').all()
    return render(request, 'main_app/reviews_admin.html', {'reviews': reviews})

def review_delete(request, id):
    review = get_object_or_404(Review, id=id)
    review.delete()
    return redirect('review_list_admin')
