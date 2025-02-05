
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Nurse, Doctor, Patient,Profile
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.dateparse import parse_date
import json
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

User = get_user_model()  # Fetch the custom user model if defined

def signup(request):
    if request.method == "POST":
        # Retrieve common fields
        username   = request.POST.get('username')
        password   = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        place      = request.POST.get('place')
        dob        = request.POST.get('dob')
        user_type  = request.POST.get('user_type')
        
        # Print common fields to the terminal for debugging
        print("Username:", username)
        print("Password:", password)
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Email:", email)
        print("Place:", place)
        print("Date of Birth:", dob)
        print("User Type:", user_type)

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        try:
            # Create the user instance
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                place=place,
                dob=dob,
                user_type=user_type,
            )
            user.save()  # Explicitly save the user

            # Handle user-type specific fields
            if user_type == 'nurse':
                print('nurse')
                # Use 'nurse_phone' from the form; pass it to the Nurse model as phone_number.
                nurse_phone = request.POST.get('nurse_phone')
                print('nurse_phone')
                shift = request.POST.get('shift')
                Nurse.objects.create(user=user, phone_number=nurse_phone, shift=shift)

            elif user_type == 'doctor':
                # Use 'doctor_phone' from the form; pass it to the Doctor model as phone_number.
                doctor_phone = request.POST.get('doctor_phone')
                specialization = request.POST.get('specification')
                experience = request.POST.get('experience')
                certificate_file = request.FILES.get('certificate_file')
                # If your model field is named 'certificate_files', pass it as such.
                Doctor.objects.create(
                    user=user,
                    specialization=specialization,
                    experience=experience,
                    phone_number=doctor_phone,
                    certificate_files=certificate_file
                )

            elif user_type == 'patient':
                # Use 'patient_phone' from the form; pass it to the Patient model as phone_number.
                patient_phone = request.POST.get('patient_phone')
                Patient.objects.create(user=user, phone_number=patient_phone)

            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    # If the request method is not POST, render the signup form.
    return render(request, 'signup.html')

# def login_user(request):=====
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')  
#         else:
#             messages.error(request, "Invalid username or password.")
#             return redirect('login')

#     return render(request, 'login.html')

# def logout_user(request):
#     logout(request)
#     return redirect('login')from myapp.models import Profile

