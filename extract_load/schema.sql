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


--Insert another column to store generated minutes
ALTER TABLE steps ADD COLUMN generated_minutes FLOAT;



-- just to check schema
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'steps';

SELECT table_name, column_name
FROM information_schema.columns
WHERE table_name IN ('steps', 'exercises', 'patients');


-- renames STEPS column to footsteps to remove ambuguity and casting errors while converting steps
ALTER TABLE steps RENAME COLUMN "STEPS" TO footsteps;

UPDATE steps SET generated_minutes = CAST(footsteps AS double precision) * 0.002;

-- Intermediate Aggregate total minutes from both steps and exercises
-- verified with excel outputs

WITH StepMinutes AS (
    SELECT "EXTERNAL_ID", SUM(generated_minutes) AS total_generated_minutes
    FROM steps
    GROUP BY "EXTERNAL_ID"
),
ExerciseMinutes AS (
    SELECT "EXTERNAL_ID", SUM("MINUTES") AS total_exercise_minutes
    FROM exercises
    GROUP BY "EXTERNAL_ID"
)
SELECT
    s."EXTERNAL_ID",
    COALESCE(s.total_generated_minutes, 0) + COALESCE(e.total_exercise_minutes, 0) AS total_minutes
FROM
    StepMinutes s
FULL OUTER JOIN ExerciseMinutes e
ON s."EXTERNAL_ID" = e."EXTERNAL_ID" ORDER BY s."EXTERNAL_ID" DESC;



-- COrrect Version with patient details
WITH StepMinutes AS (
    SELECT "EXTERNAL_ID", SUM("generated_minutes") AS total_generated_minutes
    FROM steps
    GROUP BY "EXTERNAL_ID"
),
ExerciseMinutes AS (
    SELECT "EXTERNAL_ID", SUM("MINUTES") AS total_exercise_minutes
    FROM exercises
    GROUP BY "EXTERNAL_ID"
),
CombinedMinutes AS (
    SELECT
        COALESCE(s."EXTERNAL_ID", e."EXTERNAL_ID") AS "EXTERNAL_ID",
        CAST(COALESCE(s.total_generated_minutes, 0) + COALESCE(e.total_exercise_minutes, 0) AS INTEGER) AS total_minutes
    FROM
        StepMinutes s
    FULL OUTER JOIN ExerciseMinutes e
    ON s."EXTERNAL_ID" = e."EXTERNAL_ID"
)
SELECT
    p."PATIENT_ID",
    p."first_name",
    p."last_name",
    p."country",
    cm.total_minutes
FROM
    CombinedMinutes cm
JOIN patients p ON cm."EXTERNAL_ID" = p."PATIENT_ID"
ORDER BY cm.total_minutes DESC;



