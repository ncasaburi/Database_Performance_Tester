from src.logger.SingleLogger import SingleLogger
from src.generator.DataGenerator import DataGenerator
import os

def previous_datasets():
    """This function allows the user to continue expanding an existing dataset"""

    generator = DataGenerator()
    previous_sets = generator.check_previous_sets()
    return previous_sets

def miscellaneous_generator_fn(SQL_enable, MQL_enable, resume:bool=False, previous_items_per_file:int=0, last_set_number:int=0):
    """This function allows the user to generate data to populate SQL and NoSQL databases"""

    try:
        ready = False
        while not ready:
            os.system('clear')
            print("Data generator\n\n")

            total_rows = int(input("Number of rows/documents you want to generate: "))

            if not resume:
                file_numbers = int(input("Number of files you would like the rows to be split into: "))
            else:
                file_numbers = int(total_rows) / int(previous_items_per_file)

            if file_numbers > total_rows:
                print("\nThe total number of files can't be greater than the number of rows/documents to generate")
                input("\n\nPress enter to continue...")
                continue

            if total_rows == 0 or total_rows == "":
                print("\nThe total number of rows/docuements to generate must be greater than 0")
                input("\n\nPress enter to continue...")
                continue
            
            if file_numbers == 0 or file_numbers == "":
                print("\nThe number of files must be greater than 0")
                input("\n\nPress enter to continue...")
                continue
                
            if file_numbers > total_rows:
                print("\nThe total number of rows/documents must be greater than the number of files")
                input("\n\nPress enter to continue...")
                continue

            if total_rows % file_numbers != 0:
                print("\nThe division between the total number of rows/documents and the number of files must be a natural number")
                input("\n\nPress enter to continue...")
                continue

            print("")
            print(f"As a result:")
            print("    "+str(int(file_numbers))+" files of "+str(int(total_rows/file_numbers))+" rows/documents each are going to be generated (total "+str(int(total_rows))+" rows/documents)")
            confirmation = input("\nAre you sure? [yes,no,exit]: ").lower()
            if confirmation == "exit":
                return
            if confirmation == "yes" or confirmation == "y":
                ready = True
        os.system('clear')
        print("Data generator\n")
        generator = DataGenerator(int(total_rows/file_numbers),int(file_numbers), SQL_enable, MQL_enable, int(last_set_number))
        generator.generate_patients()
        generator.generate_doctors()
        generator.generate_medicalrecords()
        generator.update_config(int(last_set_number+file_numbers))
        print("\nPress enter to continue...")
        input()
    except:
        SingleLogger().logger.exception("DataGenerator: Error while generating data", exc_info=True)