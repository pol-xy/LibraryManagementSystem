# pages/login_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import AuthSystem
from components.widgets import ModernButton, InputField, MessageBox

class LoginPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.auth = AuthSystem()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup login page UI"""
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Main container
        self.main_frame = tk.Frame(self.parent, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Center container
        center_frame = tk.Frame(self.main_frame, bg='white')
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Logo/Title
        title_frame = tk.Frame(center_frame, bg='white')
        title_frame.pack(pady=(0, 30))
        
        tk.Label(title_frame, text="📚", 
                font=('Helvetica', 48),
                bg='white').pack()
        
        tk.Label(title_frame, text="Library Management System", 
                font=('Helvetica', 20, 'bold'),
                bg='white', fg='#1E3A8A').pack(pady=(10, 0))
        
        tk.Label(title_frame, text="Sign in to your account", 
                font=('Helvetica', 12),
                bg='white', fg='#6B7280').pack()
        
        # Login Form
        form_frame = tk.Frame(center_frame, bg='white', padx=40, pady=30)
        form_frame.pack()
        
        # Username/Email field
        tk.Label(form_frame, text="Username or Email", 
                font=('Helvetica', 10),
                bg='white', anchor=tk.W).pack(fill=tk.X, pady=(0, 5))
        
        self.username_entry = tk.Entry(form_frame, font=('Helvetica', 12), 
                                      width=30, bd=2, relief=tk.GROOVE)
        self.username_entry.pack(pady=(0, 15))
        self.username_entry.focus_set()
        
        # Password field
        tk.Label(form_frame, text="Password", 
                font=('Helvetica', 10),
                bg='white', anchor=tk.W).pack(fill=tk.X, pady=(0, 5))
        
        self.password_entry = tk.Entry(form_frame, font=('Helvetica', 12), 
                                      width=30, bd=2, relief=tk.GROOVE, 
                                      show="•")
        self.password_entry.pack(pady=(0, 20))
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Login button
        login_btn = ModernButton(form_frame, text="🔐 Sign In", 
                                command=self.login,
                                bg='#1E3A8A')
        login_btn.pack(fill=tk.X, pady=(0, 20))
        
        # Links frame
        links_frame = tk.Frame(form_frame, bg='white')
        links_frame.pack(fill=tk.X)
        
        # Sign up link
        signup_link = tk.Label(links_frame, text="Create an account", 
                              font=('Helvetica', 10, 'underline'),
                              bg='white', fg='#3B82F6', cursor='hand2')
        signup_link.pack(side=tk.LEFT)
        signup_link.bind('<Button-1>', lambda e: self.controller.show_signup())
        
        # Forgot password link
        forgot_link = tk.Label(links_frame, text="Forgot password?", 
                              font=('Helvetica', 10, 'underline'),
                              bg='white', fg='#6B7280', cursor='hand2')
        forgot_link.pack(side=tk.RIGHT)
        forgot_link.bind('<Button-1>', lambda e: self.show_forgot_password())
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Input Error", 
                                 "Please enter username/email and password")
            return
        
        # Show loading
        self.parent.config(cursor='watch')
        self.parent.update()
        
        try:
            success, message = self.auth.login(username, password)
            
            if success:
                user = self.auth.get_current_user()
                messagebox.showinfo("Login Successful", message)
                self.controller.show_main_app(user['role'])
            else:
                messagebox.showerror("Login Failed", message)
                
        except Exception as e:
            messagebox.showerror("Error", f"Login error: {str(e)}")
        finally:
            self.parent.config(cursor='')
    
    def show_forgot_password(self):
        """Show forgot password dialog"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Reset Password")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Content
        tk.Label(dialog, text="Reset Password", 
                font=('Helvetica', 16, 'bold'),
                bg='white', fg='#1E3A8A').pack(pady=20)
        
        tk.Label(dialog, text="Enter your email address to receive reset instructions", 
                font=('Helvetica', 10),
                bg='white', fg='#6B7280').pack(pady=(0, 20))
        
        email_frame = tk.Frame(dialog, bg='white')
        email_frame.pack(pady=(0, 20), padx=40)
        
        tk.Label(email_frame, text="Email", 
                font=('Helvetica', 10),
                bg='white').pack(anchor=tk.W)
        
        email_entry = tk.Entry(email_frame, font=('Helvetica', 12), 
                              width=30, bd=2, relief=tk.GROOVE)
        email_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.pack(pady=(0, 20))
        
        def send_reset():
            email = email_entry.get().strip()
            if not email:
                messagebox.showwarning("Input Error", "Please enter your email")
                return
            
            success, message = self.auth.reset_password_request(email)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        ModernButton(button_frame, text="Send Reset Link", 
                    command=send_reset,
                    bg='#1E3A8A').pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Cancel", 
                 command=dialog.destroy,
                 bg='#E5E7EB', fg='black',
                 relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)