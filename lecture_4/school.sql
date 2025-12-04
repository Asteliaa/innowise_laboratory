-- Student Grades Manager - school.db

-- 1. Create tables

CREATE TABLE IF NOT EXISTS students (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name  TEXT    NOT NULL,
    birth_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS grades (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject    TEXT    NOT NULL,
    grade      INTEGER NOT NULL CHECK (grade BETWEEN 1 AND 100),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- 2. Insert data
-- Transaction for students data

BEGIN TRANSACTION;

INSERT INTO students (id, full_name, birth_year) VALUES
    (1, 'Alice Johnson',      2005),
    (2, 'Brian Smith',        2004),
    (3, 'Carla Reyes',        2006),
    (4, 'Daniel Kim',         2005),
    (5, 'Eva Thompson',       2003),
    (6, 'Felix Nguyen',       2007),
    (7, 'Grace Patel',        2005),
    (8, 'Henry Lopez',        2004),
    (9, 'Isabella Martinez',  2006);

COMMIT;

-- Transaction for grades data

BEGIN TRANSACTION;

INSERT INTO grades (student_id, subject, grade) VALUES
    (1, 'Math',               88),
    (1, 'English',            92),
    (1, 'Science',            85),
    (2, 'Math',               75),
    (2, 'History',            83),
    (2, 'English',            79),
    (3, 'Science',            95),
    (3, 'Math',               91),
    (3, 'Art',                89),
    (4, 'Math',               84),
    (4, 'Science',            88),
    (4, 'Physical Education', 93),
    (5, 'English',            90),
    (5, 'History',            85),
    (5, 'Math',               88),
    (6, 'Science',            72),
    (6, 'Math',               78),
    (6, 'English',            81),
    (7, 'Art',                94),
    (7, 'Science',            87),
    (7, 'Math',               90),
    (8, 'History',            77),
    (8, 'Math',               83),
    (8, 'Science',            80),
    (9, 'English',            96),
    (9, 'Math',               89),
    (9, 'Art',                92);

COMMIT;

-- Query 1: Find all grades for a specific student (Alice Johnson)

SELECT
    s.full_name,
    g.subject,
    g.grade
FROM students AS s
JOIN grades AS g ON g.student_id = s.id
WHERE s.full_name = 'Alice Johnson'
ORDER BY g.subject ASC;

-- Query 2: Calculate the average grade per student

SELECT
    s.full_name,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM students AS s
LEFT JOIN grades AS g ON g.student_id = s.id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC;

-- Query 3: List all students born after 2004

SELECT
    full_name,
    birth_year
FROM students
WHERE birth_year > 2004
ORDER BY birth_year ASC, full_name ASC;

-- Query 4: List all subjects and their average grades

SELECT
    subject,
    ROUND(AVG(grade), 2) AS average_grade
FROM grades
GROUP BY subject
ORDER BY average_grade DESC;

-- Query 5: Find the top 3 students with the highest average grades

SELECT
    s.full_name,
    ROUND(AVG(g.grade), 2) AS average_grade
FROM students AS s
JOIN grades AS g ON g.student_id = s.id
GROUP BY s.id, s.full_name
ORDER BY average_grade DESC
LIMIT 3;

-- Query 6: Show all students who have scored below 80 in any subject

SELECT DISTINCT
    s.full_name
FROM students AS s
JOIN grades AS g ON g.student_id = s.id
WHERE g.grade < 80
ORDER BY s.full_name ASC;

-- 3. Indexes

CREATE INDEX IF NOT EXISTS idx_grades_student_id
    ON grades (student_id);

CREATE INDEX IF NOT EXISTS idx_grades_subject
    ON grades (subject);

CREATE INDEX IF NOT EXISTS idx_students_birth_year
    ON students (birth_year);
