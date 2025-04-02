-- Create the database
CREATE DATABASE drug_allergy_system;
USE drug_allergy_system;

-- Create patients table
CREATE TABLE patients (
    Patient_ID INT PRIMARY KEY AUTO_INCREMENT,
    Age INT,
    Gender VARCHAR(10),
    Weight_kg INT,
    Height_cm INT,
    BMI INT,
    Chronic_conditions VARCHAR(100),
    Drug_allergies VARCHAR(100),
    Genetic_Disorders VARCHAR(120),
    Diagnosis VARCHAR(110),
    Symptoms VARCHAR(200),
    Fingerprint_ID VARCHAR(255)
);

-- Create allergies table
CREATE TABLE allergies (
    Allergy_ID INT PRIMARY KEY AUTO_INCREMENT,
    Patient_ID INT,
    Allergy_Name VARCHAR(100),
    Severity VARCHAR(50),
    FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID) ON DELETE CASCADE
);

-- Create medications table
CREATE TABLE medications (
    Medication_ID INT PRIMARY KEY AUTO_INCREMENT,
    Medication_Name VARCHAR(100),
    Recommended_For VARCHAR(100)
);

-- Create recommended_medications table
CREATE TABLE recommended_medications (
    Record_ID INT PRIMARY KEY AUTO_INCREMENT,
    Patient_ID INT,
    Allergy_ID INT,
    Medication_ID INT,
    Dosage VARCHAR(100),
    Duration VARCHAR(100),
    Recovery_Time_Days INT,
    FOREIGN KEY (Patient_ID) REFERENCES patients(Patient_ID) ON DELETE CASCADE,
    FOREIGN KEY (Allergy_ID) REFERENCES allergies(Allergy_ID) ON DELETE CASCADE,
    FOREIGN KEY (Medication_ID) REFERENCES medications(Medication_ID) ON DELETE CASCADE
);

-- Insert sample data (Modify values before running)
INSERT INTO patients (Age, Gender, Weight_kg, Height_cm, BMI, Chronic_conditions, Drug_allergies, Genetic_Disorders, Diagnosis, Symptoms, Fingerprint_ID) 
VALUES 
(30, 'Male', 75, 180, 23, 'Diabetes', 'Penicillin', 'None', 'Flu', 'Fever, Cough, Headache', 'FP123456');

INSERT INTO allergies (Patient_ID, Allergy_Name, Severity) 
VALUES (1, 'Penicillin Allergy', 'Severe');

INSERT INTO medications (Medication_Name, Recommended_For) 
VALUES ('Paracetamol', 'Fever');

INSERT INTO recommended_medications (Patient_ID, Allergy_ID, Medication_ID, Dosage, Duration, Recovery_Time_Days) 
VALUES (1, 1, 1, '500mg', '3 Days', 5);

-- Retrieve all data
SELECT * FROM patients;
SELECT * FROM allergies;
SELECT * FROM medications;
SELECT * FROM recommended_medications;
