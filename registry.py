class Registry(object):
    """A simple registry for keeping track of all impact functions.

    We will use a singleton pattern to ensure that there is only
    one canonical registry. The registry can be used by impact functions
    to register themselves and their GUID's.
    """

    _instance = None
    _impact_functions = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Registry, cls).__new__(
                cls, *args, **kwargs)
            cls._impact_functions = []
        return cls._instance

    @classmethod
    def register(cls, impact_function):
        if impact_function not in cls._impact_functions:
            cls._impact_functions.append(impact_function)

    @classmethod
    def list(cls):
        for impact_function in cls._impact_functions:
            print impact_function.metadata()['name']

    @classmethod
    def get(cls, name):
        """Return an instance of an impact function given its name."""
        for impact_function in cls._impact_functions:
            if impact_function.__name__ == name:
                return impact_function.instance()
        raise Exception('Impact function called %s not found' % name)

