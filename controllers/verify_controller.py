from utils.hasher import calculate_file_hash
import sqlite3

def verify_certificate(file_path, db_path="cert_system.db"):
    file_hash = calculate_file_hash(file_path)
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, status FROM Certificates WHERE file_hash = ?", (file_hash,))
        result = cursor.fetchone()
        
    if result:
        return True, "Valid: Certificate matches database records and has not been tampered with."
    else:
        return False, "Tampered/Invalid: Certificate hash does not exist in the secure database."
