from typing import Dict
from opentelemetry import service_types
from . import inbound, outbound

InBoundHandlers: Dict[
    service_types.AbstractService.__subclasses__(),
    inbound.AbstractContextHandler.__subclasses__()
] = {
    service_types.ConsoleService: inbound.ConsoleHandler,
    service_types.FlaskService: inbound.FlaskHandler,
    service_types.DjangoService: inbound.DjangoHandler
}

OutBoundHandler = outbound.set_parent_context
