from django.http import JsonResponse

def generate_course(request):
    return JsonResponse({
        "message": "Backend is working!",
        "sample": "This will later generate content"
    })
