from opentelemetry.decorators import trace_init
from config import DjangoConfig
print(trace_init(DjangoConfig))

bind = "localhost:8000"
workers = 1
proc_name = "django_app_1"
