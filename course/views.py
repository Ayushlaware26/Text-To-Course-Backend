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
