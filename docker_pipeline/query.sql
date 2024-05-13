ALTER TABLE steps ADD COLUMN generated_minutes FLOAT;
ALTER TABLE steps RENAME COLUMN "STEPS" TO footsteps;

UPDATE steps SET generated_minutes = CAST(footsteps AS double precision) * 0.002;

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
ORDER BY cm.total_minutes DESC limit 1;