from consolemenu import *
from consolemenu.items import *
from src.menu.miscellaneous.SubmenuMiscellaneousGenerator import SubmenuMiscellaneousGenerator
from src.menu.status import status

class SubmenuMiscellaneous():

    def __init__(self) -> None:
        """This function initializes the SubmenuMiscellaneous class"""

        #submenu definition
        self.submenu_miscellaneous = ConsoleMenu("Miscellaneous", status)

        #submenu items
        miscellaneous_generator = SubmenuItem("Generate data to populate databases", SubmenuMiscellaneousGenerator().get(), menu=self.submenu_miscellaneous)

        #submenu appends
        self.submenu_miscellaneous.append_item(miscellaneous_generator)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_miscellaneous
         