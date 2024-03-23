
from CustomFaker import CustomFaker
from tqdm import tqdm
import random
import zipfile
import io
import os
import json

####################### Variables ###########################

number_of_rows = 1000000
rows_per_file = 100000


#############################################################

custom_facker = CustomFaker("en_US", 42)

def generate_patient(id:int):
    return {
        #'id_patient': custom_facker.unique.random_number(digits=8),
        'id_patient': str(id),
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

def generate_medical_record(id:int,id_patient:int):
    return {
        #'id_medical_record': custom_facker.unique.random_number(digits=14),
        'id_medical_record': str(id),
        'id_patient': id_patient,
        'admission_date': custom_facker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),  # Convert date to string,
        'discharge_date': custom_facker.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),  # Convert date to string,
        'diagnosis': custom_facker.diagnosis(),  
        'treatment': custom_facker.treatment(),
        'test_result': custom_facker.test_result(),
    }



#Generate doctor

def generate_doctor(id:int):
    return {
        #'id_doctor': custom_facker.unique.random_number(digits=8),
        'id_doctor': str(id),
        'name': custom_facker.first_name(),
        'surname': custom_facker.last_name(),
        'profession': custom_facker.profession(),
    }



# Generate patients
print("Generating patients...") 

patients = []
for i in tqdm(range(number_of_rows), desc="Generating "+str(number_of_rows)+" patients", ascii=' #'):
    patient = generate_patient(i)
    patients.append(patient)
insert_p_many_json = json.dumps(patients)
# Convertir la cadena a bytes antes de escribirla en el archivo ZIP
insert_p_many_bytes = ("db.patient_documents.insertMany(" + insert_p_many_json + ")").encode()


# Generate doctors
print("Generating doctors...") 

doctors = []
for i in tqdm(range(number_of_rows), desc="Generating "+str(number_of_rows)+" doctors", ascii=' #'):
    doctor = generate_doctor(i)
    doctors.append(doctor)
insert_d_many_json = json.dumps(doctors)
# Convertir la cadena a bytes antes de escribirla en el archivo ZIP
insert_d_many_bytes = ("db.doctor_documents.insertMany(" + insert_d_many_json + ")").encode()
 


# Generate medical records for each patient
print("Generating medical records... and relationship between doctor and medical records")

medicalrecords = []
doctormedicalrecords = []
for i in tqdm(range(number_of_rows), desc="Generating "+str(number_of_rows)+" medical records", ascii=' #'):
    record = generate_medical_record(i,patients[i]['id_patient'])

    doctormedicalrecords.append({
            'id_doctor': doctors[i]['id_doctor'],
            'id_medical_record': i
        })
    medicalrecords.append(record)
insert_mr_many_json = json.dumps(medicalrecords)
# Convertir la cadena a bytes antes de escribirla en el archivo ZIP
insert_mr_many_bytes = ("db.medicalrecords_documents.insertMany(" + insert_mr_many_json + ")").encode()

insert_dmr_many_json = json.dumps(doctormedicalrecords)
# Convertir la cadena a bytes antes de escribirla en el archivo ZIP
insert_dmr_many_bytes = ("db.doctormedicalrecord_documents.insertMany(" + insert_dmr_many_json + ")").encode()



# Creation of NoSQL files in order to populate tables
    
def create_folder(path:str):
    try:
        if not os.path.exists(path):
            print("Creating folder: "+path)
            os.makedirs(path)
    except Exception as error:
        print("An error occured during the creation of path "+path+". The exception is: "+ error)




doctors_path = "data/Mongo/Inserts/Doctors/"
patients_path = "data/Mongo/Inserts/Patients/"
medicalrecords_path = "data/Mongo/Inserts/MedicalRecords/"
doctor_medicalrecords_path = "data/Mongo/Inserts/Doctor_MedicalRecords/"


# Calculation of number of files and rows per file

number_of_files = int(number_of_rows/rows_per_file)
if rows_per_file == 0 and number_of_rows != 0:
    rows_per_file = number_of_rows
    number_of_files = 1

# if paths don't exist

create_folder(doctors_path)
create_folder(patients_path)
create_folder(medicalrecords_path)
create_folder(doctor_medicalrecords_path)


print("Creating Zip file for patient documents...")
with zipfile.ZipFile(patients_path + str(number_of_rows) + '_patients_documents.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Escribir la cadena de bytes en el archivo ZIP
    zipf.writestr(str(number_of_rows) + '_patients_documents.js', insert_p_many_bytes)


print("Creating Zip file for doctor documents...")
with zipfile.ZipFile(doctors_path+str(number_of_rows)+'_doctors_documents.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Escribir la cadena de bytes en el archivo ZIP
    zipf.writestr(str(number_of_rows) + '_doctors_documents.js', insert_d_many_bytes)


print("Creating Zip file for medical record documents...")
with zipfile.ZipFile(medicalrecords_path+str(number_of_rows)+'_medicalrecords_documents.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Escribir la cadena de bytes en el archivo ZIP
    zipf.writestr(str(number_of_rows) + '_medicalrecords_documents.js', insert_mr_many_bytes)


print("Creating Zip file for the relationships among doctors and medical records (documents)...")
with zipfile.ZipFile( doctor_medicalrecords_path+ str(number_of_rows) + '_doctor_medicalrecords_documents.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Escribir la cadena de bytes en el archivo ZIP
    zipf.writestr(str(number_of_rows) + '_doctor_medicalrecords_documents.js', insert_dmr_many_bytes)


