import os

from django.core.asgi import get_asgi_application


# Compatibility entrypoint for hosting platforms configured with `api.asgi`.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_asgi_application()
