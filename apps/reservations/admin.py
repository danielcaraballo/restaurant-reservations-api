from django.contrib import admin
from .models import (Area, Customer, Rating, Reservation, Restaurant, Table, TableAvailability, Turn)

# Register your models here.
admin.site.register(Area)
admin.site.register(Customer)
admin.site.register(Rating)
admin.site.register(Reservation)
admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(TableAvailability)
admin.site.register(Turn)