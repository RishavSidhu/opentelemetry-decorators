from urllib.request import urlopen, Request

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
    request_another_service(headers={})
    return "success"


@trace_as_current_span(kind=SpanKind.CLIENT, carrier_id_or_name="headers")
def request_another_service(headers=None):
    print(headers)
    req = Request("http://localhost:8000/trace", headers=headers)
    with urlopen(req) as response:
        body = response.read()
        print(body)


if __name__ == "__main__":
    trace_init(config.TemplateConfig)
    app.run(port=5000, debug=True)
