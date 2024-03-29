from src.logger.SingleLogger import SingleLogger
from src.generator.DataGenerator import DataGenerator
import os

def miscellaneous_generator_fn(SQL_enable, MQL_enable):
    """This function allows the user to generate data to populate SQL and NoSQL databases"""

    try:
        ready = False
        while not ready:
            os.system('clear')
            print("Data generator\n\n")
            total_rows = int(input("How many rows do you want to generate?: "))
            file_numbers = int(input("How many files would you like the rows to be split into?: "))
            if total_rows == "":
                total_rows = 100000
            if file_numbers == "":
                file_numbers = 10
            print("")
            print(f"As a result, {total_rows} rows are going to be generated and split into {file_numbers} files")
            confirmation = input("Are you sure? [yes,no,exit]: ").lower()
            if confirmation == "exit":
                return
            if confirmation == "yes" or confirmation == "y":
                ready = True
        os.system('clear')
        print("Data generator\n")
        generator = DataGenerator(int(total_rows/file_numbers),file_numbers, SQL_enable, MQL_enable)
        generator.generate_patients()
        generator.generate_doctors()
        generator.generate_medicalrecords()
        print("\nPress enter to continue...")
        input()
    except:
        SingleLogger().logger.exception("Error while generating data with DataGenerator", exc_info=True)