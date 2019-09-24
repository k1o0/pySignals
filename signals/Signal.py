from abc import ABC, abstractmethod


class Signal(ABC):
    def __init__(self):
        super().__init__()
        self._observers = []

    @abstractmethod
    def apply_transfer(self, f):
        pass

    # @abstractmethod
    def map(self, f, format_spec=None):
        pass

    @abstractmethod
    def map2(self, other, f, format_spec=None):
        pass

    def __add__(self, other):
        return self.map2(other, self.__add__, format_spec='({0} + {1})')

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __pow__(self, modulo=None):
        pass

    def __truediv__(self):
        pass

    def __floordiv__(self, other):
        pass

    def __mod__(self, other):
        pass

    def __lshift__(self, other):
        pass

    def __rshift__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __invert__(self):
        pass

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass