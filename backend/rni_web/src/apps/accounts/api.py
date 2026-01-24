import json

from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie


def _json_error(code: str, message: str, status: int):
    return JsonResponse(
        {"ok": False, "data": None, "error": {"code": code, "message": message}},
        status=status,
    )


def _json_ok(data=None, status: int = 200):
    return JsonResponse({"ok": True, "data": data, "error": None}, status=status)


@require_GET
@ensure_csrf_cookie
def api_csrf(request):
    # Solo fuerza la cookie csrftoken (Django la setea por middleware)
    return _json_ok({"status": "ok"})

@require_POST
def api_login(request):
    raw = request.body  # bytes

    # DEBUG TEMP: inspecciona exactamente qué llega
    if request.GET.get("debug") == "1":
        return JsonResponse({
            "content_type": request.META.get("CONTENT_TYPE"),
            "content_length": request.META.get("CONTENT_LENGTH"),
            "raw_len": len(raw),
            "raw_repr": repr(raw),
            "raw_decoded": raw.decode("utf-8", errors="replace"),
        })

    try:
        raw = request.body.decode("utf-8-sig")  # acepta BOM si viene
        payload = json.loads(raw or "{}")
    except Exception as e:
        return _json_error("INVALID_JSON", f"Invalid JSON body. Detail: {type(e).__name__}: {e}", 400)


    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return _json_error("MISSING_CREDENTIALS", "Username and password are required.", 400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return _json_error("INVALID_CREDENTIALS", "Invalid username or password.", 401)

    login(request, user)
    return _json_ok(
        {"authenticated": True, "id": user.id, "username": user.username, "email": user.email},
        status=200,
    )


@require_POST
def api_logout(request):
    logout(request)
    return _json_ok({"status": "logged_out"}, status=200)


@require_GET
def api_me(request):
    if not request.user.is_authenticated:
        return _json_error("NOT_AUTHENTICATED", "Not authenticated.", 401)

    user = request.user
    return _json_ok(
        {"authenticated": True, "id": user.id, "username": user.username, "email": user.email},
        status=200,
    )
