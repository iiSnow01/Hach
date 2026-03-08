import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from controllers.verify_controller import verify_certificate
import traceback

class VerifyView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.X, pady=10)
        tk.Button(header_frame, text="← Back to Dashboard", command=lambda: controller.show_frame("DashboardView")).pack(side=tk.LEFT, padx=10)
        tk.Label(header_frame, text="Verify Local Certificate", font=("Helvetica", 20, "bold")).pack(side=tk.LEFT, padx=20)

        tk.Label(self, text="Select a generated PDF certificate to recalculate its SHA-256 hash\nand verify it with the local secure database.", font=("Helvetica", 12)).pack(pady=30)

        tk.Button(self, text="Select PDF to Verify", command=self.verify_pdf, font=("Helvetica", 14), bg="#2196F3", fg="white", padx=10, pady=5).pack(pady=20)

        self.result_label = tk.Label(self, text="", font=("Helvetica", 16, "bold"))
        self.result_label.pack(pady=40)

        self.details_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.details_label.pack(pady=10)

    def verify_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
        
        try:
            self.result_label.config(text="Verifying...", fg="black")
            self.update()

            is_valid, message = verify_certificate(file_path, "cert_system.db")
            
            if is_valid:
                self.result_label.config(text="✔️ " + message, fg="green")
            else:
                self.result_label.config(text="❌ " + message, fg="red")
            
            self.details_label.config(text=f"Selected File: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not verify file:\n{traceback.format_exc()}")
            self.result_label.config(text="Error reading file.", fg="red")
