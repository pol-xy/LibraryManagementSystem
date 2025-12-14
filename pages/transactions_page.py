import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from components.widgets import ModernButton, ModernTreeview, InputField, MessageBox
from backend.library_backend import LibraryBackend
from utils.helpers import get_current_date, calculate_due_date

class TransactionsPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.backend = LibraryBackend()
        
        self.setup_ui()
        self.load_transactions()
    
    def setup_ui(self):
        """Setup transactions management UI"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="🔄 Transactions Management", 
                font=('Helvetica', 24, 'bold'),
                bg='white', fg='#1E3A8A').pack(side=tk.LEFT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Borrow Book Tab
        self.borrow_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.borrow_tab, text="Borrow Book")
        self.setup_borrow_tab()
        
        # Return Book Tab
        self.return_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.return_tab, text="Return Book")
        self.setup_return_tab()
        
        # Active Loans Tab
        self.active_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.active_tab, text="Active Loans")
        self.setup_active_tab()
        
        # Transaction History Tab
        self.history_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.history_tab, text="Transaction History")
        self.setup_history_tab()
    
    def setup_borrow_tab(self):
        """Setup borrow book tab"""
        form_frame = tk.Frame(self.borrow_tab, bg='white', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Book selection
        book_frame = tk.Frame(form_frame, bg='white')
        book_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(book_frame, text="Select Book:", 
                font=('Helvetica', 10, 'bold'),
                bg='white').pack(anchor=tk.W, pady=(0, 5))
        
        self.book_selector = ttk.Combobox(book_frame, state="readonly", width=50)
        self.book_selector.pack(fill=tk.X, pady=(0, 10))
        
        # Borrower selection
        borrower_frame = tk.Frame(form_frame, bg='white')
        borrower_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(borrower_frame, text="Select Borrower:", 
                font=('Helvetica', 10, 'bold'),
                bg='white').pack(anchor=tk.W, pady=(0, 5))
        
        self.borrower_selector = ttk.Combobox(borrower_frame, state="readonly", width=50)
        self.borrower_selector.pack(fill=tk.X, pady=(0, 10))
        
        # Date selection
        dates_frame = tk.Frame(form_frame, bg='white')
        dates_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Borrow date
        borrow_date_frame = tk.Frame(dates_frame, bg='white')
        borrow_date_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Label(borrow_date_frame, text="Borrow Date:", 
                font=('Helvetica', 10),
                bg='white').pack(anchor=tk.W, pady=(0, 5))
        
        self.borrow_date = tk.Entry(borrow_date_frame, font=('Helvetica', 10))
        self.borrow_date.insert(0, get_current_date())
        self.borrow_date.pack(fill=tk.X)
        
        # Due date
        due_date_frame = tk.Frame(dates_frame, bg='white')
        due_date_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Label(due_date_frame, text="Due Date:", 
                font=('Helvetica', 10),
                bg='white').pack(anchor=tk.W, pady=(0, 5))
        
        self.due_date = tk.Entry(due_date_frame, font=('Helvetica', 10))
        self.due_date.insert(0, calculate_due_date(get_current_date()))
        self.due_date.pack(fill=tk.X)
        
        # Info label
        self.borrow_info_label = tk.Label(form_frame, text="", 
                                         font=('Helvetica', 10),
                                         bg='white', fg='#DC2626')
        self.borrow_info_label.pack(fill=tk.X, pady=(0, 20))
        
        # Borrow button
        borrow_btn = ModernButton(form_frame, text="📖 Borrow Book", 
                                 command=self.borrow_book,
                                 bg='#10B981')
        borrow_btn.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(form_frame, text="🔄 Refresh Lists", 
                               command=self.refresh_lists,
                               bg='#E5E7EB', fg='black',
                               relief=tk.FLAT, padx=15)
        refresh_btn.pack(pady=5)
        
        # Initial load of lists
        self.refresh_lists()
    
    def setup_return_tab(self):
        """Setup return book tab"""
        form_frame = tk.Frame(self.return_tab, bg='white', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Active loans selection
        loans_frame = tk.Frame(form_frame, bg='white')
        loans_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(loans_frame, text="Select Active Loan:", 
                font=('Helvetica', 10, 'bold'),
                bg='white').pack(anchor=tk.W, pady=(0, 5))
        
        self.loan_selector = ttk.Combobox(loans_frame, state="readonly", width=50)
        self.loan_selector.pack(fill=tk.X, pady=(0, 10))
        self.loan_selector.bind('<<ComboboxSelected>>', self.display_loan_details)
        
        # Loan details frame
        self.details_frame = tk.LabelFrame(form_frame, text="Loan Details", 
                                          font=('Helvetica', 10, 'bold'),
                                          bg='white', padx=15, pady=15)
        
        self.book_title_label = tk.Label(self.details_frame, text="Book: ", 
                                        font=('Helvetica', 10),
                                        bg='white', anchor=tk.W)
        self.book_title_label.pack(fill=tk.X, pady=2)
        
        self.borrower_label = tk.Label(self.details_frame, text="Borrower: ", 
                                      font=('Helvetica', 10),
                                      bg='white', anchor=tk.W)
        self.borrower_label.pack(fill=tk.X, pady=2)
        
        self.borrow_date_label = tk.Label(self.details_frame, text="Borrow Date: ", 
                                         font=('Helvetica', 10),
                                         bg='white', anchor=tk.W)
        self.borrow_date_label.pack(fill=tk.X, pady=2)
        
        self.due_date_label = tk.Label(self.details_frame, text="Due Date: ", 
                                      font=('Helvetica', 10),
                                      bg='white', anchor=tk.W)
        self.due_date_label.pack(fill=tk.X, pady=2)
        
        self.overdue_label = tk.Label(self.details_frame, text="", 
                                     font=('Helvetica', 10, 'bold'),
                                     bg='white', fg='#DC2626')
        self.overdue_label.pack(fill=tk.X, pady=2)
        
        # Return date
        return_date_frame = tk.Frame(form_frame, bg='white')
        return_date_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(return_date_frame, text="Return Date:", 
                font=('Helvetica', 10),
                bg='white').pack(anchor=tk.W, pady=(0, 5))
        
        self.return_date_entry = tk.Entry(return_date_frame, font=('Helvetica', 10))
        self.return_date_entry.insert(0, get_current_date())
        self.return_date_entry.pack(fill=tk.X)
        
        # Return button
        return_btn = ModernButton(form_frame, text="📚 Return Book", 
                                 command=self.return_book,
                                 bg='#F59E0B')
        return_btn.pack(pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(form_frame, text="🔄 Refresh Active Loans", 
                               command=self.refresh_active_loans,
                               bg='#E5E7EB', fg='black',
                               relief=tk.FLAT, padx=15)
        refresh_btn.pack(pady=5)
        
        # Initial load of active loans
        self.refresh_active_loans()
    
    def setup_active_tab(self):
        """Setup active loans tab"""
        # Treeview for active loans
        columns = ("ID", "Book", "Borrower", "Borrow Date", "Due Date", "Days Overdue", "Status")
        self.active_tree = ModernTreeview(self.active_tab, columns=columns)
        self.active_tree.pack_with_scrollbars(pady=10, padx=20)
        
        for col in columns:
            self.active_tree.heading(col, text=col)
            self.active_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.active_tree.column("Book", width=150)
        self.active_tree.column("Borrower", width=150)
        
        # Statistics frame
        stats_frame = tk.Frame(self.active_tab, bg='white')
        stats_frame.pack(fill=tk.X, pady=10, padx=20)
        
        self.total_active_label = tk.Label(stats_frame, text="Total Active: 0",
                                          font=('Helvetica', 10, 'bold'),
                                          bg='white')
        self.total_active_label.pack(side=tk.LEFT, padx=20)
        
        self.total_overdue_label = tk.Label(stats_frame, text="Overdue: 0",
                                           font=('Helvetica', 10, 'bold'),
                                           bg='white', fg='#DC2626')
        self.total_overdue_label.pack(side=tk.LEFT, padx=20)
        
        self.total_fines_label = tk.Label(stats_frame, text="Total Fines: $0.00",
                                         font=('Helvetica', 10, 'bold'),
                                         bg='white', fg='#059669')
        self.total_fines_label.pack(side=tk.LEFT, padx=20)
        
        # Action buttons
        action_frame = tk.Frame(self.active_tab, bg='white')
        action_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ModernButton(action_frame, text="🔄 Refresh", 
                    command=self.load_active_loans).pack(side=tk.LEFT, padx=5)
    
    def setup_history_tab(self):
        """Setup transaction history tab"""
        # Treeview for transaction history
        columns = ("ID", "Book", "Borrower", "Borrow Date", "Due Date", "Return Date", "Status", "Fine")
        self.history_tree = ModernTreeview(self.history_tab, columns=columns)
        self.history_tree.pack_with_scrollbars(pady=10, padx=20)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.history_tree.column("Book", width=150)
        self.history_tree.column("Borrower", width=150)
        
        # Filter frame
        filter_frame = tk.Frame(self.history_tab, bg='white')
        filter_frame.pack(fill=tk.X, pady=10, padx=20)
        
        tk.Label(filter_frame, text="Filter by Status:", 
                font=('Helvetica', 10),
                bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_filter = ttk.Combobox(filter_frame, values=["All", "borrowed", "returned", "overdue"],
                                         state="readonly", width=15)
        self.status_filter.set("All")
        self.status_filter.pack(side=tk.LEFT, padx=(0, 10))
        
        ModernButton(filter_frame, text="🔍 Apply Filter", 
                    command=self.filter_history).pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(filter_frame, text="Clear", 
                             command=self.clear_filter,
                             bg='#E5E7EB', fg='black',
                             relief=tk.FLAT, padx=10)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        action_frame = tk.Frame(self.history_tab, bg='white')
        action_frame.pack(fill=tk.X, pady=10, padx=20)
        
        ModernButton(action_frame, text="🔄 Refresh", 
                    command=self.load_transactions).pack(side=tk.LEFT, padx=5)
    
    def refresh_lists(self):
        """Refresh book and borrower lists for borrowing"""
        # Get available books
        available_books = self.backend.get_available_books()
        book_options = [f"{book['title']} by {book['author']} ({book['available_copies']} available)" 
                       for book in available_books]
        self.book_selector['values'] = book_options
        if book_options:
            self.book_selector.set(book_options[0])
        
        # Get all borrowers
        borrowers = self.backend.get_all_borrowers()
        borrower_options = [f"{borrower['name']} ({borrower['email']})" 
                           for borrower in borrowers]
        self.borrower_selector['values'] = borrower_options
        if borrower_options:
            self.borrower_selector.set(borrower_options[0])
        
        # Clear info label
        self.borrow_info_label.config(text="")
    
    def borrow_book(self):
        """Process book borrowing"""
        # Get selected book
        book_selection = self.book_selector.get()
        borrower_selection = self.borrower_selector.get()
        
        if not book_selection or not borrower_selection:
            MessageBox.show_warning("Please select both book and borrower")
            return
        
        # Extract book ID from selection
        try:
            # Find book by matching title
            available_books = self.backend.get_available_books()
            book = None
            for b in available_books:
                display_text = f"{b['title']} by {b['author']} ({b['available_copies']} available)"
                if display_text == book_selection:
                    book = b
                    break
            
            if not book:
                MessageBox.show_error("Selected book not found")
                return
            
            book_id = book['book_id']
        except:
            MessageBox.show_error("Invalid book selection")
            return
        
        # Extract borrower ID from selection
        try:
            # Find borrower by matching email
            email = borrower_selection.split("(")[1].strip(")")
            borrowers = self.backend.get_all_borrowers()
            borrower = next((b for b in borrowers if b['email'] == email), None)
            
            if not borrower:
                MessageBox.show_error("Selected borrower not found")
                return
            
            borrower_id = borrower['borrower_id']
        except:
            MessageBox.show_error("Invalid borrower selection")
            return
        
        # Get dates
        borrow_date_str = self.borrow_date.get()
        due_date_str = self.due_date.get()
        
        try:
            borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d').date()
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            
            if due_date <= borrow_date:
                MessageBox.show_error("Due date must be after borrow date")
                return
        except ValueError:
            MessageBox.show_error("Please enter valid dates in YYYY-MM-DD format")
            return
        
        # Process borrow
        transaction_id, message = self.backend.borrow_book(book_id, borrower_id, 
                                                          borrow_date, due_date)
        
        if transaction_id:
            MessageBox.show_success(f"{message}\nTransaction ID: {transaction_id}")
            
            # Clear form and refresh
            self.borrow_date.delete(0, tk.END)
            self.borrow_date.insert(0, get_current_date())
            self.due_date.delete(0, tk.END)
            self.due_date.insert(0, calculate_due_date(get_current_date()))
            
            self.refresh_lists()
            self.load_active_loans()
            self.load_transactions()
        else:
            MessageBox.show_error(message)
    
    def refresh_active_loans(self):
        """Refresh active loans for return tab"""
        active_loans = self.backend.get_active_loans()
        loan_options = [f"{loan['title']} borrowed by {loan['borrower_name']} (Due: {loan['due_date']})" 
                       for loan in active_loans]
        self.loan_selector['values'] = loan_options
        if loan_options:
            self.loan_selector.set(loan_options[0])
            self.display_loan_details()
    
    def display_loan_details(self, event=None):
        """Display details of selected loan"""
        selection = self.loan_selector.get()
        if not selection:
            return
        
        # Find the selected loan
        active_loans = self.backend.get_active_loans()
        selected_loan = None
        for loan in active_loans:
            display_text = f"{loan['title']} borrowed by {loan['borrower_name']} (Due: {loan['due_date']})"
            if display_text == selection:
                selected_loan = loan
                break
        
        if not selected_loan:
            return
        
        # Update details frame
        self.book_title_label.config(text=f"Book: {selected_loan['title']}")
        self.borrower_label.config(text=f"Borrower: {selected_loan['borrower_name']}")
        self.borrow_date_label.config(text=f"Borrow Date: {selected_loan['borrow_date']}")
        self.due_date_label.config(text=f"Due Date: {selected_loan['due_date']}")
        
        # Check if overdue
        if selected_loan['days_overdue'] > 0:
            fine = selected_loan['days_overdue'] * 5.00
            self.overdue_label.config(text=f"⚠️ Overdue by {selected_loan['days_overdue']} days - Fine: ${fine:.2f}")
        else:
            self.overdue_label.config(text="")
        
        # Show details frame
        self.details_frame.pack(fill=tk.X, pady=15)
    
    def return_book(self):
        """Process book return"""
        selection = self.loan_selector.get()
        if not selection:
            MessageBox.show_warning("Please select a loan to return")
            return
        
        # Find the selected loan
        active_loans = self.backend.get_active_loans()
        selected_loan = None
        for loan in active_loans:
            display_text = f"{loan['title']} borrowed by {loan['borrower_name']} (Due: {loan['due_date']})"
            if display_text == selection:
                selected_loan = loan
                break
        
        if not selected_loan:
            MessageBox.show_error("Selected loan not found")
            return
        
        # Get return date
        return_date_str = self.return_date_entry.get()
        try:
            return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()
        except ValueError:
            MessageBox.show_error("Please enter a valid date in YYYY-MM-DD format")
            return
        
        # Process return
        success, message = self.backend.return_book(selected_loan['transaction_id'], return_date)
        
        if success:
            MessageBox.show_success(message)
            
            # Clear and refresh
            self.return_date_entry.delete(0, tk.END)
            self.return_date_entry.insert(0, get_current_date())
            self.details_frame.pack_forget()
            
            self.refresh_active_loans()
            self.load_active_loans()
            self.load_transactions()
        else:
            MessageBox.show_error(message)
    
    def load_active_loans(self):
        """Load active loans into treeview"""
        # Clear existing items
        for item in self.active_tree.get_children():
            self.active_tree.delete(item)
        
        # Get active loans
        active_loans = self.backend.get_active_loans()
        
        # Add to treeview
        total_active = len(active_loans)
        total_overdue = 0
        total_fines = 0
        
        for loan in active_loans:
            status = "Overdue" if loan['days_overdue'] > 0 else "On Time"
            fine = loan['days_overdue'] * 5.00 if loan['days_overdue'] > 0 else 0
            
            self.active_tree.insert("", tk.END, values=(
                loan['transaction_id'],
                loan['title'],
                loan['borrower_name'],
                loan['borrow_date'],
                loan['due_date'],
                loan['days_overdue'],
                status
            ))
            
            if loan['days_overdue'] > 0:
                total_overdue += 1
                total_fines += fine
        
        # Update statistics
        self.total_active_label.config(text=f"Total Active: {total_active}")
        self.total_overdue_label.config(text=f"Overdue: {total_overdue}")
        self.total_fines_label.config(text=f"Total Fines: ${total_fines:.2f}")
    
    def load_transactions(self):
        """Load transaction history"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get all transactions
        transactions = self.backend.get_all_transactions()
        
        # Add to treeview
        for tx in transactions:
            fine_amount = f"${float(tx['fine_amount']):.2f}" if tx['fine_amount'] else "$0.00"
            
            self.history_tree.insert("", tk.END, values=(
                tx['transaction_id'],
                tx['title'],
                tx['borrower_name'],
                tx['borrow_date'],
                tx['due_date'],
                tx['return_date'] or "Not returned",
                tx['status'].title(),
                fine_amount
            ))
    
    def filter_history(self):
        """Filter transaction history by status"""
        status_filter = self.status_filter.get()
        if status_filter == "All":
            self.load_transactions()
            return
        
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Get filtered transactions
        transactions = self.backend.get_all_transactions()
        filtered = [tx for tx in transactions if tx['status'] == status_filter.lower()]
        
        # Add to treeview
        for tx in filtered:
            fine_amount = f"${float(tx['fine_amount']):.2f}" if tx['fine_amount'] else "$0.00"
            
            self.history_tree.insert("", tk.END, values=(
                tx['transaction_id'],
                tx['title'],
                tx['borrower_name'],
                tx['borrow_date'],
                tx['due_date'],
                tx['return_date'] or "Not returned",
                tx['status'].title(),
                fine_amount
            ))
    
    def clear_filter(self):
        """Clear history filter"""
        self.status_filter.set("All")
        self.load_transactions()