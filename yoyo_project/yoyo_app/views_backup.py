from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from math import radians, cos, sin, asin, sqrt

# Create your views here.
def home (request) :
    return render(request,"yoyo_app/home.html")

def login(request) :
    return render(request,"yoyo_app/login.html") 

def register(request) :
    return render(request,"yoyo_app/register.html") 

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
    
    with connection.cursor() as cursor:
        cursor.execute("select region_id,lat,lng from city")
        cities = cursor.fetchall()
    
    cities_res = []
    for row in cities:
        region_id, hlat, hlng = row
        hlat = float(hlat)
        hlng = float(hlng)
        dist = haversine(lat, lon, hlat, hlng)
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
            SELECT hotel_id,code,name, description, max_adults, price_per_night,id
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
            "can_accommodate": int(room_row[4]) >= adults,  # Check if room can fit the adults (using max_adults, not description!)
            "room_type_id": room_row[6]
        }
        
        # Check availability for this room type on the specified date
        if date:
            with connection.cursor() as cursor:
                # Check if there are any available rooms of this type on the date
                # Assuming available rooms = total rooms - booked rooms
                # For now, we'll mark rooms as available if they can accommodate the adults
                # You can enhance this with actual booking table queries
                #select * from hotel as h inner join inventory as i on h.id = i.hotel_id where (i.available_count-i.closed) > 4;
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

# Register user
@csrf_exempt
def register_user(request):
    """
    Handle user registration via POST request with JSON data
    """
    if request.method == 'POST':
        try:
            import json
            from django.contrib.auth.models import User
            from django.contrib.auth.hashers import make_password
            
            # Parse JSON data from request body
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            first_name = data.get('first_name', '').strip()
            last_name = data.get('last_name', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            # Validate input
            if not username or not first_name or not last_name or not email or not password:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            if len(password) < 6:
                return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)
            
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already registered'}, status=400)
            
            # Check if username (email) already exists
            if User.objects.filter(username=email).exists():
                return JsonResponse({'error': 'Email already registered'}, status=400)
            
            # Hash the password using Django's password hasher
            hashed_password = make_password(password)
            
            # Create new user with hashed password
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO auth_user (password, username, first_name, last_name, email, is_active, is_staff, is_superuser, date_joined) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())",
                    [hashed_password, username, first_name, last_name, email, 1, 0, 0]
                )
                # Get the ID of the newly created user
                cursor.execute("SELECT LAST_INSERT_ID()")
                user_id = cursor.fetchone()[0]
            
            return JsonResponse({
                'success': True,
                'message': 'Registration successful',
                'user_id': user_id
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# Login user
@csrf_exempt
def login_user(request):
    """
    Handle user login via POST request with JSON data
    """
    if request.method == 'POST':
        try:
            import json
            
            # Parse JSON data from request body
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            # Validate input
            if not email or not password:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            # Authenticate user
            user = authenticate(username=email, password=password)
            
            if user is not None:
                # Set user in session
                request.session['user_id'] = user.id
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'user_id': user.id
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

def logout_user(request):
    """
    Handle user logout
    """
    if request.method == 'POST':
        try:
            # Clear user session
            request.session.flush()
            return JsonResponse({'success': True, 'message': 'Logout successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

def bookings_history(request):
    """
    Display booking history page
    """
    # Get user_id from session or query parameter
    user_id = request.session.get('user_id') or request.GET.get('user_id')
    
    context = {
        'user_id': user_id if user_id else ''
    }
    
    return render(request, 'yoyo_app/bookings_history.html', context)

@csrf_exempt
def get_bookings_api(request):
    """
    API endpoint to fetch bookings for a user from database
    """
    user_id = request.GET.get('user_id')
    
    if not user_id:
        return JsonResponse({'error': 'User ID required'}, status=400)
    
    try:
        # Fetch bookings from database
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    b.id,
                    h.name as hotel_name,
                    c.name as location,
                    b.checkin_date,
                    b.checkout_date,
                    b.total_amount,
                    b.status
                FROM bookings as b
                INNER JOIN hotel as h ON b.hotel_id = h.address_id
                LEFT JOIN city as c ON h.address_id = c.region_id
                WHERE b.user_id = %s
                ORDER BY b.checkin_date DESC
            """, [user_id])
            
            bookings = cursor.fetchall()
        
        # Format the results
        result = []
        for booking in bookings:
            result.append({
                'id': booking[0],
                'hotel': booking[1],
                'location': booking[2] if booking[2] else 'N/A',
                'checkin': str(booking[3]),
                'checkout': str(booking[4]),
                'price': f'₹{booking[5]}',
                'status': booking[6]
            })
        
        return JsonResponse(result, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
