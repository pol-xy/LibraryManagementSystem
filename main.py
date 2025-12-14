# main.py - UPDATED VERSION
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.dashboard_page import DashboardPage
from pages.books_page import BooksPage
from pages.borrowers_page import BorrowersPage
from pages.transactions_page import TransactionsPage
from pages.reports_page import ReportsPage
from backend.auth import AuthSystem
from database.db_connection import get_db_connection

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg='white')
        
        # Set minimum size
        self.root.minsize(1000, 600)
        
        # Initialize systems
        self.db = get_db_connection()
        self.auth = AuthSystem()
        self.current_user = None
        self.user_role = None
        
        # Setup styles
        self.setup_styles()
        
        # Create UI container
        self.container = tk.Frame(self.root, bg='white')
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Show login page by default
        self.show_login()
        
        # Bind closing event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Configure application styles"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.colors = {
            'primary': '#1E3A8A',
            'secondary': '#3B82F6',
            'success': '#10B981',
            'danger': '#EF4444',
            'warning': '#F59E0B',
            'light': '#F8FAFC',
            'dark': '#1F2937'
        }
        
        # Configure fonts
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.heading_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.normal_font = tkfont.Font(family="Helvetica", size=10)
    
    def clear_container(self):
        """Clear the container"""
        for widget in self.container.winfo_children():
            widget.destroy()
    
    # ========== AUTHENTICATION PAGES ==========
    
    def show_login(self):
        """Show login page"""
        self.clear_container()
        self.login_page = LoginPage(self.container, self)
    
    def show_signup(self):
        """Show signup page"""
        self.clear_container()
        self.signup_page = SignupPage(self.container, self)
    
    def show_main_app(self, user_role):
        """Show main application after login"""
        self.user_role = user_role
        self.current_user = self.auth.get_current_user()
        
        # Clear container and show main app
        self.clear_container()
        self.setup_main_ui()
        
        # Show dashboard by default
        self.show_dashboard()
        
        # Update window title with username
        username = self.current_user['username'] if self.current_user else 'Guest'
        self.root.title(f"Library Management System - Welcome, {username}")
    
    # ========== MAIN APPLICATION UI ==========
    
    def setup_main_ui(self):
        """Setup the main user interface after login"""
        # Create main container with sidebar
        self.main_container = tk.Frame(self.container, bg='white')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar
        self.setup_sidebar()
        
        # Create content area
        self.content_area = tk.Frame(self.main_container, bg='white')
        self.content_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def setup_sidebar(self):
        """Setup the sidebar navigation"""
        # Sidebar frame
        sidebar = tk.Frame(self.main_container, bg=self.colors['primary'], width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)
        
        # User info at top
        user_frame = tk.Frame(sidebar, bg=self.colors['primary'])
        user_frame.pack(fill=tk.X, pady=(20, 20), padx=15)
        
        # User avatar/icon
        tk.Label(user_frame, text="👤", 
                font=('Helvetica', 24),
                bg=self.colors['primary'], fg='white').pack()
        
        # Username
        if self.current_user:
            username = self.current_user['username']
            role = self.current_user['role'].title()
            
            tk.Label(user_frame, text=username, 
                    font=('Helvetica', 12, 'bold'),
                    bg=self.colors['primary'], fg='white').pack(pady=(5, 0))
            
            tk.Label(user_frame, text=f"({role})", 
                    font=('Helvetica', 9),
                    bg=self.colors['primary'], fg='#D1D5DB').pack()
        
        # Separator
        tk.Frame(sidebar, bg='#374151', height=1).pack(fill=tk.X, padx=15, pady=(0, 20))
        
        # Navigation buttons based on role
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📚 Books", self.show_books),
            ("👥 Borrowers", self.show_borrowers),
            ("🔄 Transactions", self.show_transactions),
            ("📊 Reports", self.show_reports)
        ]
        
        # Add admin-only features
        if self.user_role in ['admin', 'librarian']:
            nav_buttons.append(("👥 User Management", self.show_user_management))
        
        for text, command in nav_buttons:
            btn = tk.Button(sidebar, text=text, font=self.normal_font,
                           command=command, bg=self.colors['primary'],
                           fg='white', relief=tk.FLAT, anchor=tk.W,
                           padx=20, pady=12, cursor='hand2')
            btn.pack(fill=tk.X, padx=10, pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.colors['secondary']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.colors['primary']))
        
        # Separator
        tk.Frame(sidebar, bg='#374151', height=1).pack(fill=tk.X, padx=15, pady=20)
        
        # Quick stats
        stats_frame = tk.Frame(sidebar, bg=self.colors['light'])
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(stats_frame, text="📊 Quick Stats", 
                font=self.heading_font,
                bg=self.colors['light']).pack(anchor=tk.W, pady=(0, 10))
        
        self.stats_labels = {}
        stats_items = [
            ("📚 Books:", "books_count"),
            ("👥 Borrowers:", "borrowers_count"),
            ("🔄 Active:", "active_loans"),
            ("⏰ Overdue:", "overdue_count")
        ]
        
        for text, key in stats_items:
            frame = tk.Frame(stats_frame, bg=self.colors['light'])
            frame.pack(fill=tk.X, pady=2)
            tk.Label(frame, text=text, font=self.normal_font,
                    bg=self.colors['light']).pack(side=tk.LEFT)
            self.stats_labels[key] = tk.Label(frame, text="0", font=self.normal_font, 
                                             fg=self.colors['primary'],
                                             bg=self.colors['light'])
            self.stats_labels[key].pack(side=tk.RIGHT)
        
        # Separator
        tk.Frame(sidebar, bg='#374151', height=1).pack(fill=tk.X, padx=15, pady=20)
        
        # Bottom section
        bottom_frame = tk.Frame(sidebar, bg=self.colors['primary'])
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Database status
        if self.db.connect():
            status_text = "✅ Connected"
            status_color = self.colors['success']
        else:
            status_text = "❌ Disconnected"
            status_color = self.colors['danger']
        
        tk.Label(bottom_frame, text=status_text, 
                font=self.normal_font, fg=status_color,
                bg=self.colors['primary']).pack(side=tk.LEFT)
        
        # Logout button
        logout_btn = tk.Button(bottom_frame, text="🚪 Logout", 
                              command=self.logout,
                              font=self.normal_font,
                              bg=self.colors['primary'],
                              fg='white', relief=tk.FLAT,
                              cursor='hand2')
        logout_btn.pack(side=tk.RIGHT)
        logout_btn.bind("<Enter>", lambda e, b=logout_btn: b.config(bg=self.colors['danger']))
        logout_btn.bind("<Leave>", lambda e, b=logout_btn: b.config(bg=self.colors['primary']))
    
    # ========== MAIN APP PAGES ==========
    
    def show_dashboard(self):
        """Show dashboard page"""
        self.clear_content_area()
        self.dashboard_page = DashboardPage(self.content_area, self)
        self.update_sidebar_stats()
    
    def show_books(self):
        """Show books management page"""
        self.clear_content_area()
        self.books_page = BooksPage(self.content_area, self)
    
    def show_borrowers(self):
        """Show borrowers management page"""
        self.clear_content_area()
        self.borrowers_page = BorrowersPage(self.content_area, self)
    
    def show_transactions(self):
        """Show transactions management page"""
        self.clear_content_area()
        self.transactions_page = TransactionsPage(self.content_area, self)
    
    def show_reports(self):
        """Show reports page"""
        self.clear_content_area()
        self.reports_page = ReportsPage(self.content_area, self)
    
    def show_user_management(self):
        """Show user management page (admin/librarian only)"""
        self.clear_content_area()
        # You can create a UserManagementPage later
        tk.Label(self.content_area, text="User Management (Coming Soon)", 
                font=('Helvetica', 20),
                bg='white').pack(expand=True)
    
    def clear_content_area(self):
        """Clear the content area"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def update_sidebar_stats(self):
        """Update sidebar statistics"""
        try:
            # Query database for statistics
            books_query = "SELECT COUNT(*) as count FROM books"
            borrowers_query = "SELECT COUNT(*) as count FROM borrowers"
            active_query = "SELECT COUNT(*) as count FROM transactions WHERE status = 'borrowed'"
            overdue_query = "SELECT COUNT(*) as count FROM transactions WHERE status = 'borrowed' AND due_date < CURDATE()"
            
            books_count = self.db.execute_query(books_query, fetch=True)[0]['count']
            borrowers_count = self.db.execute_query(borrowers_query, fetch=True)[0]['count']
            active_loans = self.db.execute_query(active_query, fetch=True)[0]['count']
            overdue_loans = self.db.execute_query(overdue_query, fetch=True)[0]['count']
            
            # Update labels
            self.stats_labels['books_count'].config(text=str(books_count))
            self.stats_labels['borrowers_count'].config(text=str(borrowers_count))
            self.stats_labels['active_loans'].config(text=str(active_loans))
            self.stats_labels['overdue_count'].config(text=str(overdue_loans))
            
        except Exception as e:
            print(f"Error updating stats: {e}")
    
    # ========== AUTHENTICATION METHODS ==========
    
    def logout(self):
        """Logout current user"""
        success, message = self.auth.logout()
        if success:
            self.current_user = None
            self.user_role = None
            messagebox.showinfo("Logged Out", message)
            self.show_login()
            self.root.title("Library Management System")
    
    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Close database connection
            self.db.close()
            self.root.destroy()

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()