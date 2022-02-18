class Singleton:
    _singleton = None

    @classmethod
    def get_instance(cls):
        if cls._singleton is None:
            cls._singleton = cls()
        return cls._singleton
