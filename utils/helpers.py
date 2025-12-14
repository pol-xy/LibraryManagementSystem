from datetime import datetime, timedelta
import re

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (basic validation)"""
    if not phone:
        return True  # Phone is optional
    pattern = r'^[\d\s\-\+\(\)]{7,20}$'
    return re.match(pattern, phone) is not None

def format_date(date_obj):
    """Format date object to string"""
    if date_obj:
        if isinstance(date_obj, str):
            return date_obj
        try:
            return date_obj.strftime('%Y-%m-%d')
        except:
            return str(date_obj)
    return ""

def get_current_date():
    """Get current date as string"""
    return datetime.now().strftime('%Y-%m-%d')

def calculate_due_date(borrow_date, days=14):
    """Calculate due date"""
    if isinstance(borrow_date, str):
        borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d')
    due_date = borrow_date + timedelta(days=days)
    return due_date.strftime('%Y-%m-%d')

def calculate_fine(due_date, return_date):
    """Calculate fine amount"""
    if not due_date or not return_date:
        return 0.00
    
    try:
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        if isinstance(return_date, str):
            return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        
        if return_date > due_date:
            days_overdue = (return_date - due_date).days
            return max(0, days_overdue * 5.00)  # $5 per day fine
    except:
        pass
    return 0.00

def validate_book_data(title, author, copies):
    """Validate book data"""
    errors = []
    if not title or len(title.strip()) < 2:
        errors.append("Title must be at least 2 characters")
    if not author or len(author.strip()) < 2:
        errors.append("Author must be at least 2 characters")
    if not copies or int(copies) < 1:
        errors.append("Copies must be at least 1")
    return errors

def validate_borrower_data(name, email):
    """Validate borrower data"""
    errors = []
    if not name or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters")
    if not validate_email(email):
        errors.append("Valid email is required")
    return errors