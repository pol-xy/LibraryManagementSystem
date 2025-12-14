from database.db_connection import get_db_connection
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class LibraryBackend:
    def __init__(self):
        self.db = get_db_connection()
    
    # ========== BOOK MANAGEMENT ==========
    
    def get_all_books(self):
        """Get all books from database"""
        query = """
        SELECT book_id, title, author, isbn, category, year, 
               copies, available_copies, 
               DATE(created_at) as created_date
        FROM books 
        ORDER BY title
        """
        return self.db.execute_query(query, fetch=True) or []
    
    def get_book_by_id(self, book_id):
        """Get book details by ID"""
        query = "SELECT * FROM books WHERE book_id = %s"
        result = self.db.execute_query(query, (book_id,), fetch=True)
        return result[0] if result else None
    
    def search_books(self, search_term, search_by="title"):
        """Search books by various criteria"""
        if search_by == "title":
            query = "SELECT * FROM books WHERE title LIKE %s ORDER BY title"
        elif search_by == "author":
            query = "SELECT * FROM books WHERE author LIKE %s ORDER BY author"
        elif search_by == "category":
            query = "SELECT * FROM books WHERE category LIKE %s ORDER BY category"
        elif search_by == "isbn":
            query = "SELECT * FROM books WHERE isbn LIKE %s ORDER BY isbn"
        else:
            query = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s ORDER BY title"
            return self.db.execute_query(query, (f"%{search_term}%", f"%{search_term}%"), fetch=True) or []
        
        return self.db.execute_query(query, (f"%{search_term}%",), fetch=True) or []
    
    def add_book(self, title, author, isbn, category, year, copies):
        """Add a new book to the database"""
        query = """
        INSERT INTO books (title, author, isbn, category, year, copies, available_copies)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (title, author, isbn, category, year, copies, copies))
    
    def update_book(self, book_id, title, author, isbn, category, year, copies):
        """Update book information"""
        # Get current book to calculate available copies
        current_book = self.get_book_by_id(book_id)
        if not current_book:
            return False
        
        # Calculate new available copies
        borrowed_copies = current_book['copies'] - current_book['available_copies']
        new_available = max(0, copies - borrowed_copies)
        
        query = """
        UPDATE books 
        SET title = %s, author = %s, isbn = %s, category = %s, 
            year = %s, copies = %s, available_copies = %s
        WHERE book_id = %s
        """
        result = self.db.execute_query(query, (title, author, isbn, category, year, copies, new_available, book_id))
        return result is not None
    
    def delete_book(self, book_id):
        """Delete a book from database"""
        # Check if book is currently borrowed
        check_query = """
        SELECT COUNT(*) as active_loans 
        FROM transactions 
        WHERE book_id = %s AND status = 'borrowed'
        """
        result = self.db.execute_query(check_query, (book_id,), fetch=True)
        
        if result and result[0]['active_loans'] > 0:
            return False, f"Cannot delete! Book has {result[0]['active_loans']} active loan(s)."
        
        query = "DELETE FROM books WHERE book_id = %s"
        result = self.db.execute_query(query, (book_id,))
        return result is not None, "Book deleted successfully" if result else "Failed to delete book"
    
    def get_book_statistics(self):
        """Get book statistics"""
        query = """
        SELECT 
            COUNT(*) as total_books,
            SUM(copies) as total_copies,
            SUM(available_copies) as available_copies,
            COUNT(CASE WHEN available_copies = 0 THEN 1 END) as unavailable_books,
            (SELECT category FROM books GROUP BY category ORDER BY COUNT(*) DESC LIMIT 1) as popular_category
        FROM books
        """
        result = self.db.execute_query(query, fetch=True)
        return result[0] if result else {}
    
    # ========== BORROWER MANAGEMENT ==========
    
    def get_all_borrowers(self):
        """Get all borrowers from database"""
        query = """
        SELECT borrower_id, name, email, phone, address, 
               DATE(created_date) as registered_date,
               (SELECT COUNT(*) FROM transactions 
                WHERE borrower_id = borrowers.borrower_id AND status = 'borrowed') as active_loans
        FROM borrowers 
        ORDER BY name
        """
        return self.db.execute_query(query, fetch=True) or []
    
    def get_borrower_by_id(self, borrower_id):
        """Get borrower details by ID"""
        query = "SELECT * FROM borrowers WHERE borrower_id = %s"
        result = self.db.execute_query(query, (borrower_id,), fetch=True)
        return result[0] if result else None
    
    def search_borrowers(self, search_term, search_by="name"):
        """Search borrowers by various criteria"""
        if search_by == "name":
            query = "SELECT * FROM borrowers WHERE name LIKE %s ORDER BY name"
        elif search_by == "email":
            query = "SELECT * FROM borrowers WHERE email LIKE %s ORDER BY email"
        elif search_by == "phone":
            query = "SELECT * FROM borrowers WHERE phone LIKE %s ORDER BY phone"
        else:
            query = "SELECT * FROM borrowers WHERE name LIKE %s OR email LIKE %s ORDER BY name"
            return self.db.execute_query(query, (f"%{search_term}%", f"%{search_term}%"), fetch=True) or []
        
        return self.db.execute_query(query, (f"%{search_term}%",), fetch=True) or []
    
    def add_borrower(self, name, email, phone, address):
        """Add a new borrower to the database"""
        # Check if email already exists
        check_query = "SELECT borrower_id FROM borrowers WHERE email = %s"
        existing = self.db.execute_query(check_query, (email,), fetch=True)
        
        if existing:
            return False, "Email already registered"
        
        query = """
        INSERT INTO borrowers (name, email, phone, address)
        VALUES (%s, %s, %s, %s)
        """
        result = self.db.execute_query(query, (name, email, phone, address))
        return result is not None, "Borrower registered successfully" if result else "Failed to register borrower"
    
    def update_borrower(self, borrower_id, name, email, phone, address):
        """Update borrower information"""
        # Check if new email conflicts with other borrowers
        check_query = """
        SELECT borrower_id FROM borrowers 
        WHERE email = %s AND borrower_id != %s
        """
        existing = self.db.execute_query(check_query, (email, borrower_id), fetch=True)
        
        if existing:
            return False, "Email already registered by another borrower"
        
        query = """
        UPDATE borrowers 
        SET name = %s, email = %s, phone = %s, address = %s
        WHERE borrower_id = %s
        """
        result = self.db.execute_query(query, (name, email, phone, address, borrower_id))
        return result is not None, "Borrower updated successfully" if result else "Failed to update borrower"
    
    def delete_borrower(self, borrower_id):
        """Delete a borrower from database"""
        # Check if borrower has active loans
        check_query = """
        SELECT COUNT(*) as active_loans 
        FROM transactions 
        WHERE borrower_id = %s AND status = 'borrowed'
        """
        result = self.db.execute_query(check_query, (borrower_id,), fetch=True)
        
        if result and result[0]['active_loans'] > 0:
            return False, f"Cannot delete! Borrower has {result[0]['active_loans']} active loan(s)."
        
        query = "DELETE FROM borrowers WHERE borrower_id = %s"
        result = self.db.execute_query(query, (borrower_id,))
        return result is not None, "Borrower deleted successfully" if result else "Failed to delete borrower"
    
    def get_borrower_statistics(self):
        """Get borrower statistics"""
        query = """
        SELECT 
            COUNT(*) as total_borrowers,
            COUNT(DISTINCT email) as unique_emails,
            (SELECT name FROM borrowers ORDER BY created_date DESC LIMIT 1) as newest_borrower,
            (SELECT COUNT(*) FROM transactions WHERE status = 'borrowed') as active_borrowers
        FROM borrowers
        """
        result = self.db.execute_query(query, fetch=True)
        return result[0] if result else {}
    
    # ========== TRANSACTION MANAGEMENT ==========
    
    def get_all_transactions(self):
        """Get all transactions from database"""
        query = """
        SELECT t.transaction_id, t.book_id, t.borrower_id,
               DATE(t.borrow_date) as borrow_date,
               DATE(t.due_date) as due_date,
               DATE(t.return_date) as return_date,
               t.status, t.fine_amount, t.created_at,
               b.title, b.author,
               br.name as borrower_name, br.email
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN borrowers br ON t.borrower_id = br.borrower_id
        ORDER BY t.created_at DESC
        """
        return self.db.execute_query(query, fetch=True) or []
    
    def get_transaction_by_id(self, transaction_id):
        """Get transaction details by ID"""
        query = """
        SELECT t.*, b.title, b.author, br.name as borrower_name, br.email
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN borrowers br ON t.borrower_id = br.borrower_id
        WHERE t.transaction_id = %s
        """
        result = self.db.execute_query(query, (transaction_id,), fetch=True)
        return result[0] if result else None
    
    def borrow_book(self, book_id, borrower_id, borrow_date=None, due_date=None):
        """Borrow a book"""
        # Check if book is available
        book = self.get_book_by_id(book_id)
        if not book or book['available_copies'] <= 0:
            return None, "Book not available for borrowing"
        
        # Check if borrower exists
        borrower = self.get_borrower_by_id(borrower_id)
        if not borrower:
            return None, "Borrower not found"
        
        # Check if borrower has overdue books
        overdue_check = """
        SELECT COUNT(*) as overdue_count 
        FROM transactions 
        WHERE borrower_id = %s AND status = 'borrowed' AND due_date < CURDATE()
        """
        overdue_result = self.db.execute_query(overdue_check, (borrower_id,), fetch=True)
        
        if overdue_result and overdue_result[0]['overdue_count'] > 0:
            return None, f"Borrower has {overdue_result[0]['overdue_count']} overdue book(s)"
        
        # Set dates
        if not borrow_date:
            borrow_date = datetime.now().date()
        
        if not due_date:
            due_date = borrow_date + timedelta(days=14)
        
        # Insert transaction
        query = """
        INSERT INTO transactions (book_id, borrower_id, borrow_date, due_date, status)
        VALUES (%s, %s, %s, %s, 'borrowed')
        """
        transaction_id = self.db.execute_query(query, (book_id, borrower_id, borrow_date, due_date))
        
        if transaction_id:
            return transaction_id, "Book borrowed successfully"
        
        return None, "Failed to borrow book"
    
    def return_book(self, transaction_id, return_date=None):
        """Return a borrowed book"""
        transaction = self.get_transaction_by_id(transaction_id)
        if not transaction:
            return False, "Transaction not found"
        
        if transaction['status'] == 'returned':
            return False, "Book already returned"
        
        if not return_date:
            return_date = datetime.now().date()
        
        # Calculate fine if overdue
        fine_amount = 0
        due_date = transaction['due_date']
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        
        if return_date > due_date:
            days_overdue = (return_date - due_date).days
            fine_amount = days_overdue * 5.00  # $5 per day fine
        
        # Update transaction
        query = """
        UPDATE transactions 
        SET return_date = %s, status = 'returned', fine_amount = %s
        WHERE transaction_id = %s
        """
        result = self.db.execute_query(query, (return_date, fine_amount, transaction_id))
        
        if result is not None:
            return True, f"Book returned successfully. Fine: ${fine_amount:.2f}"
        
        return False, "Failed to return book"
    
    def get_active_loans(self):
        """Get all active loans"""
        query = """
        SELECT t.transaction_id, t.borrow_date, t.due_date,
               b.title, b.author, b.isbn,
               br.name as borrower_name, br.email, br.phone,
               DATEDIFF(CURRENT_DATE, t.due_date) as days_overdue,
               CASE 
                   WHEN DATEDIFF(CURRENT_DATE, t.due_date) > 0 THEN 'Overdue'
                   ELSE 'On Time'
               END as status_label
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN borrowers br ON t.borrower_id = br.borrower_id
        WHERE t.status = 'borrowed'
        ORDER BY t.due_date
        """
        return self.db.execute_query(query, fetch=True) or []
    
    def get_overdue_books(self):
        """Get all overdue books"""
        query = """
        SELECT t.*, b.title, b.author, br.name as borrower_name, br.email,
               DATEDIFF(CURDATE(), t.due_date) as days_overdue
        FROM transactions t
        JOIN books b ON t.book_id = b.book_id
        JOIN borrowers br ON t.borrower_id = br.borrower_id
        WHERE t.status = 'borrowed' AND t.due_date < CURDATE()
        ORDER BY t.due_date ASC
        """
        return self.db.execute_query(query, fetch=True) or []
    
    def update_overdue_status(self):
        """Update status of overdue books"""
        query = """
        UPDATE transactions 
        SET status = 'overdue' 
        WHERE status = 'borrowed' AND due_date < CURDATE()
        """
        return self.db.execute_query(query)
    
    def get_transaction_statistics(self):
        """Get transaction statistics"""
        query = """
        SELECT 
            COUNT(*) as total_transactions,
            COUNT(CASE WHEN status = 'borrowed' THEN 1 END) as active_loans,
            COUNT(CASE WHEN status = 'returned' THEN 1 END) as returned_books,
            COUNT(CASE WHEN status = 'overdue' THEN 1 END) as overdue_books,
            SUM(fine_amount) as total_fines,
            AVG(DATEDIFF(return_date, borrow_date)) as avg_loan_duration
        FROM transactions
        """
        result = self.db.execute_query(query, fetch=True)
        return result[0] if result else {}
    
    # ========== REPORTS ==========
    
    def get_monthly_report(self, year=None, month=None):
        """Get monthly transaction report"""
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month
        
        query = """
        SELECT 
            DAY(borrow_date) as day,
            COUNT(*) as transactions,
            COUNT(CASE WHEN status = 'borrowed' THEN 1 END) as borrowed,
            COUNT(CASE WHEN status = 'returned' THEN 1 END) as returned,
            SUM(fine_amount) as daily_fines
        FROM transactions
        WHERE YEAR(borrow_date) = %s AND MONTH(borrow_date) = %s
        GROUP BY DAY(borrow_date)
        ORDER BY day
        """
        return self.db.execute_query(query, (year, month), fetch=True) or []
    
    def get_category_report(self):
        """Get report by book category"""
        query = """
        SELECT 
            b.category,
            COUNT(*) as total_books,
            SUM(b.copies) as total_copies,
            SUM(b.available_copies) as available_copies,
            COUNT(t.transaction_id) as times_borrowed
        FROM books b
        LEFT JOIN transactions t ON b.book_id = t.book_id
        GROUP BY b.category
        ORDER BY times_borrowed DESC
        """
        return self.db.execute_query(query, fetch=True) or []
    
    def get_borrower_activity_report(self, limit=10):
        """Get most active borrowers"""
        query = """
        SELECT 
            br.borrower_id,
            br.name,
            br.email,
            COUNT(t.transaction_id) as total_borrowed,
            COUNT(CASE WHEN t.status = 'borrowed' THEN 1 END) as currently_borrowed,
            SUM(t.fine_amount) as total_fines_paid,
            MAX(t.borrow_date) as last_borrowed
        FROM borrowers br
        LEFT JOIN transactions t ON br.borrower_id = t.borrower_id
        GROUP BY br.borrower_id, br.name, br.email
        ORDER BY total_borrowed DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,), fetch=True) or []
    
    def get_popular_books_report(self, limit=10):
        """Get most popular books"""
        query = """
        SELECT 
            b.book_id,
            b.title,
            b.author,
            b.category,
            COUNT(t.transaction_id) as times_borrowed,
            b.available_copies
        FROM books b
        LEFT JOIN transactions t ON b.book_id = t.book_id
        GROUP BY b.book_id, b.title, b.author, b.category, b.available_copies
        ORDER BY times_borrowed DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,), fetch=True) or []
    
    # ========== SYSTEM STATISTICS ==========
    
    def get_system_statistics(self):
        """Get comprehensive system statistics"""
        stats = {}
        
        # Book statistics
        book_stats = self.get_book_statistics()
        stats.update(book_stats)
        
        # Borrower statistics
        borrower_stats = self.get_borrower_statistics()
        stats.update(borrower_stats)
        
        # Transaction statistics
        transaction_stats = self.get_transaction_statistics()
        stats.update(transaction_stats)
        
        # Additional stats
        stats['current_date'] = datetime.now().strftime('%Y-%m-%d')
        stats['overdue_count'] = len(self.get_overdue_books())
        
        return stats
    
    def execute_custom_query(self, query):
        """Execute custom SQL query (SELECT only for safety)"""
        if not query.strip().upper().startswith('SELECT'):
            return None, "Only SELECT queries are allowed"
        
        try:
            result = self.db.execute_query(query, fetch=True)
            return result, "Query executed successfully"
        except Exception as e:
            return None, f"Query error: {str(e)}"
    
    def get_available_books(self):
        """Get all available books for borrowing"""
        query = """
        SELECT book_id, title, author, available_copies 
        FROM books 
        WHERE available_copies > 0 
        ORDER BY title
        """
        return self.db.execute_query(query, fetch=True) or []
    
    def get_categories(self):
        """Get unique book categories"""
        query = "SELECT DISTINCT category FROM books ORDER BY category"
        result = self.db.execute_query(query, fetch=True)
        return [row['category'] for row in result] if result else []