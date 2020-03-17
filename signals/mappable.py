from abc import ABC, abstractmethod
import operator
import numpy as np


class MappableMixin(ABC):
    """Mixin to implement operators and collections via map"""

    @abstractmethod
    def map(self, f, format_spec=None):
        """TODO Document"""
        pass

    @abstractmethod
    def map2(self, other, f, format_spec=None):
        """TODO Document"""
        pass

    @abstractmethod
    def mapn(*args, f=None, format_spec=None):
        """TODO Document"""
        pass


class NumpyOperators(object):

    def __add__(self, other):
        return self.map2(other, np.add, format_spec='{0} + {1}')

    def __sub__(self, other):
        return self.map2(other, np.subtract, format_spec='{0} - {1}')

    def __mul__(self, other):
        return self.map2(other, np.multiply, format_spec='{0} * {1}')

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
        # Logical or bitwise and?
        return self.map2(other, np.logical_and, format_spec='{0} * {1}')

    def __or__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __invert__(self):
        return self.map(np.invert, format_spec='~{0}')

    def __lt__(self, other):
        return self.map2(other, np.less, format_spec='{0} < {1}')

    def __le__(self, other):
        return self.map2(other, np.less_equal, format_spec='{0} <= {1}')

    def __eq__(self, other):
        return self.map2(other, np.equal, format_spec='{0} == {1}')

    def __ne__(self, other):
        return self.map2(other, np.not_equal, format_spec='{0} != {1}')

    def __gt__(self, other):
        return self.map2(other, np.greater, format_spec='{0} > {1}')

    def __ge__(self, other):
        return self.map2(other, np.greater_equal, format_spec='{0} >= {1}')


class BasicOperators(object):
    def __add__(self, other):
        return self.map2(other, operator.add, format_spec='{0} + {1}')

    def __sub__(self, other):
        return self.map2(other, operator.sub, format_spec='{0} - {1}')

    def __mul__(self, other):
        return self.map2(other, operator.mul, format_spec='{0} * {1}')

    def __pow__(self, other, modulo=None):
        return self.mapn(other, modulo, operator.pow, format_spec='{0} ** {1}')

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
        return self.map2(other, operator.and_, format_spec='({0} and {1})')

    def __or__(self, other):
        return self.map2(other, operator.or_, format_spec='({0} or {1})')

    def __xor__(self, other):
        pass

    def __invert__(self):
        return self.map(operator.invert, format_spec='-{0}')

    def __lt__(self, other):
        return self.map2(other, operator.lt, format_spec='{0} < {1}')

    def __le__(self, other):
        return self.map2(other, operator.lt, format_spec='{0} <= {1}')

    def __eq__(self, other):
        return self.map2(other, operator.eq, format_spec='{0} == {1}')

    def __ne__(self, other):
        return self.map2(other, operator.ne, format_spec='{0} != {1}')

    def __gt__(self, other):
        return self.map2(other, operator.gt, format_spec='{0} > {1}')

    def __ge__(self, other):
        return self.map2(other, operator.ge, format_spec='{0} >= {1}')
