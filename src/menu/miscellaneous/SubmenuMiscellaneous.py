from consolemenu import *
from consolemenu.items import *
from src.menu.miscellaneous.SubmenuMiscellaneousGenerator import SubmenuMiscellaneousGenerator
from src.logic.status import status
from src.logic.miscellaneous.miscellaneous_autoconnect import *

class SubmenuMiscellaneous():

    def __init__(self) -> None:
        """This function initializes the SubmenuMiscellaneous class"""

        #submenu definition
        self.submenu_miscellaneous = ConsoleMenu("Miscellaneous", status)

        #submenu items
        miscellaneous_generator = SubmenuItem("Generate data to populate databases", SubmenuMiscellaneousGenerator().get(), menu=self.submenu_miscellaneous)
        miscellaneous_autoconnect = FunctionItem((lambda condition: "Deactivate autoconnect" if condition else "Activate autoconnect")(autoconnect_read()), self.miscellaneous_autoconnect_update_fn)

        #submenu appends
        self.submenu_miscellaneous.append_item(miscellaneous_generator)
        self.submenu_miscellaneous.append_item(miscellaneous_autoconnect)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_miscellaneous

    def miscellaneous_autoconnect_update_fn(self) -> None:
        autoconnect_switch()
        self.submenu_miscellaneous.remove_item(self.submenu_miscellaneous.items[1])
        miscellaneous_autoconnect = FunctionItem((lambda condition: "Deactivate autoconnect" if condition else "Activate autoconnect")(autoconnect_read()), self.miscellaneous_autoconnect_update_fn)
        self.submenu_miscellaneous.append_item(miscellaneous_autoconnect)
        self.submenu_miscellaneous.show()
        