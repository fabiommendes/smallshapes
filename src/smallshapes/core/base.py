from smallvectors import Flatable, MathFunctionsMixin as _MathFunctionsMixin, Object
from smallvectors.core.mutability import Mutable, Immutable
from smallvectors.core.sequentiable import Sequentiable


class MathFunctionsMixin(_MathFunctionsMixin):
    __slots__ = ()

    _circle = _mcircle = _aabb = _maabb = NotImplemented


class SmallshapesBase(Flatable, Sequentiable, MathFunctionsMixin, Object):
    """
    Base class for all geometric objects in the smallshapes package.
    """

    __slots__ = ()

    @property
    def __anytype__(self):
        cls = type(self)
        for T in cls.mro():
            if not issubclass(T, (Mutable, Immutable)):
                setattr(cls, '__anytype__', T)
                return T
        raise AttributeError

    def __setitem__(self, key, value):
        N = len(self)
        if isinstance(key, int):
            if key > N:
                raise IndexError(key)
            elif key >= 0:
                self.__setitem_simple__(key, value)
            elif key < 0:
                self.__setitem_simple__(N - key, value)
        elif isinstance(key, slice):
            indexes = range(*slice)
            if indexes[-1] > len(self):
                raise IndexError
            else:
                setindex = self.__setitem_simple__
                values = [value[i] for i in indexes]
                for i, v in zip(indexes, values):
                    setindex(i, v)
        else:
            raise TypeError('invalid index: %r' % key)

    def __setitem_simple__(self, key, value):
        raise NotImplementedError


