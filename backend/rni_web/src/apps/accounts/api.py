import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token


@require_GET
@ensure_csrf_cookie
def api_csrf(request):
    """
    Fuerza la creación de la cookie CSRF
    """
    return JsonResponse({"status": "ok"})


@require_POST
def api_login(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({"error": "Missing credentials"}, status=400)

    user = authenticate(request, username=username, password=password)

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    login(request, user)

    return JsonResponse({
        "authenticated": True,
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })


@require_POST
def api_logout(request):
    logout(request)
    return JsonResponse({"status": "logged_out"})


@require_GET
def api_me(request):
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False}, status=401)

    user = request.user
    return JsonResponse({
        "authenticated": True,
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })
