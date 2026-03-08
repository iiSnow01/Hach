import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(header_frame, text="← Back to Dashboard", command=lambda: controller.show_frame("DashboardView")).pack(side=tk.LEFT, padx=10)
        tk.Label(header_frame, text="Manage Students", font=("Helvetica", 20, "bold")).pack(side=tk.LEFT, padx=20)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Student Number:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.num_entry = tk.Entry(form_frame)
        self.num_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="First Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.fn_entry = tk.Entry(form_frame)
        self.fn_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Last Name:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.ln_entry = tk.Entry(form_frame)
        self.ln_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(form_frame, text="Add Student", command=self.add_student, bg="#4CAF50", fg="white").grid(row=3, columnspan=2, pady=15)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("ID", "Student Number", "First Name", "Last Name"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Student Number", text="Student Number")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def update_view(self):
        self.load_students()

    def load_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        with sqlite3.connect("cert_system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Students")
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

    def add_student(self):
        num = self.num_entry.get().strip()
        fn = self.fn_entry.get().strip()
        ln = self.ln_entry.get().strip()

        if not (num and fn and ln):
            messagebox.showerror("Error", "All fields required")
            return

        try:
            with sqlite3.connect("cert_system.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Students (student_num, first_name, last_name) VALUES (?, ?, ?)", (num, fn, ln))
                conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            self.load_students()
            self.num_entry.delete(0, tk.END)
            self.fn_entry.delete(0, tk.END)
            self.ln_entry.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Student number already exists in database.")
