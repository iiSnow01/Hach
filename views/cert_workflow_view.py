import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import uuid
import os
from datetime import datetime
from utils.pdf_generator import generate_certificate_pdf
from utils.hasher import calculate_file_hash

class CertWorkflowView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.X, pady=10)
        tk.Button(header_frame, text="← Back to Dashboard", command=lambda: controller.show_frame("DashboardView")).pack(side=tk.LEFT, padx=10)
        tk.Label(header_frame, text="Process Certificates", font=("Helvetica", 20, "bold")).pack(side=tk.LEFT, padx=20)

        # Creation Form (Only draft creation)
        form_frame = tk.LabelFrame(self, text="Create New Certificate Draft", padx=10, pady=10)
        form_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(form_frame, text="Student ID (from DB):").grid(row=0, column=0, padx=5, pady=5)
        self.student_entry = tk.Entry(form_frame)
        self.student_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Course:").grid(row=0, column=2, padx=5, pady=5)
        self.course_entry = tk.Entry(form_frame)
        self.course_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(form_frame, text="Create Draft", command=self.create_draft, bg="#2196F3", fg="white").grid(row=0, column=4, padx=15)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "UUID", "Student", "Course", "Status"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("UUID", text="UUID")
        self.tree.heading("Student", text="Student Name")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=50)
        self.tree.column("UUID", width=250)
        self.tree.column("Student", width=150)
        self.tree.column("Course", width=150)
        self.tree.column("Status", width=120)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.action_btn = tk.Button(self, text="Perform Action", command=self.perform_action, font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.action_btn.pack(pady=15)

    def update_view(self):
        if not self.controller.current_user:
            return
        role = self.controller.current_user["role"]
        
        if role == "teacher":
            self.action_btn.config(text="Teacher: Validate Selected Draft")
        elif role == "admin":
            self.action_btn.config(text="Admin: Approve & Generate PDF")
        
        self.load_certs()

    def load_certs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        with sqlite3.connect("cert_system.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.id, c.cert_uuid, s.first_name || ' ' || s.last_name, c.course, c.status
                FROM Certificates c
                JOIN Students s ON c.student_id = s.id
            ''')
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

    def create_draft(self):
        student_id = self.student_entry.get().strip()
        course = self.course_entry.get().strip()
        
        if not student_id or not course:
            messagebox.showerror("Error", "Required fields empty")
            return
        
        if not student_id.isdigit():
            messagebox.showerror("Error", "Student ID must be a number (ID in Database).")
            return
            
        cert_uuid = str(uuid.uuid4())
        issue_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            with sqlite3.connect("cert_system.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM Students WHERE id=?", (student_id,))
                if not cursor.fetchone():
                    messagebox.showerror("Error", "Student ID not found in the database.")
                    return
                
                cursor.execute(
                    "INSERT INTO Certificates (cert_uuid, student_id, course, issue_date, status) VALUES (?, ?, ?, ?, 'draft')",
                    (cert_uuid, student_id, course, issue_date)
                )
                conn.commit()
            self.load_certs()
            self.student_entry.delete(0, tk.END)
            self.course_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Draft certificate created.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def perform_action(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a certificate from the list.")
            return
        
        item = self.tree.item(selected[0])
        cert_id = item['values'][0]
        cert_uuid = item['values'][1]
        student_name = item['values'][2]
        course = item['values'][3]
        status = item['values'][4]
        
        role = self.controller.current_user["role"]
        user_id = self.controller.current_user["id"]

        try:
            with sqlite3.connect("cert_system.db") as conn:
                cursor = conn.cursor()
                
                if role == "teacher" and status == "draft":
                    cursor.execute("UPDATE Certificates SET status='teacher_validated', teacher_id=? WHERE id=?", (user_id, cert_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Certificate Validated Successfully.")
                
                elif role == "admin" and status == "teacher_validated":
                    # Generate PDF and Hash
                    cursor.execute("SELECT issue_date FROM Certificates WHERE id=?", (cert_id,))
                    issue_date = cursor.fetchone()[0]
                    
                    os.makedirs("output", exist_ok=True)
                    output_path = f"output/{cert_uuid}.pdf"
                    
                    generate_certificate_pdf(student_name, course, issue_date, cert_uuid, output_path)
                    file_hash = calculate_file_hash(output_path)
                    
                    cursor.execute("UPDATE Certificates SET status='admin_approved', admin_id=?, file_hash=? WHERE id=?", (user_id, file_hash, cert_id))
                    conn.commit()
                    messagebox.showinfo("Success", f"Certificate Approved!\nPDF Generated at:\n{output_path}")
                
                else:
                    messagebox.showerror("Error", f"Action denied!\nRole '{role}' cannot process a certificate in status '{status}'.")
            
            self.load_certs()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
