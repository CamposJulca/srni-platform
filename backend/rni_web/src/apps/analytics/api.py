# apps/analytics/api.py
import json
import re
from typing import Any, Dict, Optional, Tuple

from django.db import connection
from django.views.decorators.http import require_GET, require_http_methods

from apps.accounts.api import _json_ok, _json_error


def _require_auth(request):
    """
    API-first auth: devuelve 401 JSON si no hay sesión.
    Evita redirects a /accounts/login/ (que en este proyecto no existe).
    """
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return _json_error("NOT_AUTHENTICATED", "Not authenticated.", 401)
    return None


def _parse_json(request):
    try:
        raw = request.body.decode("utf-8-sig")
        return json.loads(raw or "{}"), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|grant|revoke|create|replace|execute|call)\b",
    re.IGNORECASE,
)


def _validate_sql_select_only(sql: str) -> Tuple[bool, Optional[str]]:
    if not sql or not sql.strip():
        return False, "SQL is empty."

    s = sql.strip()

    # Evita multi-statement
    if ";" in s:
        return False, "Multiple statements are not allowed."

    upper = s.lstrip().upper()
    # Permitimos WITH ... SELECT (CTE) o SELECT directo
    if not (upper.startswith("SELECT") or upper.startswith("WITH")):
        return False, "Only SELECT statements are allowed."

    if _FORBIDDEN.search(s):
        return False, "Forbidden SQL keyword detected."

    return True, None


def _execute_select(sql: str) -> Dict[str, Any]:
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [c[0] for c in (cursor.description or [])]
        rows = cursor.fetchall() if columns else []
        return {"columns": columns, "rows": [list(r) for r in rows]}


@require_GET
def analytics_health(request):
    err = _require_auth(request)
    if err:
        return err

    # valida DB rápida
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return _json_ok({"db_ok": True})
    except Exception as e:
        return _json_error("ANALYTICS_DB_ERROR", str(e), 500)


@require_http_methods(["POST"])
def execute_sql(request):
    err = _require_auth(request)
    if err:
        return err

    # Seguridad: solo superusers pueden ejecutar SQL libre
    if not request.user.is_superuser:
        return _json_error("FORBIDDEN", "Only superusers can execute SQL.", 403)

    payload, parse_err = _parse_json(request)
    if parse_err:
        return _json_error("INVALID_JSON", f"Invalid JSON body. Detail: {parse_err}", 400)

    sql = (payload.get("sql") or "").strip()
    if not sql:
        return _json_error("VALIDATION_ERROR", "sql is required.", 400)

    ok, v_err = _validate_sql_select_only(sql)
    if not ok:
        return _json_error("SQL_NOT_ALLOWED", v_err, 400)

    try:
        result = _execute_select(sql)
        return _json_ok({"sql": sql, "result": result})
    except Exception as e:
        return _json_error("ANALYTICS_EXEC_ERROR", str(e), 500)
