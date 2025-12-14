# pages/signup_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.auth import AuthSystem
from components.widgets import ModernButton

class SignupPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.auth = AuthSystem()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup signup page UI"""
        # Clear parent
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Main container with scroll
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Center container
        center_frame = tk.Frame(scrollable_frame, bg='white')
        center_frame.pack(pady=20)
        
        # Logo/Title
        title_frame = tk.Frame(center_frame, bg='white')
        title_frame.pack(pady=(0, 20))
        
        tk.Label(title_frame, text="📚", 
                font=('Helvetica', 48),
                bg='white').pack()
        
        tk.Label(title_frame, text="Create New Account", 
                font=('Helvetica', 20, 'bold'),
                bg='white', fg='#1E3A8A').pack(pady=(10, 0))
        
        tk.Label(title_frame, text="Join our library management system", 
                font=('Helvetica', 12),
                bg='white', fg='#6B7280').pack()
        
        # Signup Form
        form_frame = tk.Frame(center_frame, bg='white', padx=40, pady=20)
        form_frame.pack()
        
        # Two column layout
        left_frame = tk.Frame(form_frame, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(form_frame, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Username field
        tk.Label(left_frame, text="Username *", 
                font=('Helvetica', 10),
                bg='white', anchor=tk.W).pack(fill=tk.X, pady=(0, 5))
        
        self.username_entry = tk.Entry(left_frame, font=('Helvetica', 12), 
                                      width=25, bd=2, relief=tk.GROOVE)
        self.username_entry.pack(fill=tk.X, pady=(0, 15))
        self.username_entry.focus_set()
        
        # Email field
        tk.Label(left_frame, text="Email *", 
                font=('Helvetica', 10),
                bg='white', anchor=tk.W).pack(fill=tk.X, pady=(0, 5))
        
        self.email_entry = tk.Entry(left_frame, font=('Helvetica', 12), 
                                   width=25, bd=2, relief=tk.GROOVE)
        self.email_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password field
        tk.Label(right_frame, text="Password *", 
                font=('Helvetica', 10),
                bg='white', anchor=tk.W).pack(fill=tk.X, pady=(0, 5))
        
        self.password_entry = tk.Entry(right_frame, font=('Helvetica', 12), 
                                      width=25, bd=2, relief=tk.GROOVE, 
                                      show="•")
        self.password_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Confirm Password field
        tk.Label(right_frame, text="Confirm Password *", 
                font=('Helvetica', 10),
                bg='white', anchor=tk.W).pack(fill=tk.X, pady=(0, 5))
        
        self.confirm_entry = tk.Entry(right_frame, font=('Helvetica', 12), 
                                     width=25, bd=2, relief=tk.GROOVE, 
                                     show="•")
        self.confirm_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password strength indicator
        self.strength_label = tk.Label(right_frame, text="", 
                                      font=('Helvetica', 9),
                                      bg='white', fg='#6B7280')
        self.strength_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Bind password field to check strength
        self.password_entry.bind('<KeyRelease>', self.check_password_strength)
        
        # User type selection
        type_frame = tk.Frame(form_frame, bg='white')
        type_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(type_frame, text="Account Type", 
                font=('Helvetica', 10, 'bold'),
                bg='white').pack(anchor=tk.W, pady=(0, 10))
        
        self.user_type = tk.StringVar(value="borrower")
        
        # Borrower radio
        borrower_frame = tk.Frame(type_frame, bg='white')
        borrower_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Radiobutton(borrower_frame, text="Borrower", 
                      variable=self.user_type, value="borrower",
                      font=('Helvetica', 10), bg='white',
                      selectcolor='white').pack(side=tk.LEFT)
        
        tk.Label(borrower_frame, text=" - Borrow books from library", 
                font=('Helvetica', 9),
                bg='white', fg='#6B7280').pack(side=tk.LEFT, padx=(10, 0))
        
        # Librarian radio (disabled for public signup)
        librarian_frame = tk.Frame(type_frame, bg='white')
        librarian_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Radiobutton(librarian_frame, text="Librarian", 
                      variable=self.user_type, value="librarian",
                      font=('Helvetica', 10), bg='white',
                      selectcolor='white', state='disabled').pack(side=tk.LEFT)
        
        tk.Label(librarian_frame, text=" - Library staff only", 
                font=('Helvetica', 9),
                bg='white', fg='#9CA3AF').pack(side=tk.LEFT, padx=(10, 0))
        
        # Admin radio (disabled for public signup)
        admin_frame = tk.Frame(type_frame, bg='white')
        admin_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Radiobutton(admin_frame, text="Administrator", 
                      variable=self.user_type, value="admin",
                      font=('Helvetica', 10), bg='white',
                      selectcolor='white', state='disabled').pack(side=tk.LEFT)
        
        tk.Label(admin_frame, text=" - System administrator only", 
                font=('Helvetica', 9),
                bg='white', fg='#9CA3AF').pack(side=tk.LEFT, padx=(10, 0))
        
        # Terms checkbox
        self.terms_var = tk.BooleanVar()
        terms_frame = tk.Frame(form_frame, bg='white')
        terms_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Checkbutton(terms_frame, text="I agree to the Terms of Service", 
                      variable=self.terms_var,
                      font=('Helvetica', 10), bg='white',
                      selectcolor='white').pack(anchor=tk.W)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg='white')
        buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Sign up button
        signup_btn = ModernButton(buttons_frame, text="📝 Create Account", 
                                 command=self.signup,
                                 bg='#10B981')
        signup_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = tk.Button(buttons_frame, text="Cancel", 
                              command=lambda: self.controller.show_login(),
                              bg='#E5E7EB', fg='black',
                              relief=tk.FLAT, padx=20)
        cancel_btn.pack(side=tk.LEFT)
        
        # Already have account link
        link_frame = tk.Frame(form_frame, bg='white')
        link_frame.pack(fill=tk.X)
        
        tk.Label(link_frame, text="Already have an account?", 
                font=('Helvetica', 10),
                bg='white').pack(side=tk.LEFT)
        
        login_link = tk.Label(link_frame, text=" Sign in here", 
                             font=('Helvetica', 10, 'underline'),
                             bg='white', fg='#3B82F6', cursor='hand2')
        login_link.pack(side=tk.LEFT)
        login_link.bind('<Button-1>', lambda e: self.controller.show_login())
    
    def check_password_strength(self, event=None):
        """Check password strength and update indicator"""
        password = self.password_entry.get()
        
        if not password:
            self.strength_label.config(text="")
            return
        
        is_valid, message = self.auth.validate_password_strength(password)
        
        if is_valid:
            self.strength_label.config(text="✅ Strong password", fg='#059669')
        else:
            self.strength_label.config(text=f"⚠️ {message}", fg='#DC2626')
    
    def signup(self):
        """Handle user registration"""
        # Get form data
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()
        role = self.user_type.get()
        
        # Validation
        errors = []
        
        if not username:
            errors.append("Username is required")
        elif len(username) < 3:
            errors.append("Username must be at least 3 characters")
        
        if not email:
            errors.append("Email is required")
        
        if not password:
            errors.append("Password is required")
        
        if password != confirm_password:
            errors.append("Passwords do not match")
        
        if not self.terms_var.get():
            errors.append("You must agree to the Terms of Service")
        
        # Check password strength
        is_valid, message = self.auth.validate_password_strength(password)
        if not is_valid:
            errors.append(message)
        
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        
        # Show loading
        self.parent.config(cursor='watch')
        self.parent.update()
        
        try:
            # Register user
            success, result = self.auth.register_user(username, email, password, role)
            
            if success:
                messagebox.showinfo("Registration Successful", result)
                
                # Auto login after registration
                login_success, login_msg = self.auth.login(username, password)
                if login_success:
                    user = self.auth.get_current_user()
                    self.controller.show_main_app(user['role'])
                else:
                    self.controller.show_login()
            else:
                messagebox.showerror("Registration Failed", result)
                
        except Exception as e:
            messagebox.showerror("Error", f"Registration error: {str(e)}")
        finally:
            self.parent.config(cursor='')