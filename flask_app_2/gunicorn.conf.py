from opentelemetry.decorators import trace_init
from config import FlaskConfig
trace_init(FlaskConfig)

bind = "localhost:5001"
workers = 1
proc_name = "flask_app_2"
