
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
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Doctor
from .utils import send_status_email


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
            print("if condition check")
            messages.error(request, "Username already exists.")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            print("all ready exit")

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
            print(user,"wow")
            # Handle user-type specific fields
            if user_type == 'nurse':
                print(user_type,"nurse" )
                # Use 'nurse_phone' from the form; pass it to the Nurse model as phone_number.
                nurse_phone = request.POST.get('nurse_phone')
                print(nurse_phone,'this is nurse ph')
                shift = request.POST.get('shift')
                Nurse.objects.create(user=user, phone_number=nurse_phone, shift=shift)

            elif user_type == 'doctor':
                # Use 'doctor_phone' from the form; pass it to the Doctor model as phone_number.
                doctor_phone = request.POST.get('doctor_phone')
                print(doctor_phone,"hi ph")

                specification = request.POST.get('specification')
                print(specification,"hi spec")
                
                experience = request.POST.get('experience')
                print(experience,"hi exp")

                certificate_file = request.FILES.get('certificate_file')
                print(certificate_file,"hi cert")

                # If your model field is named 'certificate_files', pass it as such.
                Doctor.objects.create(
                    user=user,
                    specification=specification,
                    experience=experience,
                    phone_number=doctor_phone,
                    certificate_files=certificate_file
                )

            elif user_type == 'patient':
                # Use 'patient_phone' from the form; pass it to the Patient model as phone_number.
                patient_phone = request.POST.get('patient_phone')
                print(patient_phone,'this is pat ph')

                Patient.objects.create(user=user, phone_number=patient_phone)

            messages.success(request, "Signup successful! Please log in.")
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('signup')

    # If the request method is not POST, render the signup form.
    return render(request, 'signup.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('approve_doctors')  
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')


from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
import os
from .models import Doctor
from .utils import send_status_email

def doctor_applications(request, action=None, application_id=None):
    if action == 'download' and application_id:
        # Handle the download certificate logic
        application = get_object_or_404(Doctor, id=application_id)
        
        if not application.certificate_file:
            raise Http404("Certificate file not found")

        file_path = application.certificate_file.path
        if not os.path.exists(file_path):
            raise Http404("File not found")

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response

    # Render doctor applications page
    doctor_applications = Doctor.objects.all()
    return render(request, 'approve_doctors.html', {'doctor_applications': doctor_applications})




def update_status(request, application_id, status):
    # Fetch the doctor application or return a 404
    application = get_object_or_404(Doctor, id=application_id)

    # Update application status and approval flag
    application.is_approved = (status == 'approved')  # Set approval status based on the action (approve/reject)
    application.save()

    # Email subject and message
    subject = f"Your Doctor Application has been {status.capitalize()}"
    message = (f"Hello {application.user.first_name},\n\n"
               f"Your application for {application.specification} has been {status.lower()}.\n\n"
               "Thanks for your time!")

    # Send status update email
    send_status_email(application.user.email, subject, message)

    # Display success message
    messages.success(request, f"Application {status.lower()} and email notification sent.")
    return redirect('approve_doctors')


def remove_doctor_application(request, application_id):
    # Fetch the doctor application or return a 404
    application = get_object_or_404(Doctor, id=application_id)
    
    # Mark the application as inactive instead of deleting
    application.is_active = False
    application.save()
    
    # Show a success message
    messages.success(request, "Doctor application successfully removed from the table view.")
    return redirect('approve_doctors')



def docters_views(request):
    # Fetch only approved doctors
    approved_doctors = Doctor.objects.filter(is_approved=True)
    return render(request, 'doctors_view.html', {'approved_doctors': approved_doctors})



def deactivate_doctor(request, application_id):
    doctor = get_object_or_404(Doctor,id=application_id)
    

    # Deactivate the doctor by setting is_approved to False
    doctor.is_approved = False
    doctor.status = "Deactivated"
    doctor.save()

    messages.success(request, f"Doctor {doctor.user} has been deactivated.")
    return redirect('doctors_view')

# def doctor_applications(request):
#     # Only show doctors pending approval
#     doctor_applications = Doctor.objects.filter(is_approved=False)  # Change the filter if necessary
#     return render(request, 'approve_doctors.html', {'doctor_applications': doctor_applications})
