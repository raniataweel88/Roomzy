
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Hotel, Room, Booking, Review
from .forms import BookingForm, ReviewForm, HotelForm, RoomForm
from django.contrib.auth.forms import UserCreationForm

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

# Register
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

# Book a room
@login_required
def booking_create(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.status = "Pending"
            booking.save()
            return redirect("my_bookings")
    else:
        form = BookingForm()
    return render(request, "booking_form.html", {"form": form, "room": room})

# Cancel booking
@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect("my_bookings")

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
            form.save()
            return redirect('hotel_list')
    else:
        form = HotelForm()
    return render(request, 'registerHotel.html', {'form': form})

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
