from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render


def is_safe_sql(query: str) -> bool:
    query = query.strip().lower()
    return query.startswith("select")


@login_required
def sql_query_view(request):
    context = {
        "query": "",
        "columns": [],
        "rows": [],
        "error": None,
    }

    if request.method == "POST":
        query = request.POST.get("query", "")
        context["query"] = query

        if not is_safe_sql(query):
            context["error"] = "Solo se permiten consultas SELECT."
            return render(request, "analytics/query.html", context)

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                context["columns"] = [col[0] for col in cursor.description]
                context["rows"] = cursor.fetchall()
        except Exception as e:
            context["error"] = str(e)

    return render(request, "analytics/query.html", context)
