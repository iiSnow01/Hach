import sqlite3
import uuid

class CertificateController:
    def __init__(self, db_path="cert_system.db"):
        self.db_path = db_path

    def execute_query(self, query, params=()):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor

    def add_student(self, student_num, first_name, last_name):
        self.execute_query(
            "INSERT INTO Students (student_num, first_name, last_name) VALUES (?, ?, ?)",
            (student_num, first_name, last_name)
        )

    def create_draft_certificate(self, student_id, course, issue_date):
        cert_uuid = str(uuid.uuid4())
        self.execute_query(
            "INSERT INTO Certificates (cert_uuid, student_id, course, issue_date, status) VALUES (?, ?, ?, ?, 'draft')",
            (cert_uuid, student_id, course, issue_date)
        )
        return cert_uuid

    def teacher_validate(self, cert_id, teacher_id):
        self.execute_query(
            "UPDATE Certificates SET status = 'teacher_validated', teacher_id = ? WHERE id = ? AND status = 'draft'",
            (teacher_id, cert_id)
        )

    def admin_approve(self, cert_id, admin_id, file_hash):
        self.execute_query(
            "UPDATE Certificates SET status = 'admin_approved', admin_id = ?, file_hash = ? WHERE id = ? AND status = 'teacher_validated'",
            (admin_id, file_hash, cert_id)
        )
