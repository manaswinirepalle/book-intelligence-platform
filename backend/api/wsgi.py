import os

from django.core.wsgi import get_wsgi_application


# Compatibility entrypoint for hosting platforms configured with `api.wsgi`.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()
