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
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('signup/',views.signup,name = 'signup'),
    # path('login/',views.user_login,name = 'login'),
    # path('approve_doctors/',views.doctor_applications,name='approve_doctors'),
    # path('doctor-applications/download/<int:application_id>/', views.doctor_applications, {'action': 'download'}, name='download_certificate'),
    # path('update-status/<int:application_id>/<str:status>/', views.update_status, name='update_status'),
    # path('deactivate-doctor/<int:doctor_id>/', views.remove_doctor_application, name='deactivate_doctor'),
    # path('doctors_view', views.docters_views,name="doctors_view"),
    # path('deactivate-doctor/<int:application_id>/', views.deactivate_doctor, name='deactivate_doctor'),
    # path('doctor-applications/', views.doctor_applications, name='approve_doctors'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


