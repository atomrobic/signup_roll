from django.urls import path
from myapp import views  # Import views from the current app

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Define the URL pattern for the signup view
    # Other URL patterns
]
