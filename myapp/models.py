from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        extra_fields.setdefault("is_active", True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "admin")  # Automatically set to admin

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)

# Profile model to serve as the base user model
class Profile(AbstractUser):
    place = models.CharField(max_length=255, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
 
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
        ('doctor', 'Doctor'),
    ]
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, default='patient')
    is_approved = models.BooleanField(default=False)

    objects = CustomUserManager()

    # Avoid conflicts by setting custom related names for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# Nurse model
class Nurse(models.Model):
    user = models.OneToOneField('myapp.Profile', on_delete=models.CASCADE, related_name='nurse')
    phone_number = models.CharField(max_length=15)
    shift = models.CharField(max_length=50, help_text="Shift timing (e.g., Morning, Evening, Night)")

    def __str__(self):
        return f"Nurse: {self.user.first_name} {self.user.last_name} ({self.shift})"

# Doctor model
class Doctor(models.Model):
    user = models.OneToOneField('myapp.Profile', on_delete=models.CASCADE, related_name='doctor')
    phone_number = models.CharField(max_length=15)
    specification = models.TextField()
    experience = models.PositiveIntegerField(help_text="Number of years of experience")
    certificate_files = models.FileField(upload_to='certificates/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Doctor: {self.user.first_name} {self.user.last_name}"

# Function to generate admission number for the Patient model
def generate_admission_number():
    count = Patient.objects.count() + 1
    return f"PAT{count:04d}2025"

# Patient model
class Patient(models.Model):
    user = models.OneToOneField('myapp.Profile', on_delete=models.CASCADE, related_name='patient')
    phone_number = models.CharField(max_length=15, unique=True)
    admission_number = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.admission_number:
            self.admission_number = generate_admission_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name} ({self.phone_number}, {self.admission_number})"
