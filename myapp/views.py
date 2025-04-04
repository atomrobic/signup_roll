from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from .models import Nurse, Doctor, Patient

User = get_user_model()  # Fetch the custom user model if defined

def signup(request):
    if request.method == "POST":
        # Retrieve common fields
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        place = request.POST.get('place')
        dob = request.POST.get('dob')
        user_type = request.POST.get('user_type')

        # Print common fields for debugging
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

            # Handle user-type-specific fields
            if user_type == 'nurse':
                print("nurse")
                nurse_phone = request.POST.get('nurse_phone')
                print(nurse_phone,"phone nurse")

                shift = request.POST.get('shift')
                print(shift ," nurse shift ")

                specialization = request.POST.get('specialization')
                print(specialization ,"specification  ")

                experience = request.POST.get('experience')
                print( experience  ," experience ")

                certificate = request.FILES.get('certificate')
                print(  certificate  ,"  certificate ")


                if not nurse_phone or not shift:
                    messages.error(request, "Phone number and shift are required for nurses.")
                    return redirect('signup')

                Nurse.objects.create(
                    user=user,
                    phone_number=nurse_phone,
                    shift=shift,
                    specialization=specialization,
                    experience=experience,
                    certificate=certificate
                )

            elif user_type == 'doctor':
                doctor_phone = request.POST.get('doctor_phone')
                specialization = request.POST.get('specialization')
                experience = request.POST.get('experience')
                certificate_file = request.FILES.get('certificate_file')

                Doctor.objects.create(
                    user=user,
                    specialization=specialization,
                    experience=experience,
                    phone_number=doctor_phone,
                    certificate_files=certificate_file
                )

            elif user_type == 'patient':
                patient_phone = request.POST.get('patient_phone')
                Patient.objects.create(user=user, phone_number=patient_phone)

            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    # Render the signup form if the request method is not POST
    return render(request, 'signup.html')
