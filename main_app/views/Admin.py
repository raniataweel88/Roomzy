from django.shortcuts import render, redirect, get_object_or_404
from ..models import Hotel, Room, Booking, Review
from ..forms import HotelForm, RoomForm, BookingForm, ReviewForm

# ---- HOTEL CRUD ----

def hotel_create(request):
    form = HotelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hotel_list')
    return render(request, 'main_app/hotel_form.html', {'form': form})

def hotel_edit(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    form = HotelForm(request.POST or None, instance=hotel)
    if form.is_valid():
        form.save()
        return redirect('hotel_list')
    return render(request, 'main_app/hotel_form.html', {'form': form})

def hotel_delete(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    hotel.delete()
    return redirect('hotel_list')


# ---- ROOM CRUD ----
def room_create(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('hotel_list')
    return render(request, 'main_app/room_form.html', {'form': form})

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
