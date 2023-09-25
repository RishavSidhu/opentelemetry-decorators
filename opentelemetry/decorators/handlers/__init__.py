from typing import Dict
from opentelemetry import service_types
from . import inbound, outbound

InBoundHandlers: Dict[
    type(service_types.AbstractService.__subclasses__),
    inbound.AbstractContextHandler.__subclasses__()
] = {
    type(service_types.ConsoleService()): inbound.ConsoleHandler,
    type(service_types.FlaskService()): inbound.FlaskHandler,
    type(service_types.DjangoService()): inbound.DjangoHandler
}

OutBoundHandler = outbound.set_parent_context
