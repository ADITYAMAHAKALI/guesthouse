from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('reserve/', views.reserve, name='reserve'), 
    path('reservesuccess/<int:pk>', views.reserve_success, name='reserve_success'), 
    path('rooms/', views.RoomListView.as_view(), name='rooms'),# List of Rooms
    path('room/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),  # Detail of each room
    path('roomstype/', views.RoomTypeListView.as_view(), name='roomsType'),# List of Rooms
    path('eachroomtype/<int:pk>', views.eachroomtype, name='eachroomtype'), 
    path('reservations/', views.ReservationListView.as_view(), name='reservations'),  # List of Reservations
    path('reservation/<str:pk>', views.ReservationDetailView.as_view(), name='reservation-detail'),
    path('customer/<int:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),  # Detail of each customer
    path('staff/<str:pk>', views.StaffDetailView.as_view(), name='staff-detail'),  # Detail of staff
    path('profile/', login_required(views.ProfileView.as_view()), name='profile'),
    path('guests/', views.GuestListView.as_view(), name='guest-list'),
    path('about/',views.about,name='about'),
]