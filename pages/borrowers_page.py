import tkinter as tk
from tkinter import ttk, messagebox
from components.widgets import ModernButton, ModernTreeview, InputField, MessageBox
from backend.library_backend import LibraryBackend
from utils.helpers import validate_borrower_data, validate_email, validate_phone

class BorrowersPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.backend = LibraryBackend()
        self.current_borrower_id = None
        
        self.setup_ui()
        self.load_borrowers()
    
    def setup_ui(self):
        """Setup borrowers management UI"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="👥 Borrowers Management", 
                font=('Helvetica', 24, 'bold'),
                bg='white', fg='#1E3A8A').pack(side=tk.LEFT)
        
        # Search frame
        search_frame = tk.Frame(self.main_frame, bg='white')
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", 
                font=('Helvetica', 10),
                bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                    font=('Helvetica', 10), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(search_frame, text="By:", 
                font=('Helvetica', 10),
                bg='white').pack(side=tk.LEFT, padx=(0, 5))
        
        self.search_by = ttk.Combobox(search_frame, values=["Name", "Email", "Phone"],
                                     state="readonly", width=15)
        self.search_by.set("Name")
        self.search_by.pack(side=tk.LEFT, padx=(0, 10))
        
        search_btn = ModernButton(search_frame, text="🔍 Search", command=self.search_borrowers)
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(search_frame, text="Clear", 
                             command=self.clear_search,
                             bg='#E5E7EB', fg='black',
                             relief=tk.FLAT, padx=10)
        clear_btn.pack(side=tk.LEFT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # View Borrowers Tab
        self.view_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.view_tab, text="View All Borrowers")
        self.setup_view_tab()
        
        # Add Borrower Tab
        self.add_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.add_tab, text="Add New Borrower")
        self.setup_add_tab()
        
        # Edit Borrower Tab
        self.edit_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.edit_tab, text="Edit Borrower")
        self.setup_edit_tab()
    
    def setup_view_tab(self):
        """Setup view borrowers tab"""
        # Treeview for borrowers
        columns = ("ID", "Name", "Email", "Phone", "Active Loans", "Joined")
        self.borrowers_tree = ModernTreeview(self.view_tab, columns=columns)
        self.borrowers_tree.pack_with_scrollbars(pady=10)
        
        for col in columns:
            self.borrowers_tree.heading(col, text=col)
            self.borrowers_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.borrowers_tree.column("Name", width=150)
        self.borrowers_tree.column("Email", width=200)
        
        # Action buttons
        action_frame = tk.Frame(self.view_tab, bg='white')
        action_frame.pack(fill=tk.X, pady=10)
        
        ModernButton(action_frame, text="🔄 Refresh", 
                    command=self.load_borrowers).pack(side=tk.LEFT, padx=5)
        
        ModernButton(action_frame, text="✏️ Edit Selected", 
                    command=self.edit_selected_borrower).pack(side=tk.LEFT, padx=5)
        
        ModernButton(action_frame, text="🗑️ Delete Selected", 
                    command=self.delete_selected_borrower,
                    bg='#EF4444').pack(side=tk.LEFT, padx=5)
        
        # Statistics
        stats_frame = tk.Frame(self.view_tab, bg='white')
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.total_borrowers_label = tk.Label(stats_frame, text="Total Borrowers: 0",
                                             font=('Helvetica', 10, 'bold'),
                                             bg='white')
        self.total_borrowers_label.pack(side=tk.LEFT, padx=20)
        
        self.active_loans_label = tk.Label(stats_frame, text="Active Loans: 0",
                                          font=('Helvetica', 10, 'bold'),
                                          bg='white', fg='#059669')
        self.active_loans_label.pack(side=tk.LEFT, padx=20)
        
        self.overdue_label = tk.Label(stats_frame, text="Overdue: 0",
                                     font=('Helvetica', 10, 'bold'),
                                     bg='white', fg='#DC2626')
        self.overdue_label.pack(side=tk.LEFT, padx=20)
    
    def setup_add_tab(self):
        """Setup add borrower tab"""
        form_frame = tk.Frame(self.add_tab, bg='white', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        self.add_fields = {}
        
        self.add_fields['name'] = InputField(form_frame, "Full Name *", input_type="entry")
        self.add_fields['email'] = InputField(form_frame, "Email *", input_type="entry")
        self.add_fields['phone'] = InputField(form_frame, "Phone Number", input_type="entry")
        self.add_fields['address'] = InputField(form_frame, "Address", input_type="text", height=4)
        
        # Add button
        add_btn = ModernButton(form_frame, text="➕ Add Borrower", 
                              command=self.add_borrower,
                              bg='#10B981')
        add_btn.pack(pady=20)
    
    def setup_edit_tab(self):
        """Setup edit borrower tab"""
        self.edit_tab_frame = tk.Frame(self.edit_tab, bg='white', padx=20, pady=20)
        self.edit_tab_frame.pack(fill=tk.BOTH, expand=True)
        
        # Select borrower to edit
        select_frame = tk.Frame(self.edit_tab_frame, bg='white')
        select_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(select_frame, text="Select Borrower to Edit:", 
                font=('Helvetica', 10, 'bold'),
                bg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        self.borrower_selector = ttk.Combobox(select_frame, state="readonly", width=40)
        self.borrower_selector.pack(side=tk.LEFT, padx=(0, 10))
        self.borrower_selector.bind('<<ComboboxSelected>>', self.load_borrower_for_edit)
        
        load_btn = ModernButton(select_frame, text="📥 Load", 
                               command=self.load_selected_borrower)
        load_btn.pack(side=tk.LEFT)
        
        # Edit form (initially hidden)
        self.edit_form_frame = tk.Frame(self.edit_tab_frame, bg='white')
        
        self.edit_fields = {}
        self.edit_fields['name'] = InputField(self.edit_form_frame, "Full Name *", input_type="entry")
        self.edit_fields['email'] = InputField(self.edit_form_frame, "Email *", input_type="entry")
        self.edit_fields['phone'] = InputField(self.edit_form_frame, "Phone Number", input_type="entry")
        self.edit_fields['address'] = InputField(self.edit_form_frame, "Address", input_type="text", height=4)
        
        # Update button
        update_btn = ModernButton(self.edit_form_frame, text="💾 Update Borrower", 
                                 command=self.update_borrower,
                                 bg='#F59E0B')
        update_btn.pack(pady=20)
    
    def load_borrowers(self):
        """Load borrowers into treeview"""
        # Clear existing items
        for item in self.borrowers_tree.get_children():
            self.borrowers_tree.delete(item)
        
        # Get borrowers from backend
        borrowers = self.backend.get_all_borrowers()
        
        # Add to treeview
        total_borrowers = len(borrowers)
        total_active_loans = 0
        
        for borrower in borrowers:
            self.borrowers_tree.insert("", tk.END, values=(
                borrower['borrower_id'],
                borrower['name'],
                borrower['email'],
                borrower['phone'] or "",
                borrower['active_loans'],
                borrower['registered_date']
            ))
            
            total_active_loans += borrower['active_loans']
        
        # Update statistics
        self.total_borrowers_label.config(text=f"Total Borrowers: {total_borrowers}")
        self.active_loans_label.config(text=f"Active Loans: {total_active_loans}")
        
        # Get overdue count
        overdue = self.backend.get_overdue_books()
        self.overdue_label.config(text=f"Overdue: {len(overdue)}")
        
        # Update borrower selector for edit tab
        borrower_options = [f"{borrower['name']} ({borrower['email']})" 
                           for borrower in borrowers]
        self.borrower_selector['values'] = borrower_options
        if borrower_options:
            self.borrower_selector.set(borrower_options[0])
    
    def search_borrowers(self):
        """Search borrowers based on criteria"""
        search_term = self.search_var.get()
        search_by = self.search_by.get().lower()
        
        if not search_term:
            self.load_borrowers()
            return
        
        borrowers = self.backend.search_borrowers(search_term, search_by)
        
        # Clear existing items
        for item in self.borrowers_tree.get_children():
            self.borrowers_tree.delete(item)
        
        # Add search results
        for borrower in borrowers:
            # Get active loans count
            active_loans = self.backend.get_active_loans()
            borrower_active_loans = sum(1 for loan in active_loans 
                                      if loan['borrower_id'] == borrower['borrower_id'])
            
            self.borrowers_tree.insert("", tk.END, values=(
                borrower['borrower_id'],
                borrower['name'],
                borrower['email'],
                borrower['phone'] or "",
                borrower_active_loans,
                borrower['created_date']
            ))
    
    def clear_search(self):
        """Clear search and reload all borrowers"""
        self.search_var.set("")
        self.load_borrowers()
    
    def add_borrower(self):
        """Add a new borrower"""
        # Get form data
        name = self.add_fields['name'].get()
        email = self.add_fields['email'].get()
        phone = self.add_fields['phone'].get()
        address = self.add_fields['address'].get()
        
        # Validate
        errors = validate_borrower_data(name, email)
        if errors:
            MessageBox.show_error("\n".join(errors))
            return
        
        if phone and not validate_phone(phone):
            MessageBox.show_error("Please enter a valid phone number")
            return
        
        if not validate_email(email):
            MessageBox.show_error("Please enter a valid email address")
            return
        
        # Add borrower to database
        success, message = self.backend.add_borrower(name, email, phone, address)
        
        if success:
            MessageBox.show_success(message)
            
            # Clear form
            for field in self.add_fields.values():
                field.set("")
            
            # Refresh borrower list
            self.load_borrowers()
            self.notebook.select(0)  # Switch to view tab
        else:
            MessageBox.show_error(message)
    
    def edit_selected_borrower(self):
        """Edit the selected borrower"""
        selection = self.borrowers_tree.selection()
        if not selection:
            MessageBox.show_warning("Please select a borrower to edit")
            return
        
        item = self.borrowers_tree.item(selection[0])
        borrower_id = item['values'][0]
        
        # Switch to edit tab and load borrower
        self.notebook.select(2)  # Edit tab index
        self.load_borrower_by_id(borrower_id)
    
    def load_selected_borrower(self):
        """Load the selected borrower from combobox"""
        selected = self.borrower_selector.get()
        if not selected:
            return
        
        # Find borrower by email (extracted from selection)
        try:
            email = selected.split("(")[1].strip(")")
            borrowers = self.backend.get_all_borrowers()
            borrower = next((b for b in borrowers if b['email'] == email), None)
            
            if borrower:
                self.load_borrower_by_id(borrower['borrower_id'])
        except:
            MessageBox.show_error("Invalid selection")
    
    def load_borrower_for_edit(self, event=None):
        """Load borrower when selected from combobox"""
        self.load_selected_borrower()
    
    def load_borrower_by_id(self, borrower_id):
        """Load borrower details by ID"""
        borrower = self.backend.get_borrower_by_id(borrower_id)
        if not borrower:
            MessageBox.show_error("Borrower not found")
            return
        
        self.current_borrower_id = borrower_id
        
        # Show edit form
        self.edit_form_frame.pack_forget()
        self.edit_form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Populate form
        self.edit_fields['name'].set(borrower['name'])
        self.edit_fields['email'].set(borrower['email'])
        self.edit_fields['phone'].set(borrower['phone'] or "")
        self.edit_fields['address'].set(borrower['address'] or "")
    
    def update_borrower(self):
        """Update borrower information"""
        if not self.current_borrower_id:
            MessageBox.show_warning("No borrower selected for editing")
            return
        
        # Get form data
        name = self.edit_fields['name'].get()
        email = self.edit_fields['email'].get()
        phone = self.edit_fields['phone'].get()
        address = self.edit_fields['address'].get()
        
        # Validate
        errors = validate_borrower_data(name, email)
        if errors:
            MessageBox.show_error("\n".join(errors))
            return
        
        if phone and not validate_phone(phone):
            MessageBox.show_error("Please enter a valid phone number")
            return
        
        if not validate_email(email):
            MessageBox.show_error("Please enter a valid email address")
            return
        
        # Update borrower in database
        success, message = self.backend.update_borrower(self.current_borrower_id, 
                                                       name, email, phone, address)
        
        if success:
            MessageBox.show_success(message)
            
            # Refresh borrower list
            self.load_borrowers()
            self.notebook.select(0)  # Switch to view tab
        else:
            MessageBox.show_error(message)
    
    def delete_selected_borrower(self):
        """Delete the selected borrower"""
        selection = self.borrowers_tree.selection()
        if not selection:
            MessageBox.show_warning("Please select a borrower to delete")
            return
        
        item = self.borrowers_tree.item(selection[0])
        borrower_id = item['values'][0]
        name = item['values'][1]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete '{name}'?\nThis action cannot be undone!")
        if not confirm:
            return
        
        # Delete borrower
        success, message = self.backend.delete_borrower(borrower_id)
        
        if success:
            MessageBox.show_success(message)
            self.load_borrowers()
        else:
            MessageBox.show_error(message)