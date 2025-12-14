import tkinter as tk
from tkinter import ttk
from components.widgets import CardFrame, ModernButton, MessageBox
from backend.library_backend import LibraryBackend
from datetime import datetime

class DashboardPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.backend = LibraryBackend()
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Setup dashboard UI"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="📖 Library Dashboard", 
                font=('Helvetica', 24, 'bold'),
                bg='white', fg='#1E3A8A').pack(side=tk.LEFT)
        
        refresh_btn = ModernButton(header_frame, text="🔄 Refresh", 
                                  command=self.load_data)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Statistics Cards
        stats_frame = tk.Frame(self.main_frame, bg='white')
        stats_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.cards = {}
        card_configs = [
            ("Total Books", "📚", "books_count"),
            ("Borrowers", "👥", "borrowers_count"),
            ("Active Loans", "🔄", "active_loans"),
            ("Overdue", "⏰", "overdue_count"),
            ("Available", "📖", "available_copies"),
            ("Total Fines", "💰", "total_fines")
        ]
        
        for i, (title, icon, key) in enumerate(card_configs):
            row = i // 3
            col = i % 3
            
            card = CardFrame(stats_frame, title=title, icon=icon, value="0")
            card.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.cards[key] = card
            
            stats_frame.grid_columnconfigure(col, weight=1)
        
        # Recent Activity
        activity_frame = tk.LabelFrame(self.main_frame, text="📈 Recent Activity", 
                                      font=('Helvetica', 12, 'bold'),
                                      bg='white', padx=15, pady=15)
        activity_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for recent activity
        columns = ("ID", "Book", "Borrower", "Status", "Due Date")
        self.activity_tree = ttk.Treeview(activity_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.activity_tree.heading(col, text=col)
            self.activity_tree.column(col, width=100)
        
        self.activity_tree.column("Book", width=200)
        self.activity_tree.column("Borrower", width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(activity_frame, orient=tk.VERTICAL, command=self.activity_tree.yview)
        h_scrollbar = ttk.Scrollbar(activity_frame, orient=tk.HORIZONTAL, command=self.activity_tree.xview)
        self.activity_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.activity_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_data(self):
        """Load dashboard data"""
        try:
            stats = self.backend.get_system_statistics()
            
            # Update cards
            card_values = {
                'books_count': str(stats.get('total_books', 0)),
                'borrowers_count': str(stats.get('total_borrowers', 0)),
                'active_loans': str(stats.get('active_loans', 0)),
                'overdue_count': str(stats.get('overdue_count', 0)),
                'available_copies': str(stats.get('available_copies', 0)),
                'total_fines': f"${stats.get('total_fines', 0):.2f}"
            }
            
            for key, card in self.cards.items():
                card.update_value(card_values.get(key, "0"))
            
            # Update recent activity
            self.update_recent_activity()
            
        except Exception as e:
            MessageBox.show_error(f"Failed to load dashboard data: {str(e)}")
    
    def update_recent_activity(self):
        """Update recent activity treeview"""
        # Clear existing items
        for item in self.activity_tree.get_children():
            self.activity_tree.delete(item)
        
        # Get recent transactions
        transactions = self.backend.get_all_transactions()
        
        # Add to treeview (limit to 10)
        for tx in transactions[:10]:
            status = tx['status']
            status_icon = {
                'borrowed': '🟡',
                'returned': '🟢',
                'overdue': '🔴'
            }.get(status, '⚪')
            
            self.activity_tree.insert("", tk.END, values=(
                tx['transaction_id'],
                tx['title'],
                tx['borrower_name'],
                f"{status_icon} {status.title()}",
                tx['due_date']
            ))