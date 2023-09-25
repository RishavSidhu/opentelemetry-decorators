from flask import Flask
from opentelemetry.trace import SpanKind
from opentelemetry.decorators import trace_init, trace_as_current_span
import config

app = Flask(__name__)
trace_init(config.FlaskConfig)


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/trace')
@trace_as_current_span("GET /trace", kind=SpanKind.SERVER)
def trace():
    return "success"


if __name__ == "__main__":
    trace_init(config.TemplateConfig)
    app.run(port=5001, debug=True)
