from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.db import connection
from math import radians, cos, sin, asin, sqrt

# Create your views here.
def home (request) :
    return render(request,"yoyo_app/home.html")

def hotels_near_location(request) :
    try:
        lat = float(request.GET.get('lat'))
        lon = float(request.GET.get('lon'))
        radius_km = float(request.GET.get('radius', 5))
        # Get date and adults from request parameters
        date = request.GET.get('date', '') 
        adults = request.GET.get('adults', '2')
        
        # Get filter parameters
        min_budget = request.GET.get('min_budget', '1000')
        max_budget = request.GET.get('max_budget', '15000')
        star_ratings = request.GET.getlist('star_ratings[]')  # List of selected star ratings
        
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid or missing lat/lon"}, status=400)
    
    with connection.cursor() as cursor :
        cursor.execute("select region_id,lat,lng from city")
        cities = cursor.fetchall()
    
    cities_res = []
    for row in cities :
        region_id,hlat,hlng = row
        hlat = float(hlat)
        hlng = float(hlng)
        dist = haversine(lat,lon,hlat,hlng)
        if dist <= radius_km:
            cities_res.append(region_id)
    
    if not cities_res:
        # No nearby cities found; return empty list early
        return JsonResponse([], safe=False)
    
    # Get hotels that can accommodate the number of adults AND their prices within budget
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT DISTINCT hotel_id, price_per_night FROM room_type WHERE max_adults >= %s AND price_per_night BETWEEN %s AND %s", 
            [adults, min_budget, max_budget]
        )
        hotel_price_rows = cursor.fetchall()
    
    # Extract hotel IDs and create a price mapping
    hotel_ids = [row[0] for row in hotel_price_rows]
    price_map = {row[0]: row[1] for row in hotel_price_rows}  # {hotel_id: price_per_night}
    
    if not hotel_ids:
        # No hotels can accommodate this number of adults within budget
        return JsonResponse([], safe=False)
    
    # Concatenate both lists before the query
    combined_params = cities_res + hotel_ids
    
    # Create placeholders for both conditions
    placeholders_cities = ','.join(['%s'] * len(cities_res))
    placeholders_hotels = ','.join(['%s'] * len(hotel_ids))
    
    # Build star rating filter
    star_filter = ""
    if star_ratings:
        star_placeholders = ','.join(['%s'] * len(star_ratings))
        star_filter = f" AND star_rating IN ({star_placeholders})"
        combined_params = combined_params + star_ratings
    
    # Query hotels that match location, capacity, budget, and star rating
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT address_id, name, slug, main_phone, description, star_rating FROM hotel WHERE address_id IN ({placeholders_cities}) AND address_id IN ({placeholders_hotels}){star_filter}",
            combined_params
        )
        hotels = cursor.fetchall()

    result = []
    for row in hotels:
        address_id, name, slug, main_phone, description, star_rating = row
        result.append({
            "address_id": address_id,
            "name": name,
            "slug": slug,
            "main_phone": main_phone,
            "description": description,
            "price_per_night": price_map.get(address_id, 0),  # Get price from the mapping
            "date": date,
            "adults": adults,
            "star_rating": star_rating,
        }) 

    return JsonResponse(result, safe=False)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c


def hotel_detail(request, address_id):
    """
    Display hotel details and check room availability
    """
    try:
        # Get search parameters from query string
        date = request.GET.get('date', '')
        adults = int(request.GET.get('adults', '2'))
    except (TypeError, ValueError):
        adults = 2
    
    # Fetch hotel information
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT address_id, name, slug, main_phone, description, star_rating FROM hotel WHERE address_id = %s",
            [address_id]
        )
        hotel_row = cursor.fetchone()
    
    if not hotel_row:
        return render(request, "yoyo_app/hotel_detail.html", {
            "error": "Hotel not found",
            "date": date,
            "adults": adults
        })
    
    # Extract hotel details
    hotel = {
        "address_id": hotel_row[0],
        "name": hotel_row[1],
        "slug": hotel_row[2],
        "main_phone": hotel_row[3],
        "description": hotel_row[4],
        "star_rating": hotel_row[5],
    }
    
    # Fetch all room types for this hotel
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT hotel_id,code,name, description, max_adults, price_per_night 
            FROM room_type 
            WHERE hotel_id = %s
            ORDER BY price_per_night ASC
            """,
            [address_id]
        )
        room_rows = cursor.fetchall()
    
    rooms = []
    for room_row in room_rows:
        room = {
            "hotel_id": room_row[0],
            "code": room_row[1],
            "room_type_name": room_row[2],  # Changed from "name" to "room_type_name" to match template
            "description": room_row[3],
            "max_adults": room_row[4],
            "price_per_night": room_row[5],
            "available": False,  # Default to unavailable
            "can_accommodate": int(room_row[4]) >= adults  # Check if room can fit the adults (using max_adults, not description!)
        }
        
        # Check availability for this room type on the specified date
        if date:
            with connection.cursor() as cursor:
                # Check if there are any available rooms of this type on the date
                # Assuming available rooms = total rooms - booked rooms
                # For now, we'll mark rooms as available if they can accommodate the adults
                # You can enhance this with actual booking table queries
                room["available"] = room["can_accommodate"]
        else:
            room["available"] = room["can_accommodate"]
        
        rooms.append(room)
    
    context = {
        "hotel": hotel,
        "rooms": rooms,
        "date": date,
        "adults": adults,
    }
    
    return render(request, "yoyo_app/hotel_detail.html", context)


