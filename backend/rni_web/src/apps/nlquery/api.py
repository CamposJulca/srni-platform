# apps/nlquery/api.py
import json
import os
import re
from typing import Any, Dict, Optional, Tuple

from django.db import connection
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.decorators import login_required

from apps.accounts.api import _json_ok, _json_error

from .services.schema_loader import SchemaLoader
from .services.prompt_builder import PromptBuilder
from .services.sql_generator import SQLGenerator


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


def _build_nl2sql(question: str) -> Tuple[Optional[str], Optional[str], Optional[int]]:
    """
    Returns: (sql, error_code, http_status)
      - sql: generated SQL if ok
      - error_code: string error code for _json_error if failed
      - http_status: recommended status code if failed
    """
    try:
        schema = SchemaLoader().load()
        prompt = PromptBuilder().build(schema=schema, user_question=question)
        sql = SQLGenerator().generate(prompt)
        return sql, None, None
    except Exception as e:
        msg = str(e)

        # Error controlado cuando falta API key (no 500)
        if "OPENAI_API_KEY" in msg or "api_key client option" in msg:
            return None, "OPENAI_NOT_CONFIGURED", 503

        return None, "NLQUERY_GENERATE_ERROR", 500


# -----------------------------
# Endpoints
# -----------------------------

@login_required
@require_GET
def schema(request):
    try:
        schema = SchemaLoader().load()
        return _json_ok({"schema": schema})
    except Exception as e:
        return _json_error("NLQUERY_SCHEMA_ERROR", str(e), 500)


@login_required
@require_GET
def health(request):
    """
    Health check del módulo nlquery.
    Útil sin API key y también cuando ya esté configurada.
    """
    db_ok = False
    schema_ok = False
    schema_tables = 0
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))

    # DB check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        db_ok = True
    except Exception:
        db_ok = False

    # Schema check
    try:
        s = SchemaLoader().load()
        schema_ok = True
        schema_tables = len(s.keys()) if isinstance(s, dict) else 0
    except Exception:
        schema_ok = False

    return _json_ok(
        {
            "db_ok": db_ok,
            "schema_ok": schema_ok,
            "schema_tables": schema_tables,
            "openai_configured": openai_configured,
        }
    )


@login_required
@require_http_methods(["POST"])
def generate_sql(request):
    payload, err = _parse_json(request)
    if err:
        return _json_error("INVALID_JSON", f"Invalid JSON body. Detail: {err}", 400)

    question = (payload.get("question") or "").strip()
    if not question:
        return _json_error("VALIDATION_ERROR", "question is required.", 400)

    sql, err_code, status = _build_nl2sql(question)
    if err_code:
        if err_code == "OPENAI_NOT_CONFIGURED":
            return _json_error(
                "OPENAI_NOT_CONFIGURED",
                "Set OPENAI_API_KEY in the environment (.env / docker-compose) and restart the backend.",
                503,
            )
        return _json_error(err_code, "Failed to generate SQL.", status or 500)

    ok, v_err = _validate_sql_select_only(sql)
    if not ok:
        return _json_error("SQL_NOT_ALLOWED", v_err, 400)

    return _json_ok({"sql": sql})


@login_required
@require_http_methods(["POST"])
def run_query(request):
    payload, err = _parse_json(request)
    if err:
        return _json_error("INVALID_JSON", f"Invalid JSON body. Detail: {err}", 400)

    question = (payload.get("question") or "").strip()
    sql_in = (payload.get("sql") or "").strip()

    if not question and not sql_in:
        return _json_error("VALIDATION_ERROR", "question or sql is required.", 400)

    sql = sql_in
    if question and not sql_in:
        sql, err_code, status = _build_nl2sql(question)
        if err_code:
            if err_code == "OPENAI_NOT_CONFIGURED":
                return _json_error(
                    "OPENAI_NOT_CONFIGURED",
                    "Set OPENAI_API_KEY in the environment (.env / docker-compose) and restart the backend.",
                    503,
                )
            return _json_error(err_code, "Failed to generate SQL.", status or 500)

    ok, v_err = _validate_sql_select_only(sql)
    if not ok:
        return _json_error("SQL_NOT_ALLOWED", v_err, 400)

    try:
        result = _execute_select(sql)
        return _json_ok({"sql": sql, "result": result})
    except Exception as e:
        return _json_error("NLQUERY_EXEC_ERROR", str(e), 500)
