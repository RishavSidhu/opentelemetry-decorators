from opentelemetry.decorators import trace_init
from config import FlaskConfig
print(trace_init(FlaskConfig))

bind = "localhost:5000"
workers = 1
proc_name = "flask_app_1"
