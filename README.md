# Library Management System
A comprehensive desktop application for managing library operations, built with Python, Tkinter, and MariaDB.

## 📋 Project Overview
This Library Management System is designed to automate and streamline library operations including book management, borrower tracking, transaction handling, and report generation. The system features a modern user interface with authentication and role-based access control.

### 🎯 Project Objectives
- Demonstrate understanding of database concepts and relational database design
- Apply SQL knowledge and implement CRUD operations effectively
- Develop a functional system with a user-friendly graphical interface
- Integrate system analysis, design, and problem-solving skills into a complete application

### 📊 Project Scope
The system covers the following functional areas:
- **Book Management**: Add, edit, delete, search, and track book inventory
- **Borrower Management**: Register, update, and manage library members
- **Transaction Management**: Handle book borrowing, returning, and fine calculations
- **Reporting & Analytics**: Generate insights on library operations and popular items
- **User Authentication**: Secure login system with role-based permissions

## 🛠️ Technology Stack
- **Backend**: Python 3.x
- **Database**: MariaDB (MySQL compatible)
- **GUI Framework**: Tkinter
- **Database Connector**: mariadb Python package
- **Visualization**: matplotlib (for reporting charts)

## Project Structure
```
📂 LibraryManagementSystem/
├── 📂 backend/
│   ├── library_backend.py
│   └── auth.py
|
├── 📂 components/
│   └── widgets.py
|
├── 📂 database/
│   ├── db_connection.py
│   ├── create_tables.sql
│   └── sample_data.sql
|
├── 📂 pages/
│   ├── login_page.py
│   ├── signup_page.py
│   ├── dashboard_page.py
│   ├── books_page.py
│   ├── borrowers_page.py
│   ├── transactions_page.py
│   └── reports_page.py 
|
├── 📂 utils/
│ └── helpers.py
|
├── main.py
├── create_admin.py
├── requirements.txt
└── README.md
```


### Database Normalization
The database design follows **Third Normal Form (3NF)**:
- **First Normal Form (1NF)**: All tables have atomic values, no repeating groups
- **Second Normal Form (2NF)**: All non-key attributes fully dependent on primary keys
- **Third Normal Form (3NF)**: No transitive dependencies between non-key attributes

### Table Structures
1. **users** - User authentication and roles
2. **borrowers** - Library member information (linked to users)
3. **books** - Book catalog with availability tracking
4. **transactions** - Loan records with status and fines

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- MariaDB Server
- Git (optional)

### Step 1: Database Setup
```
# Login to MariaDB
mysql -u root -p

# Create database and user
CREATE DATABASE LibraryManagement_DB;
USE LibraryManagement_DB;

# Run the create_tables.sql script
SOURCE /path/to/create_tables.sql;

# Optional: Load sample data
SOURCE /path/to/sample_data.sql;

## Python Environment
# Clone the repository (if using Git)
git clone <repository-url>
cd LibraryManagementSystem

# Install dependencies
pip install -r requirements.txt

## Configuration
Update database credentials in database/db_connection.py if needed:

python
self.host = "localhost"
self.user = "root"
self.password = "your_password"
self.database = "LibraryManagement_DB"

# Create Admin User
python create_admin.py

Default admin credentials:
Username: admin
Password: Admin@123
Email: admin@library.com

##💻 Run App:
python main.py
```

### User Roles & Permissions:
- Admin: Full system access, user management
- Librarian: Book and borrower management, transaction processing
- Borrower: View available books, personal borrowing history

# Key Features:
### 📖 Book Management:
- Add new books with title, author, ISBN, category
- Update book information and copies
- Search books by title, author, category, or ISBN
- Delete books (with validation for active loans)

### 👥 Borrower Management:
- Register new library members
- Update borrower information
- Track active loans and borrowing history
- Search borrowers by name, email, or phone

### 🔄 Transaction Processing
-Borrow books with automatic due date calculation
-Return books with fine calculation ($5/day overdue)
-View active loans and overdue books
-Process payments for fines

### 📊 Reports & Analytics
- System statistics dashboard
- Monthly transaction reports
- Popular books and active borrowers
- Category-based analysis
- Custom date range reports

## 🔧 CRUD Operations Implementation:
###Create Operations:
- add_book() - Add new books to inventory
- add_borrower() - Register new library members
- borrow_book() - Create new loan transactions
- register_user() - Create new system users

### Read Operations
- get_all_books() - Retrieve all books
- search_books() - Search with various criteria
- get_active_loans() - View current borrowings
- get_system_statistics() - Dashboard data

### Update Operations
- update_book() - Modify book information
- update_borrower() - Update member details
- return_book() - Update transaction status
- update_profile() - User profile updates

### Delete Operations
- delete_book() - Remove books (with validation)
- delete_borrower() - Remove members (with validation)

# 👨‍💻 Developer
- Jon Paul S. Berana
- CS 2102 - IT 211 - Database Management System
- First Semester, A.Y. 2025-2026

# 📄 License
This project is developed for educational purposes as part of IT 211 - Database Management System course requirements.
