from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('news/', views.news, name='news'),
    path('contact/', views.contact, name='contact'),
    path('attendence/', views.attendence, name='attendence'),
    path('about/', views.about, name='about'),  # Add this line
]

