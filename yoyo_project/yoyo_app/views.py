from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from math import radians, cos, sin, asin, sqrt
import random
from datetime import timedelta
import pandas as pd

def profile(request) :
    return render(request,"yoyo_app/profile.html")
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
        min_budget = request.GET.get('min_budget', '100')
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
        print("No nearby cities found")
        return JsonResponse([], safe=False)
    
    # Get hotels that can accommodate the number of adults AND their prices within budget
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT hotel_id, price_per_night FROM room_type WHERE max_adults >= %s AND price_per_night BETWEEN %s AND %s", 
            [adults, min_budget, max_budget]
        )
        hotel_price_rows = cursor.fetchall()
    
    # Extract hotel IDs and create a price mapping
    hotel_ids = [row[0] for row in hotel_price_rows]
    price_map = {row[0]: row[1] for row in hotel_price_rows}  # {hotel_id: price_per_night}
    
    if not hotel_ids:
        # No hotels can accommodate this number of adults within budget
        print("No hotels can accommodate this number of adults within budget")
        return JsonResponse([], safe=False)
    
    # Concatenate both lists before the query
    combined_params = cities_res + hotel_ids

    print(f"cities_res: {cities_res}")
    print(f"hotel_ids: {hotel_ids}")
    
    # Create placeholders for both conditions
    placeholders_cities = ','.join(['%s'] * len(cities_res))
    placeholders_hotels = ','.join(['%s'] * len(hotel_ids))
    
    # Build star rating filter
    star_filter = ""
    if star_ratings:
        star_placeholders = ','.join(['%s'] * len(star_ratings))
        star_filter = f" AND star_rating IN ({star_placeholders})"
        combined_params = combined_params + star_ratings
    
    print(combined_params)
    # Query hotels that match location, capacity, budget, and star rating
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT id, name, slug, main_phone, description, star_rating FROM hotel WHERE address_id IN ({placeholders_cities}) AND id IN ({placeholders_hotels}){star_filter}",
            combined_params
        )
        hotels = cursor.fetchall()
    print(hotels)

    result = []
    for row in hotels:
        hotel_id, name, slug, main_phone, description, star_rating = row
        result.append({
            "hotel_id": hotel_id,
            "name": name,
            "slug": slug,
            "main_phone": main_phone,
            "description": description,
            "price_per_night": price_map.get(hotel_id, 0),  # Get price from the mapping
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
            "id": room_row[6]
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
        print(f'rooms: {rooms}')

    with connection.cursor() as cursor :
        cursor.execute("select r.user_id,u.user_name,r.hotel_id,r.rating,r.title,r.body, r.created_at from review as r inner join user as u on u.user_id = r.user_id and hotel_id = %s order by created_at desc;", [address_id])
        r = cursor.fetchall()
    
    reviews = []
    for review in r:
        reviews.append({
            "user_id": review[0],
            "user_name": review[1],
            "hotel_id": review[2],
            "rating": review[3],
            "title": review[4],
            "body": review[5],
            "created_at": review[6],
        })
    
    
    
    context = {
        "hotel": hotel,
        "rooms": rooms,
        "date": date,
        "adults": adults,
        "reviews": reviews,
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
                cursor.execute(
                    "INSERT INTO user (user_id,email,password_hash,role,is_active,user_name) VALUES (%s, %s, %s, %s, %s, %s)",
                    [user_id,email,hashed_password,"customer",1,username]
                )
                print(user_id)
            
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

# Bookings API
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
            cursor.execute("select b.id,b.user_id,b.checkin_date,b.checkout_date,b.total_amount,b.status,h.name,c.name from bookings as b inner join hotel as h on h.id = b.hotel_id inner join address as a on a.id = h.address_id inner join city as c on c.id = a.city_id where user_id = %s order by b.checkout_date desc", [user_id])
            
            bookings = cursor.fetchall()
        
        # Format the results
        result = []
        for booking in bookings:
            result.append({
                'id': booking[0],
                'name' : booking[6],
                'location': booking[7],
                'checkin': str(booking[2]),
                'checkout': str(booking[3]),
                'price': f'₹{booking[4]}',
                'status': booking[5]
            })
        
        print(result)
        
        return JsonResponse(result, safe=False)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



    from django.shortcuts import render
from django.http import Http404
from django.db import connection

def payment(request, hotel_id, room_id, adults):
    # GET query params
    date = request.GET.get('date', '')
    hotel_name = request.GET.get('hotelName', '')

    # -----------------------------------------
    # FETCH ROOM DETAILS
    # -----------------------------------------
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.id, r.hotel_id, r.code, r.name, r.description, 
                   r.max_adults, r.price_per_night, h.name
            FROM room_type AS r 
            INNER JOIN hotel AS h ON r.hotel_id = h.id 
            WHERE r.id = %s AND r.hotel_id = %s
        """, [room_id, hotel_id])
        row = cursor.fetchone()

    if not row:
        raise Http404("Room not found")

    # -----------------------------------------
    # FETCH EXISTING BOOKINGS → BLOCKED DATES
    # -----------------------------------------
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT checkin_date, checkout_date 
            FROM bookings 
            WHERE hotel_id = %s
        """, [hotel_id])
        bookings = cursor.fetchall()

    # Important rule:
    # Block all dates from checkin → checkout - 1
    blockedDates = {
        d.strftime("%Y-%m-%d")
        for checkin, checkout in bookings
        for d in pd.date_range(start=checkin, end=checkout - timedelta(days=1), freq='D')
    }

    print("Blocked Dates:", blockedDates)

    # -----------------------------------------
    # BUILD ROOM DICT
    # -----------------------------------------
    room = {
        "id": row[0],
        "hotel_id": row[1],
        "code": row[2],
        "room_type_name": row[3],
        "description": row[4],
        "max_adults": row[5],
        "price_per_night": row[6],
        "hotel_name": row[7],
        "taxes": (random.randint(1, 3) / 10) * int(row[6]),
        "discount": (random.randint(1, 3) / 10) * int(row[6]),
    }

    # -----------------------------------------
    # PASS CONTEXT
    # -----------------------------------------
    context = {
        "room": room,
        "date": date,
        "adults": adults,
        "hotel_name": hotel_name,
        "blockedDates": list(blockedDates),   # <-- list() to make safe for template
    }

    return render(request, "yoyo_app/payment.html", context)

def successfull_payment(request,hotel_id,room_id):

    user_id = request.session.get('user_id') 
    if not user_id:
        return redirect('login') 

    checkin = request.GET.get('checkin') 
    checkout = request.GET.get('checkout') 
    hotel_name = request.GET.get('hotelName')
    room_type = request.GET.get('room_type')
    total_amount = request.GET.get('total_amount')
    adults = request.GET.get('adults')
    booking_reference = random.randint(100000, 999999)
    currency = random.choice(['INR', 'USD', 'EUR','GBP','AUD','CAD','CHF','CNY','HKD','NZD','SGD','ZAR','MXN','BRL','JPY','KRW','THB','PHP','IDR','MYR','VND'])
    status = 'confirmed'

    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO bookings (user_id, hotel_id,booking_reference, checkin_date, checkout_date,total_amount,currency,status) VALUES (%s, %s, %s, %s, %s, %s,%s,%s)",
            [user_id, hotel_id, booking_reference, checkin, checkout, total_amount,currency,status]
        )   
    
    booking_id = cursor.lastrowid
    with connection.cursor() as cursor:
        cursor.execute(
            "call update_inventory(%s,%s,%s);"  ,[hotel_id,room_id,adults]
        )
    
    context = {
        "hotel_id": hotel_id,
        "room_id": room_id,
        "user_id": user_id,
        "checkin": checkin,
        "checkout": checkout,
        "adults": adults,
        "hotel_name": hotel_name,
        "room_type": room_type,
        "total_amount": total_amount,
    }
    return render(request, "yoyo_app/successfull_payment.html",context)

    