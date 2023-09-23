# opentelemetry-decorators
Decorator for automatically handling propagation, with flexibility to do manual integration.

## Usage
```python
from opentelemetry.semconv.resource import ResourceAttributes as Ra

from opentelemetry.service_types import ConsoleService
from opentelemetry.decorators.template_config import TemplateConfig
from opentelemetry.decorators import trace_init, trace_decorator


# Define a configuration for your service.
class MyServiceConfig(TemplateConfig):
    RESOURCE_ATTRIBUTES = {
        Ra.SERVICE_NAMESPACE: "com.domain.app",
        Ra.SERVICE_NAME: "service",
    }
    TRACER_NAME: str = "my_service_tracer"
    JAEGER_EXPORTER = {"host": "hostname", "port": 1234}
    SERVICE_TYPE = ConsoleService

# Initialize tracing.
trace_init(MyServiceConfig)

# Start Integrating with decorators.
@trace_decorator()
def some_function(): ...
```
