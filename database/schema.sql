CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL -- 'teacher' or 'admin'
);

CREATE TABLE IF NOT EXISTS Students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_num TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cert_uuid TEXT UNIQUE NOT NULL,    -- Unique public ID
    student_id INTEGER NOT NULL,
    course TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    status TEXT NOT NULL,              -- 'draft', 'teacher_validated', 'admin_approved'
    teacher_id INTEGER,                -- Who validated it
    admin_id INTEGER,                  -- Who approved it
    file_hash TEXT UNIQUE,             -- SHA-256 of the generated PDF
    FOREIGN KEY (student_id) REFERENCES Students(id),
    FOREIGN KEY (teacher_id) REFERENCES Users(id),
    FOREIGN KEY (admin_id) REFERENCES Users(id)
);
