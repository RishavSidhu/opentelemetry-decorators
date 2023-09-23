from typing import Optional, Callable, Any, Dict
from functools import wraps

from opentelemetry import trace, context, baggage
from opentelemetry.trace import Tracer, Status, StatusCode, Span, SpanKind
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource

from . import handlers
import template_config

_is_trace_initialized = False
_tracer: Tracer
_config: template_config.TemplateConfig


def trace_init(config: template_config.TemplateConfig):
    global _tracer, _is_trace_initialized, _config
    if _is_trace_initialized:
        return _is_trace_initialized
    if not config:
        return False
    _config = config
    provider = TracerProvider(resource=Resource(attributes=config.RESOURCE_ATTRIBUTES))

    is_exporter_init = False

    if config.JAEGER_EXPORTER:
        from opentelemetry.exporter.jaeger.thrift import JaegerExporter
        processor = BatchSpanProcessor(JaegerExporter(**config.JAEGER_EXPORTER))
        provider.add_span_processor(processor)
        is_exporter_init = True

    if config.ZIPKIN_EXPORTER:
        from opentelemetry.exporter.zipkin.json import ZipkinExporter
        processor = BatchSpanProcessor(ZipkinExporter(**config.ZIPKIN_EXPORTER))
        provider.add_span_processor(processor)
        is_exporter_init = True

    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer(config.TRACER_NAME)
    _is_trace_initialized = True and is_exporter_init
    return _is_trace_initialized


def trace_decorator(name: Optional[str] = None,
                    kind: Optional[SpanKind] = SpanKind.INTERNAL,
                    carrier_name: str = None
                    ):
    def decorator(func: Callable):
        @wraps(func)
        def traceable_wrapper(*args, **kwargs):
            name_ = name if name else func.__name__
            if kind in {SpanKind.SERVER, SpanKind.CONSUMER}:
                handler = handlers.InBoundHandlers.get(type(_config.SERVICE_TYPE))
                if handler:
                    parent_context = handler.get_parent_context(_config.SERVICE_TYPE, carrier_name, *args, **kwargs)
                    context.attach(parent_context)

            with _tracer.start_as_current_span(name_, kind=kind) as current_span:
                if kind in {SpanKind.CLIENT, SpanKind.PRODUCER}:
                    args, kwargs = handlers.OutBoundHandler(carrier_name, *args, **kwargs)

                rv = func(*args, **kwargs)
                set_status(StatusCode.OK, current_span)
            return rv

        @wraps(func)
        def un_traceable_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if _is_trace_initialized:
            return traceable_wrapper
        return un_traceable_wrapper

    return decorator


def set_status(status: StatusCode, span: Optional[Span] = None, force: bool = False):
    span = span or trace.get_current_span()
    if hasattr(span, "status"):
        if (span.status.status_code == StatusCode.UNSET) or force:
            span.set_status(Status(status))
            return True
        return False
    span.set_status(Status(status))
    return True


def set_attribute(key, value: Any): trace.get_current_span().set_attribute(key, value)


def set_attributes(attributes: Dict): trace.get_current_span().set_attributes(attributes)


def add_to_bag(key, value): baggage.set_value(key, value)


def record_exception(exception: Exception, span: Optional[Span] = None):
    span = span or trace.get_current_span()
    span.set_status(Status(StatusCode.ERROR))
    span.record_exception(exception)
