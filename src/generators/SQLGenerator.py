from CustomFaker import CustomFaker
from tqdm import tqdm
import zipfile
import io
import os


####################### Variables ###########################

number_of_rows = 15000
rows_per_file = 1000

#############################################################

custom_facker = CustomFaker("en_US", 42)

# Generate patients

def generate_patient(id:int):
    return {
        #'id_patient': custom_facker.unique.random_number(digits=8),
        'id_patient': str(id),
        'name': custom_facker.first_name(),
        'surname': custom_facker.last_name(),
        'birthday': custom_facker.date_of_birth(minimum_age=18, maximum_age=98),
        'gender': custom_facker.gender(),
        'address': custom_facker.street_address(),
        'city': custom_facker.city(),
        'state': custom_facker.state(),
        'phone': custom_facker.phone_number(),
    }

# Generate medical record

def generate_medical_record(id:int):
    return {
        #'id_medical_record': custom_facker.unique.random_number(digits=14),
        'id_medical_record': str(id),
        'id_patient': None,
        'admission_date': custom_facker.date_between(start_date='-5y', end_date='today'),
        'discharge_date': custom_facker.date_between(start_date='-5y', end_date='today'),
        'diagnosis': custom_facker.diagnosis(),  
        'treatment': custom_facker.treatment(),
        'test_result': custom_facker.test_result(),
    }

# Generate doctor

def generate_doctor(id:int):
    return {
        #'id_doctor': custom_facker.unique.random_number(digits=8),
        'id_doctor': str(id),
        'name': custom_facker.first_name(),
        'surname': custom_facker.last_name(),
        'profession': custom_facker.profession(),
    }

# Generate patients

patients = []
patients_sql = []
for i in tqdm(range(number_of_rows), desc="Generating "+str(number_of_rows)+" patients", ascii=' #'):
    patient = generate_patient(i)
    patients.append(patient)
    patients_sql.append(f"INSERT INTO patients (id_patient, name, surname, birthday, gender, address, city, state, phone) VALUES ('{patient['id_patient']}','{patient['name']}', '{patient['surname']}', '{patient['birthday']}', '{patient['gender']}', '{patient['address']}', '{patient['city']}', '{patient['state']}', '{patient['phone']}');")

# # Generate doctors
    
doctors = []
doctors_sql = []
for i in tqdm(range(number_of_rows), desc="Generating "+str(number_of_rows)+" doctors", ascii=' #'):
    doctor = generate_doctor(i)
    doctors.append(doctor)
    doctors_sql.append(f"INSERT INTO doctors (id_doctor, name, surname, profession) VALUES ('{doctor['id_doctor']}','{doctor['name']}', '{doctor['surname']}', '{doctor['profession']}');")

# # Generate medical records for each patient

medicalrecords = []
medicalrecords_sql = []
doctor_medicalrecords = []
doctor_medicalrecords_sql = []
for i in tqdm(range(number_of_rows), desc="Generating "+str(number_of_rows)+" medical records", ascii=' #'):
    record = generate_medical_record(i)
    record_dmr = "INSERT INTO doctor_medical_records (id_doctor, id_medical_record) VALUES ('"+str(doctors[i]['id_doctor'])+"','"+str(record['id_medical_record'])+"');"  
    doctor_medicalrecords.append(record_dmr)
    doctor_medicalrecords_sql.append(record_dmr)
    medicalrecords.append(record)
    medicalrecords_sql.append(f"INSERT INTO medical_records (id_medical_record, id_patient, admission_date, discharge_date, diagnosis, treatment, test_results) VALUES ({record['id_medical_record']}, {patients[i]['id_patient']},'{record['admission_date']}', '{record['discharge_date']}', '{record['diagnosis']}', '{record['treatment']}', '{record['test_result']}');")

# Creation of files

def create_folder(path:str):
    try:
        if not os.path.exists(path):
            print("Creating folder: "+path)
            os.makedirs(path)
    except Exception as error:
        print("An error occured during the creation of path "+path+". The exception is: "+ error)

def create_sql_file(filepath:str, content:str, zip:bool=False):
    """This functions generate a file with the content provided. The file can be zipped or not"""
    try:
        (filepath, extension) = os.path.splitext(filepath)
        if zip:
            with zipfile.ZipFile(filepath+".zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
                basename = os.path.basename(filepath)
                zipf.writestr(basename+".sql", io.BytesIO(content.encode()).getvalue(), compresslevel=9)
        else:
            with open(filepath+'.sql', 'w') as file:
                file.write(content)
    except Exception as error:
        print("There is an error creating a file. Error: "+error)

# Calculation of number of files and rows per file

number_of_files = int(number_of_rows/rows_per_file)
if rows_per_file == 0 and number_of_rows != 0:
    rows_per_file = number_of_rows
    number_of_files = 1

doctors_path = "data/PostgreSQL/Inserts/Doctors/"
patients_path = "data/PostgreSQL/Inserts/Patients/"
medicalrecords_path = "data/PostgreSQL/Inserts/MedicalRecords/"
doctor_medicalrecords_path = "data/PostgreSQL/Inserts/Doctor_MedicalRecords/"

# if paths don't exist

create_folder(doctors_path)
create_folder(patients_path)
create_folder(medicalrecords_path)
create_folder(doctor_medicalrecords_path)

for i in tqdm(range(number_of_files), desc="Creating "+str(number_of_files)+" doctors zip files", ascii=' #'):
    create_sql_file(doctors_path+str(rows_per_file)+"_doctors_set"+str(i), '\n'.join(map(str, doctors_sql[rows_per_file*i:rows_per_file*(i+1)])),True)

for i in tqdm(range(number_of_files), desc="Creating "+str(number_of_files)+" patient zip files", ascii=' #'):
    create_sql_file(patients_path+str(rows_per_file)+"_patients_set"+str(i), '\n'.join(map(str, patients_sql[rows_per_file*i:rows_per_file*(i+1)])),True)

for i in tqdm(range(number_of_files), desc="Creating "+str(number_of_files)+" medical record zip files", ascii=' #'):
    create_sql_file(medicalrecords_path+str(rows_per_file)+"_medicalrecords_set"+str(i), '\n'.join(map(str, medicalrecords_sql[rows_per_file*i:rows_per_file*(i+1)])),True)

for i in tqdm(range(number_of_files), desc="Creating "+str(number_of_files)+" doctor medicalrecord zip files", ascii=' #'):
    create_sql_file(doctor_medicalrecords_path+str(rows_per_file)+"_doctor_medicalrecords_set"+str(i), '\n'.join(map(str, doctor_medicalrecords_sql[rows_per_file*i:rows_per_file*(i+1)])),True)