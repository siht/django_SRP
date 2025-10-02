# business_logic/misc/patterns.py

class Singleton(type):
    def __init__(cls, name, bases, dct):
        cls._instance = None
        type.__init__(cls, name, bases, dct)

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = type.__call__(cls, *args,**kw)
        return cls._instance


class Flyeight(type):
    def __init__(cls, name, bases, dct):
        cls._instances = {}
        type.__init__(cls, name, bases, dct)

    def __call__(cls, key, *args, **kw):
        instance = cls._instances.get(key)
        if instance is None:
            instance = type.__call__(cls, key, *args, **kw)
            cls._instances[key] = instance
        return instance
