
from randomdata import diagnosis, treatment, test_result
from faker import Faker
import random
import zipfile
import io
import os

####################### Variables ###########################

data_language = "en_US"
number_of_rows = 500000

#############################################################

faker = Faker()
faker.seed_instance(42)  # Set data consistency

# Setting locale
faker = Faker(data_language)

# Generate patients
def generate_patient():
    return {
        'id_patient': faker.unique.random_number(digits=8),
        'name': faker.first_name(),
        'surname': faker.last_name(),
        'birthday': faker.date_of_birth(minimum_age=18, maximum_age=90),
        'gender': random.choice(['Male', 'Female']),
        'address': faker.street_address(),
        'city': faker.city(),
        'state': faker.state(),
        'phone': faker.phone_number(),
    }

# Generate medical record
def generate_medical_record():
    return {
        'id_medical_record': faker.unique.random_number(digits=14),
        'admission_date': faker.date_between(start_date='-5y', end_date='today'),
        'discharge_date': faker.date_between(start_date='-5y', end_date='today'),
        'diagnosis': random.choice(diagnosis()),  
        'treatment': random.choice(treatment()),
        'test_result': random.choice(test_result())
    }

# Generate doctor
def generate_doctor():
    return {
        'id_doctor': faker.unique.random_number(digits=8),
        'name': faker.first_name(),
        'surname': faker.last_name(),
        'profession': random.choice(['Cardiology', 'Pediatrics', 'Gynecology', 'Ophthalmology', 'Dermatology']),
    }

# Generate patients
print("Generating patients...")
patients = [generate_patient() for _ in range(number_of_rows)]

# Generate medical records for each patient
print("Generating medical records...")
medical_records = []
for patient in patients:
    medical_records.append(generate_medical_record())

# Generate doctors
print("Generating doctors...") 
doctors = [generate_doctor() for _ in range(number_of_rows)]

# Create a unique relation between doctors and patients
perm = random.sample(range(number_of_rows), number_of_rows)
patient_doctor = []
for i in perm:
    patient_doctor.append((patients[i], doctors[i]))

# Creation of SQL files in order to populate tables

# if the path doesn't exist
current_path = "Queries/PostgreSQL/Inserts/"+str(number_of_rows)+os.path.sep
if not os.path.exists(current_path):
    os.makedirs(current_path)

print("Creating Zip file for patients...")
with zipfile.ZipFile(current_path+str(number_of_rows)+'_Patients.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    patients_in_memory = ""
    for patient in patients:
        patients_in_memory = patients_in_memory + (f"INSERT INTO patients (id_patient, name, surname, birthday, gender, address, city, state, phone) VALUES ('{patient['id_patient']}','{patient['name']}', '{patient['surname']}', '{patient['birthday']}', '{patient['gender']}', '{patient['address']}', '{patient['city']}', '{patient['state']}', '{patient['phone']}');\n")
    zipf.writestr(str(number_of_rows)+'_Patients.sql', io.BytesIO(patients_in_memory.encode()).getvalue())

print("Creating Zip file for doctors...")
with zipfile.ZipFile(current_path+str(number_of_rows)+'_Doctors.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    doctors_in_memory = ""
    for doctor in doctors:
        doctors_in_memory = doctors_in_memory + (f"INSERT INTO doctors (id_doctor, name, surname, profession) VALUES ('{doctor['id_doctor']}','{doctor['name']}', '{doctor['surname']}', '{doctor['profession']}');\n")
    zipf.writestr(str(number_of_rows)+'_Doctors.sql', io.BytesIO(doctors_in_memory.encode()).getvalue())

print("Creating Zip file for the relationships among patients, doctors and medical records...")
with zipfile.ZipFile(current_path+str(number_of_rows)+'_PatientDoctorMedicalRecord.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    patient_doctor_medical_records_in_memory = ""
    for record in medical_records:
        patient_doctor_medical_records_in_memory = patient_doctor_medical_records_in_memory + (f"INSERT INTO patient_doctor_medical_record (id_patient, id_doctor, id_medical_record) VALUES ('{patient_doctor[0][0]['id_patient']}','{patient_doctor[0][1]['id_doctor']}','{record['id_medical_record']}');\n")
        record['id_patient'] = patient_doctor[0][0]['id_patient']
        del patient_doctor[0]
    zipf.writestr(str(number_of_rows)+'_PatientDoctorMedicalRecord.sql', io.BytesIO(patient_doctor_medical_records_in_memory.encode()).getvalue())

print("Creating Zip file for medical records...")
with zipfile.ZipFile(current_path+str(number_of_rows)+'_MedicalRecords.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    medical_records_in_memory = ""
    for record in medical_records:
        medical_records_in_memory = medical_records_in_memory + (f"INSERT INTO medical_records (id_medical_record, id_patient, admission_date, discharge_date, diagnosis, treatment, test_results) VALUES ({record['id_medical_record']}, {record['id_patient']},'{record['admission_date']}', '{record['discharge_date']}', '{record['diagnosis']}', '{record['treatment']}', '{record['test_result']}');\n")
    zipf.writestr(str(number_of_rows)+'_MedicalRecords.sql', io.BytesIO(medical_records_in_memory.encode()).getvalue(), compresslevel=9)