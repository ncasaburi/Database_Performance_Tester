
from CustomFaker import CustomFaker
from tqdm import tqdm
import random
import zipfile
import io
import os
import json

####################### Variables ###########################

number_of_rows = 100

#############################################################

custom_facker = CustomFaker("en_US", 42)

# Generate patients
# def generate_patient():
#     return {
#         'id_patient': faker.unique.random_number(digits=8),
#         'name': faker.first_name(),
#         'surname': faker.last_name(),
#         #'birthday': faker.date_of_birth(minimum_age=18, maximum_age=90),
#         'birthday': faker.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d'),  # Convert date to string
#         'gender': random.choice(['Male', 'Female']),
#         #'address': faker.street_address(),
#         #'city': faker.city(),
#         #'state': faker.state(),
#         #'phone': faker.phone_number(),
#     }

def generate_patient():
    return {
        'id_patient': custom_facker.unique.random_number(digits=8),
        'name': custom_facker.first_name(),
        'surname': custom_facker.last_name(),
        'birthday': custom_facker.date_of_birth(minimum_age=18, maximum_age=98).strftime('%Y-%m-%d'),  # Convert date to string,
        'gender': custom_facker.gender(),
        'address': custom_facker.street_address(),
        'city': custom_facker.city(),
        'state': custom_facker.state(),
        'phone': custom_facker.phone_number(),
    }

# Generate medical record
# def generate_medical_record():
#     return {
#         'id_medical_record': faker.unique.random_number(digits=14),
#         'admission_date': faker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
#         'discharge_date': faker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
#         'diagnosis': random.choice(diagnosis()),  
#         'treatment': random.choice(treatment()),
#         'test_result': random.choice(test_result())
#     }

# Generate medical record

def generate_medical_record(id_patient):
    return {
        'id_medical_record': custom_facker.unique.random_number(digits=14),
        'id_patient': id_patient,
        'admission_date': custom_facker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),  # Convert date to string,
        'discharge_date': custom_facker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),  # Convert date to string,
        'diagnosis': custom_facker.diagnosis(),  
        'treatment': custom_facker.treatment(),
        'test_result': custom_facker.test_result(),
    }


# Generate doctor
# def generate_doctor():
#     return {
#         'id_doctor': faker.unique.random_number(digits=8),
#         'name': faker.first_name(),
#         'surname': faker.last_name(),
#         'profession': random.choice(['Cardiology', 'Pediatrics', 'Gynecology', 'Ophthalmology', 'Dermatology']),
#     }


#Generate doctor

def generate_doctor():
    return {
        'id_doctor': custom_facker.unique.random_number(digits=8),
        'name': custom_facker.first_name(),
        'surname': custom_facker.last_name(),
        'profession': custom_facker.profession(),
    }



# Generate patients
print("Generating patients...")
patients = [generate_patient() for _ in range(number_of_rows)]

# Generate medical records for each patient
print("Generating medical records...")
medical_records = []
for patient in patients:
    medical_records.append(generate_medical_record(patient['id_patient']))


# Generate doctors
print("Generating doctors...") 
doctors = [generate_doctor() for _ in range(number_of_rows)]

# Create a unique relation between doctors and patients
perm = random.sample(range(number_of_rows), number_of_rows)
patient_doctor = []
for i in perm:
    patient_doctor.append((patients[i], doctors[i]))


# Creation of NoSQL files in order to populate tables

# if the path doesn't exist
current_path = "data/Mongo/Inserts/"+str(number_of_rows)+os.path.sep
if not os.path.exists(current_path):
    os.makedirs(current_path)


print("Creating Zip file for patient documents...")
with zipfile.ZipFile(current_path + str(number_of_rows) + '_Patient_Documents.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    
    insert_many_json = json.dumps(patients)
    # Convertir la cadena a bytes antes de escribirla en el archivo ZIP
    insert_many_bytes = ("db.patient_documents.insertMany(" + insert_many_json + ")").encode()
    # Escribir la cadena de bytes en el archivo ZIP
    zipf.writestr(str(number_of_rows) + '_Patient_Documents.js', insert_many_bytes)


print("Creating Zip file for doctor documents...")
with zipfile.ZipFile(current_path+str(number_of_rows)+'_Doctor_Documents.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    insert_many_json = json.dumps(doctors)
    # Convertir la cadena a bytes antes de escribirla en el archivo ZIP
    insert_many_bytes = ("db.doctor_documents.insertMany(" + insert_many_json + ")").encode()
    # Escribir la cadena de bytes en el archivo ZIP
    zipf.writestr(str(number_of_rows) + '_Doctor_Documents.js', insert_many_bytes)


print("Creating Zip file for medical record documents...")
with zipfile.ZipFile(current_path+str(number_of_rows)+'_MedicalRecord_Documents.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    insert_many_json = json.dumps(medical_records)
    # Convertir la cadena a bytes antes de escribirla en el archivo ZIP
    insert_many_bytes = ("db.medicalrecords_documents.insertMany(" + insert_many_json + ")").encode()
    # Escribir la cadena de bytes en el archivo ZIP
    zipf.writestr(str(number_of_rows) + '_MedicalRecord_Documents.js', insert_many_bytes)


print("Creating Zip file for the relationships among patients, doctors and medical records (documents)...")
with zipfile.ZipFile(current_path + str(number_of_rows) + '_DoctorMedicalRecord_Documents.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    patient_doctor_medical_records_in_memory = []
    for record in medical_records:
        patient_doctor_medical_records_in_memory.append({
            'id_doctor': patient_doctor[0][1]['id_doctor'],
            'id_medical_record': record['id_medical_record']
        })
        record['id_patient'] = patient_doctor[0][0]['id_patient']
        del patient_doctor[0]
    insert_many_json = json.dumps(patient_doctor_medical_records_in_memory)
    # Convertir la cadena a bytes antes de escribirla en el archivo ZIP
    insert_many_bytes = ("db.doctormedicalrecord_documents.insertMany(" + insert_many_json + ")").encode()
    # Escribir la cadena de bytes en el archivo ZIP
    zipf.writestr(str(number_of_rows) + '_DoctorMedicalRecord_Documents.js', insert_many_bytes)


