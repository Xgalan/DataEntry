#!/usr/bin/env python3
# coding: utf-8

import statistics



class Subject(object):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, modifier=None):
        for observer in self._observers:
            if modifier != observer:
                observer.update_values(self)


class UnitRegistry:
    ''' Represent the units of measurement of the model. '''
    units_of_measurement = {
        'um': 'Micrometer',
        'mm': 'Millimeter',
        'cm': 'Centimeter',
        'm': 'Meter'
        }

    def __init__(self, units='mm'):
        if units in self.units_of_measurement:
            self._units = units
            if isinstance(units, str):
                self.description = self.units_of_measurement[units]
        else:
            raise TypeError

    def __str__(self):
        ''' Representation of a unit of measurement. '''
        return 'Units: %s' % (self.description)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if isinstance(value, str):
            if value in self.units_of_measurement:
                self._units = value
                self.description = self.units_of_measurement[value]
        else:
            raise TypeError('The name of the unit of measurement is invalid.')


class Model(Subject):
    ''' Model class of a list of values of float type. With statistics. '''
    def __init__(self, values=[], offset=0):
        Subject.__init__(self)
        self._units = UnitRegistry()
        try:
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

    def _check_and_convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return None

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, name):
        try:
            print(self._units)
            self._units.units = name
            self.notify()
        except:
            raise TypeError

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        if isinstance(offset, (float, int)):
            self._offset = float(offset)
            self.notify()
        else:
            raise TypeError('offset must be a float type or an int type.')

    @property
    def values(self):
        return [float_value for float_value in filter(
            lambda x: x is not None, [self._check_and_convert_to_float(v) for v in
                                      map(lambda x: x + self.offset, self._values)]
            )]

    @values.setter
    def values(self, some_values):
        if isinstance(some_values, list):
            self._values = [self._check_and_convert_to_float(v) for v in
                            some_values]
            self.notify()
        else:
            raise TypeError('values must be a list type.')

    def count_values(self):
        return 'Count: ' + str(len(self.values))

    def min(self):
        if self.values:
            return min(self.values)
        else:
            return 0

    def max(self):
        if self.values:
            return max(self.values)
        else:
            return 0

    def mean(self):
        if self.values:
            return statistics.mean(self.values)
        else:
            return 0

    def pstdev(self):
        if self.values:
            return statistics.pstdev(self.values)
        else:
            return 0

    def __repr__(self):
        return "{__class__.__name__}(values=[{_values_str}], offset={_offset_str})".format(
            __class__=self.__class__,
            _values_str=", ".join(map(repr, self.values)),
            _offset_str=str(self.offset),
            **self.__dict__)

    def __str__(self):
        ''' string representation of an interval of min and max values. '''
        return 'model min:%.2f - max:%.2f' % (self.min(), self.max())
