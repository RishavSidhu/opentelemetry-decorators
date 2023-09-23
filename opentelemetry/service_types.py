from abc import ABC, abstractmethod


class AbstractService(ABC):
    @abstractmethod
    def get(self, *args, **kwargs): ...


class ConsoleService(AbstractService):
    def get(self, environ, key):
        return environ.get(key)


class FlaskService(AbstractService):
    def get(self, request, key):
        return request.headers.get_all(key)


class DjangoService(AbstractService):
    def get(self, headers, key):
        return headers.get(key)
