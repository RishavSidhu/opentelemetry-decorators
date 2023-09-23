from opentelemetry import propagate
from opentelemetry.propagators.textmap import Setter

PROPAGATOR = propagate.get_global_textmap()


class RequestSetter(Setter):
    def set(self, carrier, key: str, value: str) -> None:
        carrier.headers[key] = value


def set_parent_context(carrier_name, *args, **kwargs):
    carrier = kwargs.get(carrier_name)
    if carrier:
        if hasattr(carrier, "headers"):
            PROPAGATOR.inject(carrier=carrier, setter=RequestSetter())
        else:
            PROPAGATOR.inject(carrier=carrier)
    return args, kwargs
