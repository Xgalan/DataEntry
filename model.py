#!/usr/bin/env python3
# coding: utf-8
import statistics


class Model:
    ''' Model class of a list of values of float type. With statistics. '''
    def __init__(self, values=[], offset=0, observable=None):
        try:
            if observable is not None:
                observable.register_observer(self)
            # kwargs validation
            if isinstance(values, list):
                self._values = values
            else:
                raise TypeError('values must be of type list.')
            if isinstance(offset, (float, int)):
                self._offset = float(offset)
            else:
                raise TypeError('offset must be type float or type int.')
        except TypeError:
            raise TypeError
            return

    def _check_and_convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return None

    def notify(self, observable, *args, **kwargs):
        if 'values' in kwargs:
            self.values = kwargs['values']
        if 'offset' in kwargs:
            self.offset = kwargs['offset']

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, aOffset):
        if isinstance(aOffset, (float, int)):
            self._offset = float(aOffset)
        else:
            raise TypeError('offset must be a float type or an int type.')

    @property
    def values(self):
        return [float_value for float_value in filter(
            lambda x: x is not None, [self._check_and_convert_to_float(v) for v in
                                      map(lambda x: x + self.offset, self._values)]
            )]

    @values.setter
    def values(self, someValues):
        if isinstance(someValues, list):
            self._values = [self._check_and_convert_to_float(v) for v in
                            someValues]
        else:
            raise TypeError('values must be a list type.')

    def count_values(self):
        return('Count: ' + str(len(self.values)))

    def min(self):
        return min(self.values)

    def max(self):
        return max(self.values)

    def mean(self):
        return statistics.mean(self.values)

    def pstdev(self):
        return statistics.pstdev(self.values)

    def __repr__(self):
        return "{__class__.__name__}(values=[{_values_str}], offset={_offset_str})".format(
            __class__=self.__class__,
            _values_str=", ".join(map(repr, self.values)),
            _offset_str=str(self.offset),
            **self.__dict__)

    def __str__(self):
        ''' string representation of an interval of min and max values. '''
        return 'model min:%.2f - max:%.2f' % (self.min(), self.max())
