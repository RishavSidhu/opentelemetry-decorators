from urllib.request import urlopen, Request

from django.http import HttpResponse

from opentelemetry.trace import SpanKind
from opentelemetry.decorators import trace_as_current_span


@trace_as_current_span("GET /trace", kind=SpanKind.SERVER)
def trace(request):
    print(request.headers)
    return HttpResponse(request_another_service())


@trace_as_current_span(kind=SpanKind.CLIENT, carrier_id_or_name="headers")
def request_another_service(headers=None):
    print(headers)
    req = Request("http://localhost:5001/trace", headers=headers)
    with urlopen(req) as response:
        body = response.read()
        print(body)
        return body
