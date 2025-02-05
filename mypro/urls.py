# from django.urls import path
# from myapp import views

# urlpatterns = [
#     # path('dashboard/', views.dashboard, name='dashboard'),
#     # path('approve_doctors/',views.doctor_applications_view, name='approve_doctors'),
#     # path('appointments/', views.appointments, name='appointments'),
#     # path('settings/', views.settings, name='settings'),
#     # path('approve_certificate/<int:certificate_id>/', views.approve_certificate, name='approve_certificate'),
#     # path('reject_certificate/<int:certificate_id>/', views.reject_certificate, name='reject_certificate'),
#     # path('update_certificates/', views.update_certificate, name='update_certificate'),  # No certificate_id needed
#     #  path('signup/',views.signup,name="signup"),

#  ]
from django.urls import path
from myapp import views

urlpatterns = [
    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
    path('signup/',views.signup,name = 'signup'),
]
