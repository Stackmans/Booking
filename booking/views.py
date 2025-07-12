from rest_framework import serializers
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User, Event, Booking
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    EventSerializer,
    BookingSerializer
)
from django.db.models import Sum


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_staff:
            raise PermissionDenied("Only staff can create events.")
        serializer.save(owner=user)


class BookEventView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        event_id = self.kwargs.get("event_id")
        user = request.user

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Подію не знайдено"}, status=status.HTTP_404_NOT_FOUND)

        if Booking.objects.filter(user=user, event=event).exists():
            return Response({"error": "Ви вже забронювали цю подію"}, status=status.HTTP_400_BAD_REQUEST)

        booked_seats = Booking.objects.filter(event=event).aggregate(total=Sum("seats_booked"))["total"] or 0
        available_seats = event.max_seats - booked_seats

        seats_requested = request.data.get("seats_booked")
        try:
            seats_requested = int(seats_requested)
        except (ValueError, TypeError):
            return Response({"error": "Недійсне значення для seats_booked. Має бути ціле число."}, status=status.HTTP_400_BAD_REQUEST)

        if not seats_requested or seats_requested <= 0 or seats_requested > available_seats:
            return Response({"error": "Недостатньо доступних місць або запитана недійсна кількість"}, status=status.HTTP_400_BAD_REQUEST)


        booking = Booking.objects.create(user=user, event=event, seats_booked=seats_requested)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


class MyEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(owner=self.request.user)


class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
