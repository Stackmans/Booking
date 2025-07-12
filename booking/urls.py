from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    EventListCreateView,
    BookEventView,
    MyEventsView,
    MyBookingsView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("events/", EventListCreateView.as_view(), name="events"),
    path("events/<int:event_id>/book/", BookEventView.as_view(), name="book-event"),
    path("my/events/", MyEventsView.as_view(), name="my-events"),
    path("my/bookings/", MyBookingsView.as_view(), name="my-bookings"),
]
