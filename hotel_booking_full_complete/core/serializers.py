from rest_framework import serializers
from .models import Hotel, HotelPhoto, RoomType, Booking, BookingRoom

class HotelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPhoto
        fields = ['url','caption','order']

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ['id','code','name','max_adults','max_children','description']

class HotelSerializer(serializers.ModelSerializer):
    photos = HotelPhotoSerializer(many=True, read_only=True)
    room_types = RoomTypeSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = ['id','name','slug','star_rating','main_phone','status','photos','room_types']

class BookingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRoom
        fields = ['room_type','rate_plan','price_per_night']

class BookingSerializer(serializers.ModelSerializer):
    rooms = BookingRoomSerializer(many=True)
    class Meta:
        model = Booking
        fields = ['id','booking_reference','hotel','checkin_date','checkout_date','total_amount','currency','status','rooms']

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms', [])
        booking = Booking.objects.create(**validated_data)
        for r in rooms_data:
            BookingRoom.objects.create(booking=booking, **r)
        return booking
