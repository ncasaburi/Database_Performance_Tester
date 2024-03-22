
class SingleLogger():
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, logger) -> None:
        self.__logger = logger