import tkinter as tk

class DashboardView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.config(bg="#f0f0f0")

        self.header = tk.Label(self, text="Dashboard", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
        self.header.pack(pady=40)

        # Basic Nav
        tk.Button(self, text="Manage Students", command=lambda: controller.show_frame("StudentView"), width=25, font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self, text="Process Certificates", command=lambda: controller.show_frame("CertWorkflowView"), width=25, font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self, text="Verify Certificate", command=lambda: controller.show_frame("VerifyView"), width=25, font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout, width=25, font=("Helvetica", 12), fg="red").pack(pady=30)

    def update_view(self):
        if self.controller.current_user:
            role = self.controller.current_user["role"]
            self.header.config(text=f"Dashboard ({role.capitalize()})")

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("LoginView")
