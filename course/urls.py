from django.urls import path
from . import views

urlpatterns = [
    path('generate_course/', views.generate_course, name='generate_course'),
]
