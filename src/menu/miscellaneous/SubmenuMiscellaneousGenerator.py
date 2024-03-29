from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.miscellaneous.miscellaneous_generator import miscellaneous_generator_fn

class SubmenuMiscellaneousGenerator():

    def __init__(self) -> None:
        """This function initializes the SubmenuMiscellaneousGenerator class"""
        
        #submenu definition
        self.submenu_miscellaneous_generator = ConsoleMenu("Data Generator", status)
        
        #submenu items
        miscellaneous_generator_both = FunctionItem("Generate data to populate both SQL and NoSQL databases", miscellaneous_generator_fn, args=[True,True]) 
        miscellaneous_generator_sql = FunctionItem("Generate data to populate SQL databases", miscellaneous_generator_fn, args=[True,False])
        miscellaneous_generator_mql = FunctionItem("Generate data to populate NoSQL databases", miscellaneous_generator_fn, args=[False,True])

        #submenu appends
        self.submenu_miscellaneous_generator.append_item(miscellaneous_generator_both)
        self.submenu_miscellaneous_generator.append_item(miscellaneous_generator_sql)
        self.submenu_miscellaneous_generator.append_item(miscellaneous_generator_mql)

    def get(self) -> ConsoleMenu:
        return self.submenu_miscellaneous_generator