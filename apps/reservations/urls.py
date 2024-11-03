from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AreaViewSet, RatingViewSet,
                    ReservationViewSet, RestaurantViewSet,
                    TableViewSet, TableScheduleViewSet, TurnViewSet)

router = DefaultRouter()
router.register(r'areas', AreaViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'tables', TableViewSet)
router.register(r'tables-schedule', TableScheduleViewSet)
router.register(r'turns', TurnViewSet)

urlpatterns = router.urls
