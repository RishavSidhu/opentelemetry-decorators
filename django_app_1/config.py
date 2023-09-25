from opentelemetry.semconv.resource import ResourceAttributes as Ra

from opentelemetry.service_types import DjangoService
from opentelemetry.decorators.template_config import TemplateConfig


class DjangoConfig(TemplateConfig):
    RESOURCE_ATTRIBUTES = {
        Ra.SERVICE_NAMESPACE: "com.domain.app",
        Ra.SERVICE_NAME: "django_app_1",
    }
    TRACER_NAME = "main"
    JAEGER_EXPORTER = {"agent_host_name": "localhost", "agent_port": 6831}
    SERVICE_TYPE = DjangoService()
