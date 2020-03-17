from abc import ABC, abstractmethod
from signals.mappable import MappableMixin, NumpyOperators


class Signal(ABC):
    def __init__(self):
        super().__init__()
        self._observers = []

    @abstractmethod
    def __apply_transfer(self, trans_fun, args, format_spec):
        pass

    @abstractmethod
    def on_value(self, f):
        pass

    @abstractmethod
    def output(self):
        pass

    @abstractmethod
    def to(self, other):
        pass

    @abstractmethod
    def __repr__(self):
        pass
