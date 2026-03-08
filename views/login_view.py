import tkinter as tk
from tkinter import messagebox
import sqlite3

class LoginView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.config(bg="#f0f0f0")

        tk.Label(self, text="Login", font=("Helvetica", 24, "bold"), bg="#f0f0f0").pack(pady=40)

        tk.Label(self, text="Username", bg="#f0f0f0").pack()
        self.username_entry = tk.Entry(self, font=("Helvetica", 14))
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password", bg="#f0f0f0").pack()
        self.password_entry = tk.Entry(self, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login, font=("Helvetica", 14), width=15).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with sqlite3.connect("cert_system.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, role FROM Users WHERE username=? AND password_hash=?", (username, password))
            user = cursor.fetchone()

            if user:
                self.controller.current_user = {"id": user[0], "username": username, "role": user[1]}
                self.controller.show_frame("DashboardView")
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Invalid username or password")
