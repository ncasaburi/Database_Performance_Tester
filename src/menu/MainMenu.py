from consolemenu import *
from consolemenu.items import *
from src.menu.SubmenuPostgres.SubmenuPostgres import SubmenuPostgres
from src.menu.SubmenuMongo.SubmenuMongo import SubmenuMongo
from src.menu.status import status

class MainMenu():

    def __init__(self) -> None:
        """This function initializes the CustomMenu class"""

        #menu definition
        menu = ConsoleMenu("Database Performance Tester", status )

        #menu items
        menu_postgres = SubmenuItem("PostgreSQL", SubmenuPostgres().get(), menu)
        menu_mongo = SubmenuItem("MongoDB", SubmenuMongo().get(), menu)

        #menu appends
        menu.append_item(menu_postgres)
        menu.append_item(menu_mongo)

        #display menu
        menu.start()
        menu.join()
         