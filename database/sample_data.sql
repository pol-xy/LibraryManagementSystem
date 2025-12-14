USE LibraryManagement_DB;

-- Insert sample books
INSERT INTO books (title, author, isbn, category, year, copies, available_copies) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'Fiction', 1925, 3, 3),
('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'Fiction', 1960, 2, 2),
('1984', 'George Orwell', '9780451524935', 'Science Fiction', 1949, 4, 4),
('Pride and Prejudice', 'Jane Austen', '9780141439518', 'Romance', 1813, 3, 3),
('The Hobbit', 'J.R.R. Tolkien', '9780547928227', 'Fantasy', 1937, 2, 2),
('The Catcher in the Rye', 'J.D. Salinger', '9780316769488', 'Fiction', 1951, 3, 3),
('Brave New World', 'Aldous Huxley', '9780060850524', 'Science Fiction', 1932, 2, 2),
('The Lord of the Rings', 'J.R.R. Tolkien', '9780618640157', 'Fantasy', 1954, 1, 1),
('Harry Potter and the Sorcerer''s Stone', 'J.K. Rowling', '9780590353427', 'Fantasy', 1997, 5, 5),
('The Da Vinci Code', 'Dan Brown', '9780307474278', 'Mystery', 2003, 4, 4);

-- Insert sample borrowers
INSERT INTO borrowers (name, email, phone, address) VALUES
('John Smith', 'john.smith@email.com', '555-0101', '123 Main St, Cityville'),
('Emma Johnson', 'emma.j@email.com', '555-0102', '456 Oak Ave, Townsville'),
('Michael Brown', 'michael.b@email.com', '555-0103', '789 Pine Rd, Villagetown'),
('Sarah Davis', 'sarah.d@email.com', '555-0104', '321 Elm St, Hamletcity'),
('David Wilson', 'david.w@email.com', '555-0105', '654 Maple Dr, Boroughburg'),
('Lisa Miller', 'lisa.m@email.com', '555-0106', '987 Birch Ln, Countyville'),
('James Taylor', 'james.t@email.com', '555-0107', '147 Cedar Way, Districtown'),
('Maria Garcia', 'maria.g@email.com', '555-0108', '258 Spruce Ct, Parishville'),
('Robert Martinez', 'robert.m@email.com', '555-0109', '369 Willow Path, Cantonburg'),
('Jennifer Lee', 'jennifer.l@email.com', '555-0110', '741 Aspen Blvd, Township');

-- Insert sample transactions
INSERT INTO transactions (book_id, borrower_id, borrow_date, due_date, return_date, status) VALUES
(1, 1, '2024-01-15', '2024-02-15', '2024-02-10', 'returned'),
(2, 2, '2024-01-20', '2024-02-20', '2024-02-18', 'returned'),
(3, 3, '2024-02-01', '2024-03-01', NULL, 'borrowed'),
(4, 4, '2024-02-05', '2024-03-05', '2024-03-10', 'returned'),
(5, 5, '2024-02-10', '2024-03-10', NULL, 'borrowed'),
(1, 6, '2024-02-12', '2024-03-12', '2024-03-05', 'returned'),
(6, 7, '2024-02-15', '2024-03-15', NULL, 'borrowed'),
(7, 8, '2024-02-18', '2024-03-18', NULL, 'borrowed'),
(8, 9, '2024-02-20', '2024-03-20', '2024-03-25', 'returned'),
(9, 10, '2024-02-22', '2024-03-22', NULL, 'borrowed');