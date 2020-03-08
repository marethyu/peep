from peep import Type

DEFAULT_VALUES = {
    Type.INT: 0,
    Type.FLOAT: 0.0,
    Type.BOOL: False,
    Type.STRING: ""
}

class Default(object):
    @staticmethod
    def default_value(type):
        return DEFAULT_VALUES.get(type)
