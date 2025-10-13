from django.contrib import admin

# Register your models here.
from .models import User, Hotel, Room, Booking, Review

admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Review)
