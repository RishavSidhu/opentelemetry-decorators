from abc import ABC, abstractmethod
from opentelemetry import propagate

PROPAGATOR = propagate.get_global_textmap()


class AbstractContextHandler(ABC):
    @abstractmethod
    def get_parent_context(self, getter, carrier_name, *args, **kwargs): ...


class ConsoleHandler(AbstractContextHandler):
    def get_parent_context(self, getter, carrier_name, *args, **kwargs):
        carrier = kwargs.get(carrier_name)
        if not carrier:
            from os import environ
            carrier = environ
        return PROPAGATOR.extract(getter=getter, carrier=carrier)


class FlaskHandler(AbstractContextHandler):
    def get_parent_context(self, getter, carrier_name, *args, **kwargs):
        carrier = kwargs.get(carrier_name)
        if not carrier:
            from flask import request
            carrier = request
        return PROPAGATOR.extract(getter=getter, carrier=carrier)


class DjangoHandler(AbstractContextHandler):
    def get_parent_context(self, getter, carrier_name, *args, **kwargs):
        carrier = kwargs.get(carrier_name)
        if not carrier:
            carrier = kwargs.get("request", args[1] if len(args) == 2 else [0])
            carrier = {k.lower(): [v] for k, v in carrier.headers.items()}
        return PROPAGATOR.extract(getter=getter, carrier=carrier)
