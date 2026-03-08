import sqlite3
import os

def initialize_db(db_path="cert_system.db", schema_path=os.path.join("database", "schema.sql")):
    if not os.path.exists(db_path):
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, "r") as f:
                conn.executescript(f.read())
            
            # Seed users
            conn.execute("INSERT INTO Users (username, password_hash, role) VALUES ('admin', 'admin123', 'admin')")
            conn.execute("INSERT INTO Users (username, password_hash, role) VALUES ('teacher', 'teacher123', 'teacher')")
            conn.commit()
        print("Database built from schema with seed users.")
    else:
        print("Database already exists.")

if __name__ == "__main__":
    initialize_db()
