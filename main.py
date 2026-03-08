import tkinter as tk
import os
from database.db_manager import initialize_db
from views.login_view import LoginView
from views.dashboard_view import DashboardView
from views.student_view import StudentView
from views.cert_workflow_view import CertWorkflowView
from views.verify_view import VerifyView

class CertSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Certificate Management System")
        self.geometry("900x600")

        self.current_user = None

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginView, DashboardView, StudentView, CertWorkflowView, VerifyView):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginView")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        try:
            frame.update_view() # Refresh if necessary
        except AttributeError:
            pass
        frame.tkraise()

def main():
    initialize_db()
    app = CertSystemApp()
    app.mainloop()

if __name__ == "__main__":
    main()
