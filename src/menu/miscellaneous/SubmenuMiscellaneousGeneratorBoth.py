from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.miscellaneous.miscellaneous_generator import miscellaneous_generator_fn
from src.logic.miscellaneous.miscellaneous_generator import previous_datasets
from src.logger.SingleLogger import SingleLogger

class SubmenuMiscellaneousGeneratorBoth():

    def __init__(self) -> None:
        """This function initializes the SubmenuMiscellaneousGeneratorBoth class"""
        
        #submenu definition
        self.submenu_miscellaneous_generator_both = ConsoleMenu("Data Generator SQL and NoSQL", status)

        self.miscellaneous_generator_both_update_fn()

    def get(self) -> ConsoleMenu:
        return self.submenu_miscellaneous_generator_both
    
    def miscellaneous_generator_both_update_fn(self) -> None:

        datasets = previous_datasets()

        while not len(self.submenu_miscellaneous_generator_both.items) == 0:
            for item in self.submenu_miscellaneous_generator_both.items:
                self.submenu_miscellaneous_generator_both.remove_item(item)

        if bool(datasets):
            for key, value in datasets.items():
                self.submenu_miscellaneous_generator_both.append_item( FunctionItem("Continue dataset of "+str(len(value))+" files and "+str(key)+" items each", self.miscellaneous_generator_both_update_auxiliar_fn, args=[key,value]) )
        self.submenu_miscellaneous_generator_both.append_item(FunctionItem("Generate a new dataset", self.miscellaneous_generator_both_update_auxiliar_fn, args=[0,0]))

        self.submenu_miscellaneous_generator_both.draw()

    def miscellaneous_generator_both_update_auxiliar_fn(self, key, value):

        if not (key == 0) and not (len(value) == 0):
            miscellaneous_generator_fn(True,True,True,key,len(value))
            self.miscellaneous_generator_both_update_fn()
            self.submenu_miscellaneous_generator_both.show()
        else:
            miscellaneous_generator_fn(True,True)
            self.miscellaneous_generator_both_update_fn()
            self.submenu_miscellaneous_generator_both.show()
