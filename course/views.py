from django.http import JsonResponse
from .auth_utils import require_auth

@require_auth
def generate_course(request):
    # You can access token payload here
    user_info = request.auth_payload

    # For now, just return dummy data
    return JsonResponse({
        "message": "This is a protected endpoint!",
        "user": user_info
    })

# Dummy user courses
@require_auth
def user_courses(request):
    user = request.auth_payload
    return JsonResponse({
        "courses": [
            {"id": 1, "title": "React for Beginners"},
            {"id": 2, "title": "Django with Auth0"},
        ],
        "user": user.get("sub"),  # user ID from Auth0
    })


# Dummy course details
@require_auth
def course_detail(request, course_id):
    return JsonResponse({
        "id": course_id,
        "title": f"Course {course_id}",
        "description": f"This is a dummy course with ID {course_id}.",
        "lessons": [
            {"id": 1, "title": "Introduction"},
            {"id": 2, "title": "Deep Dive"},
        ],
    })


# Dummy lesson detail
@require_auth
def lesson_detail(request, course_id, lesson_id):
    return JsonResponse({
        "course_id": course_id,
        "lesson_id": lesson_id,
        "title": f"Lesson {lesson_id}",
        "content": "This is dummy lesson content for testing protected endpoints."
    })