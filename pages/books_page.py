import tkinter as tk
from tkinter import ttk, messagebox
from components.widgets import ModernButton, ModernTreeview, InputField, MessageBox
from backend.library_backend import LibraryBackend
from utils.helpers import validate_book_data

class BooksPage:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.backend = LibraryBackend()
        self.current_book_id = None
        
        self.setup_ui()
        self.load_books()
    
    def setup_ui(self):
        """Setup books management UI"""
        # Main container
        self.main_frame = tk.Frame(self.parent, bg='white')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(header_frame, text="📚 Books Management", 
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
        
        self.search_by = ttk.Combobox(search_frame, values=["Title", "Author", "Category", "ISBN"],
                                     state="readonly", width=15)
        self.search_by.set("Title")
        self.search_by.pack(side=tk.LEFT, padx=(0, 10))
        
        search_btn = ModernButton(search_frame, text="🔍 Search", command=self.search_books)
        search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(search_frame, text="Clear", 
                             command=self.clear_search,
                             bg='#E5E7EB', fg='black',
                             relief=tk.FLAT, padx=10)
        clear_btn.pack(side=tk.LEFT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # View Books Tab
        self.view_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.view_tab, text="View All Books")
        self.setup_view_tab()
        
        # Add Book Tab
        self.add_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.add_tab, text="Add New Book")
        self.setup_add_tab()
        
        # Edit Book Tab
        self.edit_tab = tk.Frame(self.notebook, bg='white')
        self.notebook.add(self.edit_tab, text="Edit Book")
        self.setup_edit_tab()
    
    def setup_view_tab(self):
        """Setup view books tab"""
        # Treeview for books
        columns = ("ID", "Title", "Author", "Category", "Year", "Total", "Available")
        self.books_tree = ModernTreeview(self.view_tab, columns=columns)
        self.books_tree.pack_with_scrollbars(pady=10)
        
        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=100, anchor=tk.CENTER)
        
        self.books_tree.column("Title", width=200)
        self.books_tree.column("Author", width=150)
        
        # Action buttons
        action_frame = tk.Frame(self.view_tab, bg='white')
        action_frame.pack(fill=tk.X, pady=10)
        
        ModernButton(action_frame, text="🔄 Refresh", 
                    command=self.load_books).pack(side=tk.LEFT, padx=5)
        
        ModernButton(action_frame, text="✏️ Edit Selected", 
                    command=self.edit_selected_book).pack(side=tk.LEFT, padx=5)
        
        ModernButton(action_frame, text="🗑️ Delete Selected", 
                    command=self.delete_selected_book,
                    bg='#EF4444').pack(side=tk.LEFT, padx=5)
        
        # Statistics
        stats_frame = tk.Frame(self.view_tab, bg='white')
        stats_frame.pack(fill=tk.X, pady=10)
        
        self.total_books_label = tk.Label(stats_frame, text="Total Books: 0",
                                         font=('Helvetica', 10, 'bold'),
                                         bg='white')
        self.total_books_label.pack(side=tk.LEFT, padx=20)
        
        self.available_label = tk.Label(stats_frame, text="Available: 0",
                                       font=('Helvetica', 10, 'bold'),
                                       bg='white', fg='#059669')
        self.available_label.pack(side=tk.LEFT, padx=20)
        
        self.borrowed_label = tk.Label(stats_frame, text="Borrowed: 0",
                                      font=('Helvetica', 10, 'bold'),
                                      bg='white', fg='#DC2626')
        self.borrowed_label.pack(side=tk.LEFT, padx=20)
    
    def setup_add_tab(self):
        """Setup add book tab"""
        form_frame = tk.Frame(self.add_tab, bg='white', padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Form fields
        self.add_fields = {}
        
        self.add_fields['title'] = InputField(form_frame, "Book Title *", input_type="entry")
        self.add_fields['author'] = InputField(form_frame, "Author *", input_type="entry")
        self.add_fields['isbn'] = InputField(form_frame, "ISBN", input_type="entry")
        
        # Category dropdown
        category_frame = tk.Frame(form_frame, bg='white')
        category_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(category_frame, text="Category", 
                font=('Helvetica', 10),
                bg='white', anchor=tk.W).pack(fill=tk.X)
        
        self.add_category = ttk.Combobox(category_frame, values=[
            "Fiction", "Science Fiction", "Fantasy", "Mystery", 
            "Romance", "Non-Fiction", "Biography", "Science", 
            "History", "Technology", "Other"
        ], state="readonly")
        self.add_category.set("Fiction")
        self.add_category.pack(fill=tk.X, pady=2)
        
        self.add_fields['year'] = InputField(form_frame, "Publication Year", input_type="entry")
        self.add_fields['copies'] = InputField(form_frame, "Number of Copies *", input_type="entry")
        
        # Add button
        add_btn = ModernButton(form_frame, text="➕ Add Book", 
                              command=self.add_book,
                              bg='#10B981')
        add_btn.pack(pady=20)
    
    def setup_edit_tab(self):
        """Setup edit book tab"""
        self.edit_tab_frame = tk.Frame(self.edit_tab, bg='white', padx=20, pady=20)
        self.edit_tab_frame.pack(fill=tk.BOTH, expand=True)
        
        # Select book to edit
        select_frame = tk.Frame(self.edit_tab_frame, bg='white')
        select_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(select_frame, text="Select Book to Edit:", 
                font=('Helvetica', 10, 'bold'),
                bg='white').pack(side=tk.LEFT, padx=(0, 10))
        
        self.book_selector = ttk.Combobox(select_frame, state="readonly", width=40)
        self.book_selector.pack(side=tk.LEFT, padx=(0, 10))
        self.book_selector.bind('<<ComboboxSelected>>', self.load_book_for_edit)
        
        load_btn = ModernButton(select_frame, text="📥 Load", 
                               command=self.load_selected_book)
        load_btn.pack(side=tk.LEFT)
        
        # Edit form (initially hidden)
        self.edit_form_frame = tk.Frame(self.edit_tab_frame, bg='white')
        
        self.edit_fields = {}
        self.edit_fields['title'] = InputField(self.edit_form_frame, "Book Title *", input_type="entry")
        self.edit_fields['author'] = InputField(self.edit_form_frame, "Author *", input_type="entry")
        self.edit_fields['isbn'] = InputField(self.edit_form_frame, "ISBN", input_type="entry")
        
        # Category dropdown for edit
        category_frame = tk.Frame(self.edit_form_frame, bg='white')
        category_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(category_frame, text="Category", 
                font=('Helvetica', 10),
                bg='white', anchor=tk.W).pack(fill=tk.X)
        
        self.edit_category = ttk.Combobox(category_frame, values=[
            "Fiction", "Science Fiction", "Fantasy", "Mystery", 
            "Romance", "Non-Fiction", "Biography", "Science", 
            "History", "Technology", "Other"
        ], state="readonly")
        self.edit_category.pack(fill=tk.X, pady=2)
        
        self.edit_fields['year'] = InputField(self.edit_form_frame, "Publication Year", input_type="entry")
        self.edit_fields['copies'] = InputField(self.edit_form_frame, "Number of Copies *", input_type="entry")
        
        # Update button
        update_btn = ModernButton(self.edit_form_frame, text="💾 Update Book", 
                                 command=self.update_book,
                                 bg='#F59E0B')
        update_btn.pack(pady=20)
    
    def load_books(self):
        """Load books into treeview"""
        # Clear existing items
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        # Get books from backend
        books = self.backend.get_all_books()
        
        # Add to treeview
        total_books = len(books)
        total_copies = 0
        available_copies = 0
        
        for book in books:
            self.books_tree.insert("", tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                book['year'],
                book['copies'],
                book['available_copies']
            ))
            
            total_copies += book['copies']
            available_copies += book['available_copies']
        
        # Update statistics
        self.total_books_label.config(text=f"Total Books: {total_books}")
        self.available_label.config(text=f"Available: {available_copies}")
        self.borrowed_label.config(text=f"Borrowed: {total_copies - available_copies}")
        
        # Update book selector for edit tab
        book_options = [f"{book['title']} by {book['author']} (ID: {book['book_id']})" 
                       for book in books]
        self.book_selector['values'] = book_options
        if book_options:
            self.book_selector.set(book_options[0])
    
    def search_books(self):
        """Search books based on criteria"""
        search_term = self.search_var.get()
        search_by = self.search_by.get().lower()
        
        if not search_term:
            self.load_books()
            return
        
        books = self.backend.search_books(search_term, search_by)
        
        # Clear existing items
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        
        # Add search results
        for book in books:
            self.books_tree.insert("", tk.END, values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                book['year'],
                book['copies'],
                book['available_copies']
            ))
    
    def clear_search(self):
        """Clear search and reload all books"""
        self.search_var.set("")
        self.load_books()
    
    def add_book(self):
        """Add a new book"""
        # Get form data
        title = self.add_fields['title'].get()
        author = self.add_fields['author'].get()
        isbn = self.add_fields['isbn'].get()
        category = self.add_category.get()
        year = self.add_fields['year'].get()
        copies = self.add_fields['copies'].get()
        
        # Validate
        errors = validate_book_data(title, author, copies)
        if errors:
            MessageBox.show_error("\n".join(errors))
            return
        
        try:
            year = int(year) if year else 2024
            copies = int(copies)
            
            # Add book to database
            result = self.backend.add_book(title, author, isbn, category, year, copies)
            
            if result:
                MessageBox.show_success(f"Book '{title}' added successfully!")
                
                # Clear form
                for field in self.add_fields.values():
                    field.set("")
                self.add_category.set("Fiction")
                
                # Refresh book list
                self.load_books()
                self.notebook.select(0)  # Switch to view tab
            else:
                MessageBox.show_error("Failed to add book")
        except ValueError:
            MessageBox.show_error("Please enter valid numbers for year and copies")
        except Exception as e:
            MessageBox.show_error(f"Error: {str(e)}")
    
    def edit_selected_book(self):
        """Edit the selected book"""
        selection = self.books_tree.selection()
        if not selection:
            MessageBox.show_warning("Please select a book to edit")
            return
        
        item = self.books_tree.item(selection[0])
        book_id = item['values'][0]
        
        # Switch to edit tab and load book
        self.notebook.select(2)  # Edit tab index
        self.load_book_by_id(book_id)
    
    def load_selected_book(self):
        """Load the selected book from combobox"""
        selected = self.book_selector.get()
        if not selected:
            return
        
        # Extract book ID from selection string
        try:
            book_id = int(selected.split("ID: ")[1].strip(")"))
            self.load_book_by_id(book_id)
        except:
            MessageBox.show_error("Invalid selection")
    
    def load_book_for_edit(self, event=None):
        """Load book when selected from combobox"""
        self.load_selected_book()
    
    def load_book_by_id(self, book_id):
        """Load book details by ID"""
        book = self.backend.get_book_by_id(book_id)
        if not book:
            MessageBox.show_error("Book not found")
            return
        
        self.current_book_id = book_id
        
        # Show edit form
        self.edit_form_frame.pack_forget()
        self.edit_form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Populate form
        self.edit_fields['title'].set(book['title'])
        self.edit_fields['author'].set(book['author'])
        self.edit_fields['isbn'].set(book['isbn'] or "")
        self.edit_category.set(book['category'])
        self.edit_fields['year'].set(str(book['year']))
        self.edit_fields['copies'].set(str(book['copies']))
    
    def update_book(self):
        """Update book information"""
        if not self.current_book_id:
            MessageBox.show_warning("No book selected for editing")
            return
        
        # Get form data
        title = self.edit_fields['title'].get()
        author = self.edit_fields['author'].get()
        isbn = self.edit_fields['isbn'].get()
        category = self.edit_category.get()
        year = self.edit_fields['year'].get()
        copies = self.edit_fields['copies'].get()
        
        # Validate
        errors = validate_book_data(title, author, copies)
        if errors:
            MessageBox.show_error("\n".join(errors))
            return
        
        try:
            year = int(year) if year else 2024
            copies = int(copies)
            
            # Update book in database
            success = self.backend.update_book(self.current_book_id, title, author, 
                                             isbn, category, year, copies)
            
            if success:
                MessageBox.show_success(f"Book '{title}' updated successfully!")
                
                # Refresh book list
                self.load_books()
                self.notebook.select(0)  # Switch to view tab
            else:
                MessageBox.show_error("Failed to update book")
        except ValueError:
            MessageBox.show_error("Please enter valid numbers for year and copies")
        except Exception as e:
            MessageBox.show_error(f"Error: {str(e)}")
    
    def delete_selected_book(self):
        """Delete the selected book"""
        selection = self.books_tree.selection()
        if not selection:
            MessageBox.show_warning("Please select a book to delete")
            return
        
        item = self.books_tree.item(selection[0])
        book_id = item['values'][0]
        title = item['values'][1]
        
        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", 
                                     f"Are you sure you want to delete '{title}'?\nThis action cannot be undone!")
        if not confirm:
            return
        
        # Delete book
        success, message = self.backend.delete_book(book_id)
        
        if success:
            MessageBox.show_success(message)
            self.load_books()
        else:
            MessageBox.show_error(message)