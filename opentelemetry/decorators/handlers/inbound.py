from abc import ABC, abstractmethod
from opentelemetry import propagate

PROPAGATOR = propagate.get_global_textmap()


class AbstractContextHandler(ABC):
    @abstractmethod
    def get_parent_context(self, getter, carrier_id_or_name=None, *args, **kwargs): ...


class ConsoleHandler(AbstractContextHandler):
    def get_parent_context(self, getter, carrier_id_or_name=None, *args, **kwargs):
        carrier = kwargs.get(carrier_id_or_name) if isinstance(carrier_id_or_name, str) else None
        if args and (not carrier) and isinstance(carrier_id_or_name, int):
            carrier = args[carrier_id_or_name] if len(args) > carrier_id_or_name else None
        if not carrier:
            from os import environ
            carrier = environ
        return PROPAGATOR.extract(getter=getter, carrier=carrier)


class FlaskHandler(AbstractContextHandler):
    def get_parent_context(self, getter, carrier_id_or_name=None, *args, **kwargs):
        carrier = kwargs.get(carrier_id_or_name) if isinstance(carrier_id_or_name, str) else None
        if args and (not carrier) and isinstance(carrier_id_or_name, int):
            carrier = args[carrier_id_or_name] if len(args) > carrier_id_or_name else None
        if not carrier:
            from flask import request
            carrier = request
        return PROPAGATOR.extract(getter=getter, carrier=carrier)


class DjangoHandler(AbstractContextHandler):
    def get_parent_context(self, getter, carrier_id_or_name=None, *args, **kwargs):
        carrier = kwargs.get(carrier_id_or_name) if isinstance(carrier_id_or_name, str) else None
        if args and (not carrier) and isinstance(carrier_id_or_name, int):
            carrier = args[carrier_id_or_name] if len(args) > carrier_id_or_name else None
        if not carrier:
            carrier = kwargs.get("request", args[1] if len(args) == 2 else args[0])
            carrier = {k.lower(): [v] for k, v in carrier.headers.items()}
        return PROPAGATOR.extract(getter=getter, carrier=carrier)
