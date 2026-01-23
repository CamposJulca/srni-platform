from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def execute_sql(request):
    # TODO: validar SELECT y ejecutar
    return JsonResponse({"columns": [], "rows": []})
