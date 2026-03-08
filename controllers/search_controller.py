import sqlite3

def search_certificates(search_term, db_path="cert_system.db"):
    # Searches by Student Name, Cert UUID, or Course
    query = """
        SELECT c.cert_uuid, s.first_name, s.last_name, c.course, c.status
        FROM Certificates c
        JOIN Students s ON c.student_id = s.id
        WHERE s.first_name LIKE ? OR s.last_name LIKE ? OR c.cert_uuid LIKE ? OR c.course LIKE ?
    """
    wildcard_term = f"%{search_term}%"
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (wildcard_term, wildcard_term, wildcard_term, wildcard_term))
        return cursor.fetchall()
