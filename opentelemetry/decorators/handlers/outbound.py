from opentelemetry import propagate
from opentelemetry.propagators.textmap import Setter

PROPAGATOR = propagate.get_global_textmap()


class RequestSetter(Setter):
    def set(self, carrier, key: str, value: str) -> None:
        carrier.headers[key] = value


def get_or_update_kwargs(carrier_id_or_name=None, **kwargs):
    if isinstance(carrier_id_or_name, str):
        carrier = kwargs.get(carrier_id_or_name)
        if not carrier:
            kwargs.update({carrier_id_or_name: dict()})
    return kwargs


def set_parent_context(carrier_id_or_name, *args, **kwargs):
    carrier = None
    if carrier_id_or_name:
        kwargs = get_or_update_kwargs(carrier_id_or_name, **kwargs)
        carrier = kwargs.get(carrier_id_or_name)
        if args and (not carrier) and isinstance(carrier_id_or_name, int):
            carrier = args[carrier_id_or_name] if len(args) > carrier_id_or_name else None
    if carrier or isinstance(carrier, dict):
        if hasattr(carrier, "headers"):
            PROPAGATOR.inject(carrier=carrier, setter=RequestSetter())
        else:
            PROPAGATOR.inject(carrier=carrier)
    return args, kwargs
