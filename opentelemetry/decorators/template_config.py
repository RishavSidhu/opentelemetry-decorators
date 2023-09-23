from typing import Dict, Optional
from dataclasses import dataclass

from opentelemetry.semconv.resource import ResourceAttributes as Ra

from opentelemetry.service_types import AbstractService


@dataclass
class TemplateConfig:
    RESOURCE_ATTRIBUTES = {
        Ra.SERVICE_NAMESPACE: "com.domain.app",
        Ra.SERVICE_NAME: "service",
    }
    TRACER_NAME: str = "tracer.name"
    JAEGER_EXPORTER: Optional[Dict] = None
    ZIPKIN_EXPORTER: Optional[Dict] = None
    SERVICE_TYPE: AbstractService.__subclasses__() = None
    outbound_attributes: dict