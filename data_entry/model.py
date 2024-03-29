# -*- coding: utf-8 -*-


class UnitRegistry:
    """Represent the units of measurement of the model."""

    units_of_measurement = {
        "um": {
            "description": "Micrometer",
        },
        "mm": {
            "description": "Millimeter",
        },
        "cm": {
            "description": "Centimeter",
        },
        "m": {
            "description": "Meter",
        },
        "g": {
            "description": "Gram",
        },
    }

    def __init__(self, units="mm"):
        self.units = units

    def __str__(self):
        return "Units: %s" % (self.description)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if isinstance(value, str):
            if value in self.units_of_measurement:
                self._units = value
                self.description = self.units_of_measurement[value]["description"]
        else:
            raise ValueError("The name of the unit of measurement is invalid.")

    def __repr__(self):
        return "{__class__.__name__}(units={_units_str}, description={_description_str}, precision={_precision_str})".format(
            __class__=self.__class__,
            _units_str=self.units,
            _description_str=self.description,
            **self.__dict__
        )


class Model:
    """
    Model class of a list of values of float type. With offline statistics.
    """

    def __init__(self, values=[], offset=0) -> None:
        self._units = UnitRegistry()
        self._precision = 2
        self._tolerance = {"min": 0.0, "max": 0.0}
        try:
            if isinstance(values, list):
                self._values = values
            else:
                raise TypeError("values must be of type list.")
            if isinstance(offset, (float, int)):
                self._offset = float(offset)
            else:
                raise TypeError("offset must be type float or type int.")
        except TypeError:
            raise TypeError

    def _convert_to_float(self, value) -> float:
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
        except:
            raise TypeError

    @property
    def precision(self):
        return self._precision

    @precision.setter
    def precision(self, value):
        if isinstance(value, int):
            self._precision = value
        else:
            raise TypeError("precision must be of int type")

    @property
    def tolerance(self):
        return self._tolerance

    @tolerance.setter
    def tolerance(self, tolerance):
        try:
            if isinstance(tolerance, dict):
                if "min" in tolerance and "max" in tolerance:
                    if isinstance(tolerance["min"], (int, float)) and isinstance(
                        tolerance["max"], (int, float)
                    ):
                        if tolerance["min"] <= tolerance["max"]:
                            self._tolerance = tolerance
                        else:
                            raise ValueError
                else:
                    raise TypeError
            else:
                raise TypeError
        except TypeError:
            print("tolerance must be a dict containing keywords 'min', 'max'")
        except ValueError:
            print("min tolerance must be minor or equal to max tolerance!")

    @property
    def offset(self) -> float | int:
        return self._offset

    @offset.setter
    def offset(self, offset):
        if isinstance(offset, (float, int)):
            self._offset = self._convert_to_float(offset)
        else:
            raise TypeError("offset must be a float type or an int type.")

    @property
    def values(self) -> list:
        return [v for v in map(lambda x: x + self.offset, self._values)]

    @values.setter
    def values(self, some_values):
        if isinstance(some_values, list):
            self._values = [
                f
                for f in filter(None, [self._convert_to_float(v) for v in some_values])
            ]
        else:
            raise TypeError("values must be a list type.")

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
            return str(self.min()) + " - " + str(self.max()) + " " + self.units.units
        else:
            return None

    def __repr__(self):
        return (
            "{__class__.__name__}(values=[{_values_str}], offset={_offset_str})".format(
                __class__=self.__class__,
                _values_str=", ".join(map(repr, self.values)),
                _offset_str=str(self.offset),
                **self.__dict__
            )
        )

    def __str__(self):
        """string representation of an interval of min and max values."""
        return "model min:%.2f - max:%.2f" % (self.min(), self.max())
