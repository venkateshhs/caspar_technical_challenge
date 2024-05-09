CREATE DATABASE hospital_database;

CREATE TABLE hospital_database.patients (
    patient_id INT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    country VARCHAR(255)
);

CREATE TABLE hospital_database.exercises (
    id INT PRIMARY KEY,
    external_id INT,
    minutes INT,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (external_id) REFERENCES patients(patient_id)
);
CREATE TABLE hospital_database.steps (
    id INT PRIMARY KEY,
	external_id INT,
    steps INT,
    submission_time TIMESTAMP,
    updated_at TIMESTAMP,
	FOREIGN KEY (external_id) REFERENCES patients(patient_id)
);


select count(*) from steps;
select count(*) from exercises;
select count(*) from patients;


