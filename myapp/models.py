from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username


class PersonalDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    place = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class UserType(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    
    # Doctor-specific fields
    specialization = models.CharField(max_length=100, blank=True, null=True)
    phone_doctor = models.CharField(max_length=15, blank=True, null=True)
    
    # Patient-specific fields
    guardian_email = models.EmailField(blank=True, null=True)
    
    # Nurse-specific fields
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_nurse = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

