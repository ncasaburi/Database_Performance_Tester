from consolemenu import *
from consolemenu.items import *
from src.logic.status import status
from src.logic.postgres.row.postgres_row_insert import postgres_row_insert_fn
from src.logic.postgres.row.postgres_row_batch_insert import postgres_row_batch_insert_fn

class SubmenuPostgresRowInsert():

    def __init__(self) -> None:
        """This function initializes the SubmenuPostgresRowInsert class"""
        
        #submenu definition
        self.submenu_postgres_row_insert = ConsoleMenu("PostgreSQL Row Inserts", status)
        
        #submenu items
        postgres_row_insert_default = FunctionItem("Insert default rows", postgres_row_insert_fn, args=["default"])
        postgres_row_batch_insert_default = FunctionItem("Batch default row insert", postgres_row_batch_insert_fn)  
        postgres_row_insert_custom = FunctionItem("Insert custom rows", postgres_row_insert_fn, args=["custom"])

        #submenu appends
        self.submenu_postgres_row_insert.append_item(postgres_row_insert_default)
        self.submenu_postgres_row_insert.append_item(postgres_row_batch_insert_default)
        self.submenu_postgres_row_insert.append_item(postgres_row_insert_custom)
    
    def get(self) -> ConsoleMenu:
        return self.submenu_postgres_row_insert