
from Queries.PostgreSQL.randomdata import diagnosis, treatment, test_result
from faker import Faker
import random

faker = Faker()
faker.seed_instance(42)  # Set data consistency

# Setting locale
faker = Faker('en_US')

# Generate patients
def generate_patient():
    return {
        'id_patient': faker.unique.random_number(digits=8),
        'name': faker.first_name(),
        'surname': faker.last_name(),
        'birthday': faker.date_of_birth(minimum_age=18, maximum_age=90),
        'gender': random.choice(['Masculino', 'Femenino']),
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

number_of_rows = 10000

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
print("Creating SQL file for patients...")
with open('Queries/PostgreSQL/Inserts/InsertPatients'+str(number_of_rows)+'.sql', 'w') as file:
    for patient in patients:
        file.write(f"INSERT INTO patients (id_patient, name, surname, birthday, gender, address, city, state, phone) VALUES ('{patient['id_patient']}','{patient['name']}', '{patient['surname']}', '{patient['birthday']}', '{patient['gender']}', '{patient['address']}', '{patient['city']}', '{patient['state']}', '{patient['phone']}');\n")

print("Creating SQL file for doctors...")
with open('Queries/PostgreSQL/Inserts/InsertDoctors'+str(number_of_rows)+'.sql', 'w') as file:
    for doctor in doctors:
        file.write(f"INSERT INTO doctors (id_doctor, name, surname, profession) VALUES ('{doctor['id_doctor']}','{doctor['name']}', '{doctor['surname']}', '{doctor['profession']}');\n")

print("Creating SQL file for the relationships among patients, doctors and medical records...")
with open('Queries/PostgreSQL/Inserts/InsertPatientDoctorMedicalRecord'+str(number_of_rows)+'.sql', 'w') as file:
    for record in medical_records:
        file.write(f"INSERT INTO patient_doctor_medical_record (id_patient, id_doctor, id_medical_record) VALUES ('{patient_doctor[0][0]['id_patient']}','{patient_doctor[0][1]['id_doctor']}','{record['id_medical_record']}');\n")
        record['id_patient'] = patient_doctor[0][0]['id_patient']
        del patient_doctor[0]

print("Creating SQL file for medical records...")
with open('Queries/PostgreSQL/Inserts/InsertMedicalRecords'+str(number_of_rows)+'.sql', 'w') as file:
    for record in medical_records:
        file.write(f"INSERT INTO medical_records (id_medical_record, id_patient, admission_date, discharge_date, diagnosis, treatment, test_results) VALUES ({record['id_medical_record']}, {record['id_patient']},'{record['admission_date']}', '{record['discharge_date']}', '{record['diagnosis']}', '{record['treatment']}', '{record['test_result']}');\n")
