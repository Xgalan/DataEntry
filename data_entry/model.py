# -*- coding: utf-8 -*-

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
        'um': { 'description': 'Micrometer', },
        'mm': { 'description': 'Millimeter', },
        'cm': { 'description': 'Centimeter', },
        'm': { 'description': 'Meter', },
        }

    def __init__(self, units='mm'):
        self.units = units

    def __str__(self):
        return 'Units: %s' % (self.description)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if isinstance(value, str):
            if value in self.units_of_measurement:
                self._units = value
                self.description = self.units_of_measurement[value]['description']
        else:
            raise ValueError('The name of the unit of measurement is invalid.')

    def __repr__(self):
        return "{__class__.__name__}(units={_units_str}, description={_description_str}, precision={_precision_str})".format(
            __class__=self.__class__,
            _units_str=self.units,
            _description_str=self.description,
            **self.__dict__)


class Model(Subject):
    '''
    Model class of a list of values of float type. With offline statistics.
    '''
    def __init__(self, values=[], offset=0):
        Subject.__init__(self)
        self._units = UnitRegistry()
        self._precision = 2

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

    def _convert_to_float(self, value):
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
            self._units.units = name
            self.notify()
        except:
            raise TypeError

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        if isinstance(value, int):
            self._precision = value
            self.notify()
        else:
            raise TypeError('precision must be of int type')

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        if isinstance(offset, (float, int)):
            self._offset = self._convert_to_float(offset)
            self.notify()
        else:
            raise TypeError('offset must be a float type or an int type.')

    @property
    def values(self):
        return [v for v in map(lambda x: x + self.offset, self._values)]

    @values.setter
    def values(self, some_values):
        if isinstance(some_values, list):
            self._values = [f for f in filter(None, [
                self._convert_to_float(v) for v in some_values])
                            ]
            self.notify()
        else:
            raise TypeError('values must be a list type.')

    def count_values(self):
        return 'Count: ' + str(len(self.values))

    def min(self):
        if self.values:
            return round(min(self.values), self.precision)
        else:
            return 0.0

    def max(self):
        if self.values:
            return round(max(self.values), self.precision)
        else:
            return 0.0

    def min_max(self):
        if self.values:
            return (str(self.min()) +
                    ' - ' +
                    str(self.max()) +
                    ' ' +
                    self.units.units)
        else:
            return None

    def __repr__(self):
        return "{__class__.__name__}(values=[{_values_str}], offset={_offset_str})".format(
            __class__=self.__class__,
            _values_str=", ".join(map(repr, self.values)),
            _offset_str=str(self.offset),
            **self.__dict__)

    def __str__(self):
        ''' string representation of an interval of min and max values. '''
        return 'model min:%.2f - max:%.2f' % (self.min(), self.max())
