-- Create patient table
CREATE TABLE patients (
    id_patient SERIAL PRIMARY KEY,
    name VARCHAR(100),
    surname VARCHAR(100),
    birthday DATE,
    gender VARCHAR(20),
    address VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(100),
    phone VARCHAR(50)
);

-- Create medical record table
CREATE TABLE medical_records (
    id_medical_record BIGSERIAL PRIMARY KEY,
    id_patient INTEGER REFERENCES patients(id_patient),
    admission_date DATE,
    discharge_date DATE,
    diagnosis TEXT,
    treatment TEXT,
    test_results TEXT
);

-- Create doctor table
CREATE TABLE doctors (
    id_doctor SERIAL PRIMARY KEY,
    name VARCHAR(100),
    surname VARCHAR(100),
    profession VARCHAR(100)
);

-- Create table with the relation among patient, doctor and medical record
CREATE TABLE patient_doctor_medical_record (
    id_patient INTEGER REFERENCES patients(id_patient),
    id_doctor INTEGER REFERENCES doctors(id_doctor),
    id_medical_record BIGINT REFERENCES medical_records(id_medical_record),
    PRIMARY KEY (id_patient, id_doctor)
);

