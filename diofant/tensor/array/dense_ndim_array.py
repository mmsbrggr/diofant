import functools
import itertools

from ...core import Basic, Tuple
from ...core.sympify import sympify
from ...matrices import Matrix
from ...utilities import flatten
from .mutable_ndim_array import MutableNDimArray
from .ndim_array import ImmutableNDimArray, NDimArray


class DenseNDimArray(NDimArray):

    def __getitem__(self, index):
        """
        Allows to get items from N-dim array.

        Examples
        ========

        >>> a = MutableDenseNDimArray([0, 1, 2, 3], (2, 2))
        >>> a
        [[0, 1], [2, 3]]
        >>> a[0, 0]
        0
        >>> a[1, 1]
        3

        Symbolic index:
        >>> a[n, m]
        [[0, 1], [2, 3]][n, m]
        >>> a[n, m].subs({n: 1, m: 1})
        3

        """
        syindex = self._check_symbolic_index(index)
        if syindex is not None:
            return syindex

        if isinstance(index, tuple) and any(isinstance(i, slice) for i in index):
            def slice_expand(s, dim):
                if not isinstance(s, slice):
                    return s,
                start, stop, step = s.indices(dim)
                return [start + i*step for i in range((stop-start)//step)]

            sl_factors = [slice_expand(i, dim) for (i, dim) in zip(index, self.shape)]
            eindices = itertools.product(*sl_factors)
            array = [self._array[self._parse_index(i)] for i in eindices]
            nshape = [len(el) for i, el in enumerate(sl_factors) if isinstance(index[i], slice)]
            return type(self)(array, nshape)
        else:
            if isinstance(index, slice):
                return self._array[index]
            else:
                index = self._parse_index(index)
                return self._array[index]

    @classmethod
    def zeros(cls, *shape):
        list_length = functools.reduce(lambda x, y: x*y, shape)
        return cls._new(([0]*list_length,), shape)

    def tomatrix(self):
        """
        Converts MutableDenseNDimArray to Matrix. Can convert only 2-dim array, else will raise error.

        Examples
        ========

        >>> a = MutableDenseNDimArray([1 for i in range(9)], (3, 3))
        >>> b = a.tomatrix()
        >>> b
        Matrix([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]])

        """
        if self.rank() != 2:
            raise ValueError('Dimensions must be of size of 2')

        return Matrix(self.shape[0], self.shape[1], self._array)

    def __iter__(self):
        return self._array.__iter__()

    def reshape(self, *newshape):
        """
        Returns MutableDenseNDimArray instance with new shape. Elements number
        must be        suitable to new shape. The only argument of method sets
        new shape.

        Examples
        ========

        >>> a = MutableDenseNDimArray([1, 2, 3, 4, 5, 6], (2, 3))
        >>> a.shape
        (2, 3)
        >>> a
        [[1, 2, 3], [4, 5, 6]]
        >>> b = a.reshape(3, 2)
        >>> b.shape
        (3, 2)
        >>> b
        [[1, 2], [3, 4], [5, 6]]

        """
        new_total_size = functools.reduce(lambda x, y: x*y, newshape)
        if new_total_size != self._loop_size:
            raise ValueError("Invalid reshape parameters " + str(newshape))

        # there is no `.func` as this class does not subtype `Basic`:
        return type(self)(self._array, newshape)


class ImmutableDenseNDimArray(DenseNDimArray, ImmutableNDimArray):

    def __new__(cls, iterable=None, shape=None, **kwargs):
        return cls._new(iterable, shape, **kwargs)

    @classmethod
    def _new(cls, iterable, shape, **kwargs):
        shape, flat_list = cls._handle_ndarray_creation_inputs(iterable, shape, **kwargs)
        shape = Tuple(*(sympify(x, strict=True) for x in shape))
        flat_list = flatten(flat_list)
        flat_list = Tuple(*flat_list)
        self = Basic.__new__(cls, flat_list, shape, **kwargs)
        self._shape = shape
        self._array = list(flat_list)
        self._rank = len(shape)
        self._loop_size = functools.reduce(lambda x, y: x*y, shape) if shape else 0
        return self

    def __setitem__(self, index, value):
        raise TypeError('immutable N-dim array')

    def __hash__(self):
        return Basic.__hash__(self)


class MutableDenseNDimArray(DenseNDimArray, MutableNDimArray):

    def __new__(cls, iterable=None, shape=None, **kwargs):
        return cls._new(iterable, shape, **kwargs)

    @classmethod
    def _new(cls, iterable, shape, **kwargs):
        shape, flat_list = cls._handle_ndarray_creation_inputs(iterable, shape, **kwargs)
        flat_list = flatten(flat_list)
        self = object.__new__(cls)
        self._shape = shape
        self._array = list(flat_list)
        self._rank = len(shape)
        self._loop_size = functools.reduce(lambda x, y: x*y, shape) if shape else 0
        return self

    def __setitem__(self, index, value):
        """Allows to set items to MutableDenseNDimArray.

        Examples
        ========

        >>> a = MutableDenseNDimArray.zeros(2,  2)
        >>> a[0, 0] = 1
        >>> a[1, 1] = 1
        >>> a
        [[1, 0], [0, 1]]

        """
        index = self._parse_index(index)
        self._setter_iterable_check(value)
        value = sympify(value, strict=True)

        self._array[index] = value
