from django.urls import path
from . import views

urlpatterns = [
    path("generate_course/", views.generate_course, name="generate_course"),
    path("user-courses/", views.user_courses, name="user_courses"),
    path("course/<int:course_id>/", views.course_detail, name="course_detail"),
    path(
        "course/<int:course_id>/lesson/<int:lesson_id>/",
        views.lesson_detail,
        name="lesson_detail",
    ),
]
