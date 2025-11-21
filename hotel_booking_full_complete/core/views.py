from rest_framework import generics, status
from rest_framework.response import Response
from .models import Hotel, Booking
from .serializers import HotelSerializer, BookingSerializer

class HotelListView(generics.ListAPIView):
    queryset = Hotel.objects.filter(status='published')
    serializer_class = HotelSerializer

class HotelDetailView(generics.RetrieveAPIView):
    queryset = Hotel.objects.filter(status='published')
    serializer_class = HotelSerializer
    lookup_field = 'slug'

class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
