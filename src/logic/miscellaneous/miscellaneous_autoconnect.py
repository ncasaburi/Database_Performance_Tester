from src.logger.SingleLogger import SingleLogger
from src.config.Config import Config

def autoconnect_read() -> bool:
    """This function checks whether the autoconnect option is enabled and returns the result"""

    try:
        return (lambda: True if Config().default_dbs["default_database_autoconnect"] == "True" else False)()
    except:
        SingleLogger().logger.exception("Error while reading the autoconnect option", exc_info=True)

def autoconnect_set(value:bool):
    """This function sets the autoconnect option"""

    try:
        Config().option_create_modify("Databases","default_database_autoconnect",str(value))
    except:
        SingleLogger().logger.exception("Error setting the autoconnect option", exc_info=True)

def autoconnect_switch():
    """This function swithches the autoconnect option"""

    try:
        autoconnect_set(not autoconnect_read())
    except:
        SingleLogger().logger.exception("Error switching the autoconnect option", exc_info=True)
