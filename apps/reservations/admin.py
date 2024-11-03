from django.contrib import admin
from apps.reservations.models import (Area, Rating, Reservation,
                                      Restaurant, Table, TableSchedule, Turn)

# Register your models here.

admin.site.register(Area)
admin.site.register(Rating)
admin.site.register(Reservation)
admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(TableSchedule)
admin.site.register(Turn)
