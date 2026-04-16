from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse


def root_status(_request):
    return JsonResponse(
        {
            "status": "ok",
            "message": "Book Intelligence backend is running",
            "api_base": "/api/",
            "health": "/health/",
        }
    )


def health_check(_request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    path('', root_status),
    path('health/', health_check),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
