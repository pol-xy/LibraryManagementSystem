import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from components.widgets import ModernButton, ModernTreeview, MessageBox
from backend.library_backend import LibraryBackend
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ReportsPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.backend = LibraryBackend()
        
        self.setup_ui()
        self.load_dashboard()
    
    def setup_ui(self):
        """Setup reports page UI"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="📊 Reports & Analytics", 
                font=('Helvetica', 24, 'bold'),
                bg='white', fg='#1E3A8A').pack(side=tk.LEFT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Dashboard Tab
        self.dashboard_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.setup_dashboard_tab()
        
        # Books Report Tab
        self.books_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.books_tab, text="Books Report")
        self.setup_books_tab()
        
        # Borrowers Report Tab
        self.borrowers_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.borrowers_tab, text="Borrowers Report")
        self.setup_borrowers_tab()
        
        # Transaction Analysis Tab
        self.transactions_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.transactions_tab, text="Transaction Analysis")
        self.setup_transactions_tab()
    
    def setup_dashboard_tab(self):
        """Setup dashboard tab"""
        # Key metrics frame
        metrics_frame = tk.Frame(self.dashboard_tab, bg='white')
        metrics_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.metric_labels = {}
        metrics = [
            ("Total Books", "📚"),
            ("Total Borrowers", "👥"),
            ("Active Loans", "🔄"),
            ("Overdue Books", "⏰"),
            ("Available Books", "📖"),
            ("Total Fines", "💰")
        ]
        
        for i, (title, icon) in enumerate(metrics):
            frame = tk.Frame(metrics_frame, bg='white', relief=tk.RAISED, borderwidth=1)
            frame.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
            
            tk.Label(frame, text=f"{icon} {title}", 
                    bg='#1E3A8A', fg='white',
                    font=('Helvetica', 10, 'bold')).pack(fill=tk.X)
            
            value_label = tk.Label(frame, text="0", 
                                  font=('Helvetica', 16, 'bold'),
                                  bg='white')
            value_label.pack(pady=10)
            
            self.metric_labels[title] = value_label
            
            metrics_frame.grid_columnconfigure(i%3, weight=1)
        
        # Charts frame
        charts_frame = tk.Frame(self.dashboard_tab, bg='white')
        charts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left chart frame
        left_chart_frame = tk.Frame(charts_frame, bg='white')
        left_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(left_chart_frame, text="Book Categories Distribution", 
                font=('Helvetica', 12, 'bold'),
                bg='white').pack(pady=(0, 10))
        
        self.category_canvas_frame = tk.Frame(left_chart_frame, bg='white')
        self.category_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Right chart frame
        right_chart_frame = tk.Frame(charts_frame, bg='white')
        right_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(right_chart_frame, text="Monthly Borrowing Trend", 
                font=('Helvetica', 12, 'bold'),
                bg='white').pack(pady=(0, 10))
        
        self.monthly_canvas_frame = tk.Frame(right_chart_frame, bg='white')
        self.monthly_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top performers frame
        performers_frame = tk.Frame(self.dashboard_tab, bg='white')
        performers_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Top books frame
        books_frame = tk.Frame(performers_frame, bg='white')
        books_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(books_frame, text="📚 Most Borrowed Books", 
                font=('Helvetica', 12, 'bold'),
                bg='white').pack(pady=(0, 10))
        
        # Treeview for top books
        book_columns = ("Rank", "Title", "Author", "Borrow Count")
        self.top_books_tree = ttk.Treeview(books_frame, columns=book_columns, 
                                          show="headings", height=6)
        self.top_books_tree.pack(fill=tk.BOTH, expand=True)
        
        for col in book_columns:
            self.top_books_tree.heading(col, text=col)
            self.top_books_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.top_books_tree.column("Title", width=150)
        
        # Top borrowers frame
        borrowers_frame = tk.Frame(performers_frame, bg='white')
        borrowers_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        tk.Label(borrowers_frame, text="👥 Most Active Borrowers", 
                font=('Helvetica', 12, 'bold'),
                bg='white').pack(pady=(0, 10))
        
        # Treeview for top borrowers
        borrower_columns = ("Rank", "Name", "Email", "Borrow Count")
        self.top_borrowers_tree = ttk.Treeview(borrowers_frame, columns=borrower_columns, 
                                              show="headings", height=6)
        self.top_borrowers_tree.pack(fill=tk.BOTH, expand=True)
        
        for col in borrower_columns:
            self.top_borrowers_tree.heading(col, text=col)
            self.top_borrowers_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.top_borrowers_tree.column("Name", width=120)
        self.top_borrowers_tree.column("Email", width=150)
        
        # Refresh button
        refresh_btn = ModernButton(self.dashboard_tab, text="🔄 Refresh Dashboard", 
                                  command=self.load_dashboard)
        refresh_btn.pack(pady=20)
    
    def setup_books_tab(self):
        """Setup books report tab"""
        # Filter frame
        filter_frame = tk.Frame(self.books_tab, bg='white')
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(filter_frame, text="Category:", 
                font=('Helvetica', 10),
                bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.category_filter = ttk.Combobox(filter_frame, state="readonly", width=20)
        self.category_filter.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(filter_frame, text="Availability:", 
                font=('Helvetica', 10),
                bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.availability_filter = ttk.Combobox(filter_frame, 
                                               values=["All", "Available", "Unavailable"],
                                               state="readonly", width=15)
        self.availability_filter.set("All")
        self.availability_filter.pack(side=tk.LEFT, padx=(0, 15))
        
        ModernButton(filter_frame, text="🔍 Apply Filters", 
                    command=self.filter_books_report).pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(filter_frame, text="Clear", 
                             command=self.clear_books_filter,
                             bg='#E5E7EB', fg='black',
                             relief=tk.FLAT, padx=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        stats_frame = tk.Frame(self.books_tab, bg='white')
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.books_total_label = tk.Label(stats_frame, text="Total Titles: 0",
                                         font=('Helvetica', 10, 'bold'),
                                         bg='white')
        self.books_total_label.pack(side=tk.LEFT, padx=20)
        
        self.books_copies_label = tk.Label(stats_frame, text="Total Copies: 0",
                                          font=('Helvetica', 10, 'bold'),
                                          bg='white')
        self.books_copies_label.pack(side=tk.LEFT, padx=20)
        
        self.books_available_label = tk.Label(stats_frame, text="Available: 0",
                                             font=('Helvetica', 10, 'bold'),
                                             bg='white', fg='#059669')
        self.books_available_label.pack(side=tk.LEFT, padx=20)
        
        self.books_borrowed_label = tk.Label(stats_frame, text="Borrowed: 0",
                                            font=('Helvetica', 10, 'bold'),
                                            bg='white', fg='#DC2626')
        self.books_borrowed_label.pack(side=tk.LEFT, padx=20)
        
        # Treeview for books report
        columns = ("ID", "Title", "Author", "Category", "Year", "Total", "Available", "Borrowed", "Status")
        self.books_report_tree = ModernTreeview(self.books_tab, columns=columns)
        self.books_report_tree.pack_with_scrollbars(pady=10)
        
        for col in columns:
            self.books_report_tree.heading(col, text=col)
            self.books_report_tree.column(col, width=80, anchor=tk.CENTER)
        
        self.books_report_tree.column("Title", width=150)
        self.books_report_tree.column("Author", width=120)
        
        # Action buttons
        action_frame = tk.Frame(self.books_tab, bg='white')
        action_frame.pack(fill=tk.X, pady=10)
        
        ModernButton(action_frame, text="🔄 Refresh", 
                    command=self.load_books_report).pack(side=tk.LEFT, padx=5)
    
    def setup_borrowers_tab(self):
        """Setup borrowers report tab"""
        # Treeview for borrowers report
        columns = ("ID", "Name", "Email", "Phone", "Joined", "Total Borrowed", "Active Loans", "Overdue", "Total Fines")
        self.borrowers_report_tree = ModernTreeview(self.borrowers_tab, columns=columns)
        self.borrowers_report_tree.pack_with_scrollbars(pady=10, padx=20)
        
        for col in columns:
            self.borrowers_report_tree.heading(col, text=col)
            self.borrowers_report_tree.column(col, width=80, anchor=tk.CENTER)
        
        self.borrowers_report_tree.column("Name", width=120)
        self.borrowers_report_tree.column("Email", width=150)
        
        # Statistics frame
        stats_frame = tk.Frame(self.borrowers_tab, bg='white')
        stats_frame.pack(fill=tk.X, pady=10, padx=20)
        
        self.borrowers_total_label = tk.Label(stats_frame, text="Total Borrowers: 0",
                                             font=('Helvetica', 10, 'bold'),
                                             bg='white')
        self.borrowers_total_label.pack(side=tk.LEFT, padx=20)
        
        self.borrowers_active_label = tk.Label(stats_frame, text="Active Borrowers: 0",
                                              font=('Helvetica', 10, 'bold'),
                                              bg='white', fg='#059669')
        self.borrowers_active_label.pack(side=tk.LEFT, padx=20)
        
        self.borrowers_fines_label = tk.Label(stats_frame, text="Borrowers with Fines: 0",
                                             font=('Helvetica', 10, 'bold'),
                                             bg='white', fg='#DC2626')
        self.borrowers_fines_label.pack(side=tk.LEFT, padx=20)
        
        # Action buttons
        action_frame = tk.Frame(self.borrowers_tab, bg='white')
        action_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ModernButton(action_frame, text="🔄 Refresh", 
                    command=self.load_borrowers_report).pack(side=tk.LEFT, padx=5)
    
    def setup_transactions_tab(self):
        """Setup transaction analysis tab"""
        # Date range frame
        date_frame = tk.Frame(self.transactions_tab, bg='white')
        date_frame.pack(fill=tk.X, pady=(0, 10), padx=20)
        
        tk.Label(date_frame, text="Start Date (YYYY-MM-DD):", 
                font=('Helvetica', 10),
                bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.start_date = tk.Entry(date_frame, font=('Helvetica', 10), width=15)
        self.start_date.insert(0, (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        self.start_date.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(date_frame, text="End Date:", 
                font=('Helvetica', 10),
                bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.end_date = tk.Entry(date_frame, font=('Helvetica', 10), width=15)
        self.end_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.end_date.pack(side=tk.LEFT, padx=(0, 15))
        
        ModernButton(date_frame, text="📈 Generate Report", 
                    command=self.generate_transaction_report).pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        self.transaction_stats_frame = tk.Frame(self.transactions_tab, bg='white')
        self.transaction_stats_frame.pack(fill=tk.X, pady=10, padx=20)
        
        self.transactions_total_label = tk.Label(self.transaction_stats_frame, text="Total Transactions: 0",
                                               font=('Helvetica', 10, 'bold'),
                                               bg='white')
        self.transactions_total_label.pack(side=tk.LEFT, padx=20)
        
        self.transactions_borrowed_label = tk.Label(self.transaction_stats_frame, text="Books Borrowed: 0",
                                                   font=('Helvetica', 10, 'bold'),
                                                   bg='white')
        self.transactions_borrowed_label.pack(side=tk.LEFT, padx=20)
        
        self.transactions_returned_label = tk.Label(self.transaction_stats_frame, text="Books Returned: 0",
                                                   font=('Helvetica', 10, 'bold'),
                                                   bg='white')
        self.transactions_returned_label.pack(side=tk.LEFT, padx=20)
        
        self.transactions_fines_label = tk.Label(self.transaction_stats_frame, text="Total Fines: $0.00",
                                                font=('Helvetica', 10, 'bold'),
                                                bg='white', fg='#DC2626')
        self.transactions_fines_label.pack(side=tk.LEFT, padx=20)
        
        # Chart frame
        self.chart_frame = tk.Frame(self.transactions_tab, bg='white')
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Treeview for transaction details
        columns = ("Date", "Transactions", "Borrowed", "Returned", "Daily Fines")
        self.transaction_detail_tree = ModernTreeview(self.transactions_tab, columns=columns)
        self.transaction_detail_tree.pack_with_scrollbars(pady=10, padx=20)
        
        for col in columns:
            self.transaction_detail_tree.heading(col, text=col)
            self.transaction_detail_tree.column(col, width=100, anchor=tk.CENTER)
    
    def load_dashboard(self):
        """Load dashboard data"""
        try:
            stats = self.backend.get_system_statistics()
            
            # Update metrics
            self.metric_labels["Total Books"].config(text=str(stats.get('total_books', 0)))
            self.metric_labels["Total Borrowers"].config(text=str(stats.get('total_borrowers', 0)))
            self.metric_labels["Active Loans"].config(text=str(stats.get('active_loans', 0)))
            self.metric_labels["Overdue Books"].config(text=str(stats.get('overdue_books', 0)))
            self.metric_labels["Available Books"].config(text=str(stats.get('available_copies', 0)))
            self.metric_labels["Total Fines"].config(text=f"${stats.get('total_fines', 0):.2f}")
            
            # Load category chart
            self.load_category_chart()
            
            # Load monthly trend chart
            self.load_monthly_trend_chart()
            
            # Load top books
            self.load_top_books()
            
            # Load top borrowers
            self.load_top_borrowers()
            
        except Exception as e:
            MessageBox.show_error(f"Failed to load dashboard: {str(e)}")
    
    def load_category_chart(self):
        """Load book categories pie chart"""
        # Clear previous chart
        for widget in self.category_canvas_frame.winfo_children():
            widget.destroy()
        
        # Get category data
        categories = self.backend.get_category_report()
        
        if not categories:
            tk.Label(self.category_canvas_frame, text="No category data available",
                    bg='white').pack(expand=True)
            return
        
        # Create figure
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        # Prepare data
        category_names = [cat['category'] for cat in categories]
        book_counts = [cat['total_books'] for cat in categories]
        
        # Create pie chart
        ax.pie(book_counts, labels=category_names, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, self.category_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def load_monthly_trend_chart(self):
        """Load monthly borrowing trend chart"""
        # Clear previous chart
        for widget in self.monthly_canvas_frame.winfo_children():
            widget.destroy()
        
        # Get monthly data (last 6 months)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)  # 6 months
        
        # This is a simplified version - in real app, you'd query the database
        tk.Label(self.monthly_canvas_frame, text="Monthly trend data would be displayed here",
                bg='white').pack(expand=True)
    
    def load_top_books(self):
        """Load top borrowed books"""
        # Clear existing items
        for item in self.top_books_tree.get_children():
            self.top_books_tree.delete(item)
        
        # Get top books
        top_books = self.backend.get_popular_books_report(limit=10)
        
        # Add to treeview
        for i, book in enumerate(top_books, 1):
            self.top_books_tree.insert("", tk.END, values=(
                i,
                book['title'],
                book['author'],
                book['times_borrowed'] or 0
            ))
    
    def load_top_borrowers(self):
        """Load top active borrowers"""
        # Clear existing items
        for item in self.top_borrowers_tree.get_children():
            self.top_borrowers_tree.delete(item)
        
        # Get top borrowers
        top_borrowers = self.backend.get_borrower_activity_report(limit=10)
        
        # Add to treeview
        for i, borrower in enumerate(top_borrowers, 1):
            self.top_borrowers_tree.insert("", tk.END, values=(
                i,
                borrower['name'],
                borrower['email'],
                borrower['total_borrowed'] or 0
            ))
    
    def load_books_report(self):
        """Load books report"""
        # Clear existing items
        for item in self.books_report_tree.get_children():
            self.books_report_tree.delete(item)
        
        # Get all books
        books = self.backend.get_all_books()
        
        # Update categories filter
        categories = list(set(book['category'] for book in books))
        self.category_filter['values'] = ["All Categories"] + categories
        if categories:
            self.category_filter.set("All Categories")
        
        # Add to treeview and calculate statistics
        total_titles = len(books)
        total_copies = 0
        available_copies = 0
        
        for book in books:
            borrowed = book['copies'] - book['available_copies']
            status = "Available" if book['available_copies'] > 0 else "Unavailable"
            
            self.books_report_tree.insert("", tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                book['year'],
                book['copies'],
                book['available_copies'],
                borrowed,
                status
            ))
            
            total_copies += book['copies']
            available_copies += book['available_copies']
        
        # Update statistics
        self.books_total_label.config(text=f"Total Titles: {total_titles}")
        self.books_copies_label.config(text=f"Total Copies: {total_copies}")
        self.books_available_label.config(text=f"Available: {available_copies}")
        self.books_borrowed_label.config(text=f"Borrowed: {total_copies - available_copies}")
    
    def filter_books_report(self):
        """Filter books report by category and availability"""
        category_filter = self.category_filter.get()
        availability_filter = self.availability_filter.get()
        
        # Clear existing items
        for item in self.books_report_tree.get_children():
            self.books_report_tree.delete(item)
        
        # Get all books
        books = self.backend.get_all_books()
        
        # Apply filters
        filtered_books = []
        for book in books:
            # Category filter
            if category_filter != "All Categories" and book['category'] != category_filter:
                continue
            
            # Availability filter
            if availability_filter == "Available" and book['available_copies'] <= 0:
                continue
            elif availability_filter == "Unavailable" and book['available_copies'] > 0:
                continue
            
            filtered_books.append(book)
        
        # Add filtered books to treeview
        total_titles = len(filtered_books)
        total_copies = 0
        available_copies = 0
        
        for book in filtered_books:
            borrowed = book['copies'] - book['available_copies']
            status = "Available" if book['available_copies'] > 0 else "Unavailable"
            
            self.books_report_tree.insert("", tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                book['year'],
                book['copies'],
                book['available_copies'],
                borrowed,
                status
            ))
            
            total_copies += book['copies']
            available_copies += book['available_copies']
        
        # Update statistics
        self.books_total_label.config(text=f"Total Titles: {total_titles}")
        self.books_copies_label.config(text=f"Total Copies: {total_copies}")
        self.books_available_label.config(text=f"Available: {available_copies}")
        self.books_borrowed_label.config(text=f"Borrowed: {total_copies - available_copies}")
    
    def clear_books_filter(self):
        """Clear books report filters"""
        self.category_filter.set("All Categories")
        self.availability_filter.set("All")
        self.load_books_report()
    
    def load_borrowers_report(self):
        """Load borrowers report"""
        # Clear existing items
        for item in self.borrowers_report_tree.get_children():
            self.borrowers_report_tree.delete(item)
        
        # Get all borrowers with their activity
        borrowers = self.backend.get_all_borrowers()
        active_loans = self.backend.get_active_loans()
        overdue_books = self.backend.get_overdue_books()
        
        # Create dictionaries for quick lookup
        active_counts = {}
        overdue_counts = {}
        
        for loan in active_loans:
            borrower_id = loan['borrower_id']
            active_counts[borrower_id] = active_counts.get(borrower_id, 0) + 1
        
        for loan in overdue_books:
            borrower_id = loan['borrower_id']
            overdue_counts[borrower_id] = overdue_counts.get(borrower_id, 0) + 1
        
        # Add to treeview and calculate statistics
        total_borrowers = len(borrowers)
        active_borrowers = 0
        borrowers_with_fines = 0
        
        for borrower in borrowers:
            borrower_id = borrower['borrower_id']
            active = active_counts.get(borrower_id, 0)
            overdue = overdue_counts.get(borrower_id, 0)
            
            # Get total borrowed count (simplified - would need separate query in real app)
            total_borrowed = 0  # This should be calculated from transactions
            
            # Get total fines (simplified)
            total_fines = 0.00  # This should be calculated from transactions
            
            self.borrowers_report_tree.insert("", tk.END, values=(
                borrower['borrower_id'],
                borrower['name'],
                borrower['email'],
                borrower['phone'] or "",
                borrower['registered_date'],
                total_borrowed,
                active,
                overdue,
                f"${total_fines:.2f}"
            ))
            
            if active > 0:
                active_borrowers += 1
            if total_fines > 0:
                borrowers_with_fines += 1
        
        # Update statistics
        self.borrowers_total_label.config(text=f"Total Borrowers: {total_borrowers}")
        self.borrowers_active_label.config(text=f"Active Borrowers: {active_borrowers}")
        self.borrowers_fines_label.config(text=f"Borrowers with Fines: {borrowers_with_fines}")
    
    def generate_transaction_report(self):
        """Generate transaction report for date range"""
        try:
            start_date_str = self.start_date.get()
            end_date_str = self.end_date.get()
            
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            
            if start_date > end_date:
                MessageBox.show_error("Start date must be before end date")
                return
            
            # Get all transactions
            transactions = self.backend.get_all_transactions()
            
            # Filter by date range
            filtered_transactions = []
            for tx in transactions:
                tx_date = datetime.strptime(tx['borrow_date'], '%Y-%m-%d')
                if start_date <= tx_date <= end_date:
                    filtered_transactions.append(tx)
            
            # Update statistics
            total_transactions = len(filtered_transactions)
            borrowed = sum(1 for tx in filtered_transactions if tx['status'] == 'borrowed')
            returned = sum(1 for tx in filtered_transactions if tx['status'] == 'returned')
            total_fines = sum(float(tx['fine_amount'] or 0) for tx in filtered_transactions)
            
            self.transactions_total_label.config(text=f"Total Transactions: {total_transactions}")
            self.transactions_borrowed_label.config(text=f"Books Borrowed: {borrowed}")
            self.transactions_returned_label.config(text=f"Books Returned: {returned}")
            self.transactions_fines_label.config(text=f"Total Fines: ${total_fines:.2f}")
            
            # Group by date for detail tree
            daily_data = {}
            for tx in filtered_transactions:
                date = tx['borrow_date']
                if date not in daily_data:
                    daily_data[date] = {'transactions': 0, 'borrowed': 0, 'returned': 0, 'fines': 0}
                
                daily_data[date]['transactions'] += 1
                if tx['status'] == 'borrowed':
                    daily_data[date]['borrowed'] += 1
                elif tx['status'] == 'returned':
                    daily_data[date]['returned'] += 1
                
                daily_data[date]['fines'] += float(tx['fine_amount'] or 0)
            
            # Clear and populate detail tree
            for item in self.transaction_detail_tree.get_children():
                self.transaction_detail_tree.delete(item)
            
            for date, data in sorted(daily_data.items()):
                self.transaction_detail_tree.insert("", tk.END, values=(
                    date,
                    data['transactions'],
                    data['borrowed'],
                    data['returned'],
                    f"${data['fines']:.2f}"
                ))
            
            # Clear previous chart
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            # Create simple bar chart if there's data
            if daily_data:
                dates = list(sorted(daily_data.keys()))
                transaction_counts = [daily_data[date]['transactions'] for date in dates]
                
                # Create figure
                fig = Figure(figsize=(8, 4), dpi=100)
                ax = fig.add_subplot(111)
                
                # Create bar chart
                ax.bar(dates, transaction_counts)
                ax.set_xlabel('Date')
                ax.set_ylabel('Number of Transactions')
                ax.set_title('Daily Transaction Count')
                ax.tick_params(axis='x', rotation=45)
                
                # Create canvas
                canvas = FigureCanvasTkAgg(fig, self.chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            else:
                tk.Label(self.chart_frame, text="No transaction data for selected date range",
                        bg='white').pack(expand=True)
                
        except ValueError:
            MessageBox.show_error("Please enter valid dates in YYYY-MM-DD format")
        except Exception as e:
            MessageBox.show_error(f"Error generating report: {str(e)}")