from django.urls import path
from .views import home, courses, news, contact, about, NoFace, attendence, display_csv_files

urlpatterns = [
    path('', home, name='home'),
    path('courses/', courses, name='courses'),
    path('news/', news, name='news'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('noface/', NoFace, name='NoFace'),
    path('attendence/', attendence, name='attendence'),
    path('display-csv/', display_csv_files, name='display_csv_files'),
]
