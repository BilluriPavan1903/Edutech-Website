from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .db import reg_collection  # ✅ Ensure your MongoDB collection is imported correctly
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect



def signup(request):
    return render(request, 'signup.html')





@csrf_exempt
def signup_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password or not email:
            return JsonResponse({'success': False, 'message': 'All fields are required.'})

        if reg_collection.find_one({'email': email}):
            return JsonResponse({'success': False, 'message': 'Email already registered.'})

        if reg_collection.find_one({'username': username}):
            return JsonResponse({'success': False, 'message': 'Username already exists.'})

        reg_collection.insert_one({
            'username': username,
            'password': password,
            'email': email
        })

        return JsonResponse({'success': True, 'message': 'User registered successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



 
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'success': False, 'message': 'All fields are required.'})

        user = reg_collection.find_one({'username': username})
        if not user:
            return JsonResponse({'success': False, 'message': 'Username does not exist.'})
        if user['password'] != password:
            return JsonResponse({'success': False, 'message': 'Incorrect password.'})

        request.session['username'] = username  # ✅ Session storage
        return JsonResponse({'success': True, 'message': 'Login successful.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def home(request):
    username = request.session.get('username')
    return render(request, 'home.html', {'username': username})



def login(request):
    return render(request, 'login.html')

def get_username(request):
    return JsonResponse({'username': request.user.username})


