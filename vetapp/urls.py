



urlpatterns = [
            ]

from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('services/', views.services, name='services'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('review-clinic/', views.review_clinic, name='review_clinic'),
    path('signup/', views.register, name='signup'),
    path('accounts/login/', views.UserLogin, name='login'),
	path('logout/', views.UserLogout, name='logout'),
    path('appointment-history/', views.appointment_history, name='appointment_history'),
]
