
from src.logger.SingleLogger import SingleLogger
from src.config.Zipper import Zipper
from src.config.Config import Config
from src.generator.CustomFaker import CustomFaker
from tqdm import tqdm
import time
import fnmatch
import os
import re

class DataGenerator():

    def __init__(self, default_insert_set:int=10000, default_insert_files:int=10, SQL_enable:bool=True, MQL_enable:bool=True, last_set_number:int=0) -> None:
        """This function initializes the DataGenerator class"""

        try:
            self._default_insert_set = default_insert_set
            self._default_insert_files = default_insert_files

            self._last_set_number = last_set_number + 1
            
            self._SQL_enable = SQL_enable
            self._MQL_enable = MQL_enable
            self._custom_facker = CustomFaker("en_US", 42)
            
            self._postgres_doctors_path = f"{Config().default_data['default_postgres_inserts']}Doctors/"
            self._postgres_patients_path = f"{Config().default_data['default_postgres_inserts']}Patients/"
            self._postgres_medicalrecords_path = f"{Config().default_data['default_postgres_inserts']}MedicalRecords/"
            self._postgres_doctor_medicalrecords_path = f"{Config().default_data['default_postgres_inserts']}Doctor_MedicalRecords/"

            self._mongo_doctors_path = f"{Config().default_data['default_mongo_inserts']}Doctors/"
            self._mongo_patients_path = f"{Config().default_data['default_mongo_inserts']}Patients/"
            self._mongo_medicalrecords_path = f"{Config().default_data['default_mongo_inserts']}MedicalRecords/"
            self._mongo_doctor_medicalrecords_path = f"{Config().default_data['default_mongo_inserts']}Doctor_MedicalRecords/"
        except:
            SingleLogger().logger.exception("Error while initializing DataGenerator", exc_info=True)

    def _create_patient(self, id:int) -> dict:
        """This function creates a patient with all their data"""

        return {
            # 'id_patient': str(id),
            'id_patient': id,
            'name': self.custom_facker.first_name(),
            'surname': self.custom_facker.last_name(),
            'birthday': self.custom_facker.date_of_birth(minimum_age=18, maximum_age=98),
            'gender': self.custom_facker.gender(),
            'address': self.custom_facker.street_address(),
            'city': self.custom_facker.city(),
            'state': self.custom_facker.state(),
            'phone': self.custom_facker.phone_number(),
        }

    def _create_medical_record(self, id:int) -> dict:
        """This function creates a medical record with all its data"""

        return {
            # 'id_medical_record': str(id),
            'id_medical_record': id,
            'id_patient': id,
            'admission_date': self.custom_facker.date_between(start_date='-5y', end_date='today'),
            'discharge_date': self.custom_facker.date_between(start_date='-5y', end_date='today'),
            'diagnosis': self.custom_facker.diagnosis(),  
            'treatment': self.custom_facker.treatment(),
            'test_result': self.custom_facker.test_result(),
        }

    def _create_doctor(self, id:int) -> dict:
        """This function creates a doctor with all their data"""

        return {
            #'id_doctor': str(id),
            'id_doctor': id,
            'name': self.custom_facker.first_name(),
            'surname': self.custom_facker.last_name(),
            'profession': self.custom_facker.profession(),
        }
    
    def generate_patients(self) -> None:
        """This function generates patients"""

        try:
            sets = lambda: "sets" if self.default_insert_files > 1 else "set"
            SingleLogger().logger.info(f"Generating data with {int(self.default_insert_set*self.default_insert_files)} patients and splitting them into {self.default_insert_files}...")
            start_counter = time.time()
            for i1 in tqdm(range(self._last_set_number, self._last_set_number + self.default_insert_files), desc="Generating "+str(self.default_insert_files)+" "+sets()+" of "+str(self.default_insert_set)+" patients", ascii=' #'):

                patients = []
                patients_sql = []
                patients_mql = []
                for i2 in tqdm(range(self.default_insert_set), desc="  Creating "+str(self.default_insert_set)+" patients", ascii=' #', leave=False):
                    patient = self._create_patient(i2 + 1 + ( (i1 - 1 ) * self.default_insert_set))
                    patients.append(patient)
                    if self.SQL_enable:
                        patients_sql.append(f"INSERT INTO patients (id_patient, name, surname, birthday, gender, address, city, state, phone) VALUES ('{patient['id_patient']}','{patient['name']}', '{patient['surname']}', '{patient['birthday']}', '{patient['gender']}', '{patient['address']}', '{patient['city']}', '{patient['state']}', '{patient['phone']}');")
                    if self.MQL_enable:
                        patients_mql.append({key: value if key != 'birthday' else value.strftime('%Y-%m-%d') for key, value in patient.items()})

                # Creating zip files for patients
                
                Zipper().zip_content(f"{self._postgres_patients_path}{self.default_insert_set}_patients_set{i1}", '\n'.join(map(str, patients_sql)),"sql")
                Zipper().zip_content(f"{self._mongo_patients_path}{self.default_insert_set}_patients_set{i1}", "db.patients.insertMany(["+',\n'.join(map(str, patients_mql))+"\n])","js")
            
            stop_counter = time.time()
            SingleLogger().logger.info(f"Done! Elapsed time: {stop_counter - start_counter} seconds")
            SingleLogger().logger.info("The data has been generated")
            del start_counter
            del stop_counter
            del patients
            del patients_sql
            del patients_mql
        except:
            SingleLogger().logger.exception("Error while generating patients with DataGenerator", exc_info=True)

    def generate_doctors(self) -> None:
        """This function generates doctors"""

        try:
            sets = lambda: "sets" if self.default_insert_files > 1 else "set"
            SingleLogger().logger.info(f"Generating data with {int(self.default_insert_set*self.default_insert_files)} doctors and splitting them into {self.default_insert_files}...")
            start_counter = time.time()                                                                 
            for i1 in tqdm(range(self._last_set_number, self._last_set_number + self.default_insert_files), desc="Generating "+str(self.default_insert_files)+" "+sets()+" of "+str(self.default_insert_set)+" doctors", ascii=' #'):
        
                doctors = []
                doctors_sql = []
                doctors_mql = []
                for i2 in tqdm(range(self.default_insert_set), desc="  Generating "+str(self.default_insert_set)+" doctors", ascii=' #', leave=False):
                    doctor = self._create_doctor(i2 + 1 + ( (i1 - 1 ) * self.default_insert_set))
                    doctors.append(doctor)
                    if self.SQL_enable:
                        doctors_sql.append(f"INSERT INTO doctors (id_doctor, name, surname, profession) VALUES ('{doctor['id_doctor']}','{doctor['name']}', '{doctor['surname']}', '{doctor['profession']}');")
                    if self.MQL_enable:
                        doctors_mql.append(doctor)

                # Creating zip files for doctors

                Zipper().zip_content(f"{self._postgres_doctors_path}{self.default_insert_set}_doctors_set{i1}", '\n'.join(map(str, doctors_sql)),"sql")
                Zipper().zip_content(f"{self._mongo_doctors_path}{self.default_insert_set}_doctors_set{i1}", "db.doctors.insertMany(["+',\n'.join(map(str, doctors_mql))+"\n])","js")
            
            stop_counter = time.time()
            SingleLogger().logger.info(f"Done! Elapsed time: {stop_counter - start_counter} seconds")
            SingleLogger().logger.info("The data has been generated")
            del start_counter
            del stop_counter
            del doctors
            del doctors_sql
            del doctors_mql
        except:
            SingleLogger().logger.exception("Error while generating doctors with DataGenerator", exc_info=True)

    def generate_medicalrecords(self) -> None:
        """This function generates medical records"""

        try:
            sets = lambda: "sets" if self.default_insert_files > 1 else "set"
            SingleLogger().logger.info(f"Generating data with {int(self.default_insert_set*self.default_insert_files)} doctors and splitting them into {self.default_insert_files}...")
            start_counter = time.time()                                                                 
            for i1 in tqdm(range(self._last_set_number, self._last_set_number + self.default_insert_files), desc="Generating "+str(self.default_insert_files)+" "+sets()+" of "+str(self.default_insert_set)+" doctor medical records", ascii=' #'):

                medicalrecords = []
                medicalrecords_sql = []
                medicalrecords_mql = []
                doctor_medicalrecords_sql = []
                doctor_medicalrecords_mql = []
                for i2 in tqdm(range(self.default_insert_set), desc="  Generating "+str(self.default_insert_set)+" medical records", ascii=' #', leave=False):
                    record = self._create_medical_record(i2 + 1 + ( (i1 - 1 ) * self.default_insert_set))
                    record_dmr = f"INSERT INTO doctor_medical_records (id_doctor, id_medical_record) VALUES ('{i2 + 1 + ( (i1 - 1 ) * self.default_insert_set)}','{record['id_medical_record']}');"
                    doctor_medicalrecords_sql.append(record_dmr)
                    doctor_medicalrecords_mql.append(f"{{'id_doctor': {i2 + 1 + ( (i1 - 1 ) * self.default_insert_set)}, 'id_medicalrecord': {i2 + 1 + ( (i1 - 1 ) * self.default_insert_set)}}}")
                    medicalrecords.append(record)
                    medicalrecords_sql.append(f"INSERT INTO medical_records (id_medical_record, id_patient, admission_date, discharge_date, diagnosis, treatment, test_results) VALUES ({record['id_medical_record']}, {record['id_patient']},'{record['admission_date']}', '{record['discharge_date']}', '{record['diagnosis']}', '{record['treatment']}', '{record['test_result']}');")
                    medicalrecords_mql.append({key: value if key != 'admission_date' and key != 'discharge_date' else value.strftime('%Y-%m-%d') for key, value in record.items()})

                # Creating zip files for medical records
                    
                Zipper().zip_content(f"{self._postgres_medicalrecords_path}{self.default_insert_set}_medicalrecords_set{i1}", '\n'.join(map(str, medicalrecords_sql)),"sql")
                Zipper().zip_content(f"{self._mongo_medicalrecords_path}{self.default_insert_set}_medicalrecords_set{i1}", "db.medical_records.insertMany(["+',\n'.join(map(str, medicalrecords_mql))+"\n])","js")

                # Creating zip files for doctor medical records

                Zipper().zip_content(f"{self._postgres_doctor_medicalrecords_path}{self.default_insert_set}_doctor_medicalrecords_set{i1}", '\n'.join(map(str, doctor_medicalrecords_sql)),"sql")
                Zipper().zip_content(f"{self._mongo_doctor_medicalrecords_path}{self.default_insert_set}_doctor_medicalrecords_set{i1}", "db.doctor_medical_records.insertMany(["+',\n'.join(map(str, doctor_medicalrecords_mql))+"\n])","js")
            
            stop_counter = time.time()
            SingleLogger().logger.info(f"Done! Elapsed time: {stop_counter - start_counter} seconds")
            SingleLogger().logger.info("The data has been generated")
            del start_counter
            del stop_counter
            del record
            del record_dmr
            del medicalrecords
            del medicalrecords_sql
            del medicalrecords_mql
            del doctor_medicalrecords_sql
            del doctor_medicalrecords_mql
        except:
            SingleLogger().logger.exception("Error while generating medical records with DataGenerator", exc_info=True)
    
    def update_config(self, number_of_files:int=0):
        """This function updates the config values with the new numbers of items per sets and number of files"""

        try:
            Config().option_create_modify("Memory","default_insert_set",str(self._default_insert_set))
            if number_of_files == 0:
                Config().option_create_modify("Memory","default_insert_files",str(self._default_insert_files))
            else:
                Config().option_create_modify("Memory","default_insert_files",str(number_of_files))
        except:
            SingleLogger().logger.exception("Error while updating config file on DataGenerator", exc_info=True)

    def check_previous_sets(self):
        """List all files in a directory that match a given pattern"""

        try:
            sets = {}

            # First check for doctors

            for root, dirs, files in os.walk(self._postgres_doctors_path):
                for filename in files:
                    if re.match(r'\d+_(doctors)_set\d+\.zip', filename):
                        rows_per_set = re.match(r'^(\d+)_', filename).group(1)
                        if rows_per_set:
                            if str(rows_per_set) in sets:
                                sets[str(rows_per_set)].append(str(filename))
                            else:
                                sets.update({str(rows_per_set): [str(filename)]})
            
            sets = self.get_common_filenames(self._mongo_doctors_path,"doctors", sets)
            sets = self.get_common_filenames(self._postgres_patients_path,"patients", sets)
            sets = self.get_common_filenames(self._mongo_patients_path,"patients", sets)
            sets = self.get_common_filenames(self._postgres_medicalrecords_path,"medicalrecords", sets)
            sets = self.get_common_filenames(self._mongo_medicalrecords_path,"medicalrecords", sets)
            sets = self.get_common_filenames(self._postgres_doctor_medicalrecords_path,"doctor_medicalrecords", sets)

            return sets
        except:
            SingleLogger().logger.exception("Error while checking previous sets on DataGenerator", exc_info=True)
    
    def get_common_filenames(self, path, entity, previous_dict):
        """This function return a dictionary with the datasets available"""
        
        try:
            temp_dict = {}

            for root, dirs, files in os.walk(path):
                for filename in files:
                    if re.match(r'\d+_('+entity+')_set\d+\.zip', filename):
                        rows_per_set = re.match(r'^(\d+)_', filename).group(1)
                        if rows_per_set and rows_per_set in previous_dict:
                            if str(rows_per_set) in temp_dict:
                                temp_dict[str(rows_per_set)].append(str(filename))
                            else:
                                temp_dict.update({str(rows_per_set): [str(filename)]})

            for key, value in temp_dict.items():
                if not len(value) == len(previous_dict[key]):
                    del temp_dict[key]

            return temp_dict
        except:
            SingleLogger().logger.exception("Error while getting common filenames on DataGenerator", exc_info=True)

    @property
    def SQL_enable(self) -> bool:
        return self._SQL_enable
    
    @SQL_enable.setter
    def SQL_enable(self, value:bool):
        self.SQL_enable = value

    @property
    def MQL_enable(self) -> bool:
        return self._MQL_enable
    
    @MQL_enable.setter
    def MQL_enable(self, value:bool):
        self.MQL_enable = value

    @property
    def default_insert_set(self) -> int:
        return self._default_insert_set
    
    @default_insert_set.setter
    def default_insert_set(self, value:int):
        self._default_insert_set = value
        
    @property
    def default_insert_files(self) -> int:
        return self._default_insert_files
    
    @default_insert_files.setter
    def default_insert_files(self, value:int):
        self._default_insert_files = value

    @property
    def custom_facker(self):
        return self._custom_facker
    
    @custom_facker.setter
    def custom_facker(self, value):
        self._custom_facker = value