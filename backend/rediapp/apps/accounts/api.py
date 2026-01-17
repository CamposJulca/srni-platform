from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_GET

@require_POST
def api_login(request):
    # TODO: leer JSON y autenticar
    return JsonResponse({"status": "ok"})

@require_POST
def api_logout(request):
    logout(request)
    return JsonResponse({"status": "logged_out"})

@require_GET
def api_me(request):
    user = request.user
    return JsonResponse({
        "id": user.id,
        "email": user.email,
        "username": user.username
    })
