from type import Type

class Default(object):
    @staticmethod
    def default_value(type):
        if type == Type.INT:
            return 0
        elif type == Type.FLOAT:
            return 0.0
        elif type == Type.BOOL:
            return False
        else: # type == Type.STRING
            return ""