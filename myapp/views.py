from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, PersonalDetails, UserType  # Use relative imports
from django.contrib.auth.hashers import make_password

def signup(request):
    if request.method == "POST":
        # Collect form data
        username = request.POST.get('username')
        print(f"Username: {username}")  # Debugging the value of username
        password = request.POST.get('password')
        print(f"Password: {password}")  # Debugging the value of password
        confirm_password = request.POST.get('confirm_password')
        print(f"Confirm Password: {confirm_password}")  # Debugging the value of confirm_password
        first_name = request.POST.get('first_name')
        print(f"First Name: {first_name}")  # Debugging the value of first_name
        last_name = request.POST.get('last_name')
        print(f"Last Name: {last_name}")  # Debugging the value of last_name
        email = request.POST.get('email')
        print(f"Email: {email}")  # Debugging the value of email
        place = request.POST.get('place')
        print(f"Place: {place}")  # Debugging the value of place
        dob = request.POST.get('dob')
        print(f"DOB: {dob}")  # Debugging the value of dob
        user_type = request.POST.get('user_type')
        print(f"User Type: {user_type}")  # Debugging the value of user_type

        # Validate password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Check for existing users
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup.html')

        # Create and save user
        user = User.objects.create(
            username=username,
            password=make_password(password),
            email=email
        )
        print(f"Created user: {user}")  # Debugging the user created

        # Save personal details
        personal_details = PersonalDetails.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            place=place,
            dob=dob
        )
        print(f"Created personal details: {personal_details}")  # Debugging personal details creation

        # Validate fields based on user type
        user_type_data = {'user': user, 'user_type': user_type}
        
        if user_type == "doctor":
            specialization = request.POST.get('specialization')
            phone_doctor = request.POST.get('phone_doctor')
            print(f"Specialization: {specialization}, Phone (Doctor): {phone_doctor}")  # Debugging

            if not specialization or not phone_doctor:
                messages.error(request, "Specialization and phone number are required for doctors.")
                return render(request, 'signup.html')

            user_type_data['specialization'] = specialization
            user_type_data['phone_doctor'] = phone_doctor

        elif user_type == "patient":
            guardian_email = request.POST.get('guardian_email')
            print(f"Guardian Email: {guardian_email}")  # Debugging

            if not guardian_email:
                messages.error(request, "Guardian email is required for patients.")
                return render(request, 'signup.html')

            user_type_data['guardian_email'] = guardian_email

        elif user_type == "nurse":
            department = request.POST.get('department')
            phone_nurse = request.POST.get('phone_nurse')
            print(f"Department: {department}, Phone (Nurse): {phone_nurse}")  # Debugging

            if not department or not phone_nurse:
                messages.error(request, "Department and phone number are required for nurses.")
                return render(request, 'signup.html')

            user_type_data['department'] = department
            user_type_data['phone_nurse'] = phone_nurse

        # Create and save UserType model instance
        user_type_instance = UserType.objects.create(**user_type_data)
        print(f"Created UserType: {user_type_instance}")  # Debugging the created UserType

        # Add success message
        messages.success(request, "Signup successful! Please login.")

        # Redirect to login page
        return redirect('login')  # Adjust this to your actual login page URL

    return render(request, 'signup.html')
