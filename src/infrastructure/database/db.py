import sqlite3

_db_path: str = './src/infrastructure/database/library-ms.db'

def get_all() -> list[tuple]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM book')
        return cursor.fetchall()
    
def get_all_copies() -> list[tuple]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT 
            b.book_id, 
            b.title, 
            b.book_publisher, 
            IFNULL(SUM(copy.no_of_copies), 0) AS count
        FROM book b
        LEFT JOIN book_copies copy 
               ON b.book_id = copy.book_id
        GROUP BY b.book_id;''')
        return cursor.fetchall()
    
def get_by_title(title: str):
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM book 
        WHERE title = ? ''', (title,))
        return cursor.fetchall()
    
def get_copies_by_title(title: str) -> list[str]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT 
            b.book_id, 
            b.title, 
            b.book_publisher, 
            IFNULL(SUM(copy.no_of_copies), 0) AS count
        FROM book b
        LEFT JOIN book_copies copy 
               ON b.book_id = copy.book_id
        WHERE b.title = ?
        GROUP BY b.book_id;''', (title,))
        return cursor.fetchall()

def get_copies_info_by_title(title: str) -> list[str]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT 
          branch.branch_name, 
          IFNULL(SUM(copy.no_of_copies), 0) AS count
        FROM library_branch branch
        LEFT JOIN book_copies copy 
               ON branch.branch_id = copy.branch_id
        LEFT JOIN book b 
               ON copy.book_id = b.book_id
        WHERE b.title = ? OR b.title IS NULL
        GROUP BY branch.branch_id;''', (title,))
        return cursor.fetchall()

def get_all_late_fees() -> list[tuple]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                br.card_no AS Card_No,
                br.name AS Borrower_Name,
                CASE 
                    WHEN bl.Late = 1 THEN lb.LateFee * (julianday(bl.Returned_date) - julianday(bl.date_out))
                    ELSE 0
                END AS LateFeeBalance
            FROM borrower br
            JOIN book_loans bl ON br.card_no = bl.card_no 
            JOIN library_branch lb ON bl.branch_id = lb.branch_id 
            JOIN book b ON bl.book_id = b.book_id 
            GROUP BY br.card_no
            ORDER BY LateFeeBalance DESC;
        """
        cursor.execute(query)
        return cursor.fetchall()

def get_borrowers_late_fees(search: str):
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        query = """
        SELECT 
            br.card_no AS Card_No,
            br.name AS Borrower_Name,
            CASE 
                WHEN bl.Late = 1 THEN lb.LateFee * (julianday(bl.Returned_date) - julianday(bl.date_out))
                ELSE 0
            END AS LateFeeBalance
        FROM borrower br
        JOIN book_loans bl ON br.card_no = bl.card_no 
        JOIN library_branch lb ON bl.branch_id = lb.branch_id 
        JOIN book b ON bl.book_id = b.book_id 
        WHERE br.card_no LIKE ? OR br.name LIKE ?
        GROUP BY br.card_no
        ORDER BY LateFeeBalance DESC;
        """
        cursor.execute(query, (f"%{search}%", f"%{search}%"))
        return cursor.fetchall()
    
def get_all_books_late_fees() -> list[tuple]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT
            b.book_id AS Book_ID,
            b.title AS Book_Title,
            bl.due_date AS Due_Date,
            CASE 
                WHEN bl.Late = 1 THEN lb.LateFee * (julianday(bl.Returned_date) - julianday(bl.date_out))
                ELSE 'Non-Applicable'
            END AS LateFee
        FROM book_loans bl
        JOIN book b ON bl.book_id = b.book_id
        JOIN library_branch lb ON bl.branch_id = lb.branch_id
        ORDER BY LateFee DESC;''')
        return cursor.fetchall()

def get_books_late_fees(search: str):
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        query = """
        SELECT
            b.book_id AS Book_ID,
            b.title AS Book_Title,
            bl.due_date AS Due_Date,
            CASE 
                WHEN bl.Late = 1 THEN lb.LateFee * (julianday(bl.Returned_date) - julianday(bl.date_out))
                ELSE 'Non-Applicable'
            END AS LateFee
        FROM book_loans bl
        JOIN book b ON bl.book_id = b.book_id
        JOIN library_branch lb ON bl.branch_id = lb.branch_id
        WHERE b.book_id LIKE ? OR b.title LIKE ?
        ORDER BY LateFee DESC;
        """
        cursor.execute(query, (f"%{search}%", f"%{search}%"))
        return cursor.fetchall()
    
def get_date_range(date1: str, date2: str) -> list[tuple]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT
            b.book_id AS Book_ID,
            b.title AS Book_Title,
            bl.date_out AS Date_Out,
            bl.due_date AS Due_Date,
            bl.returned_date AS Returned_Date,
            julianday(bl.returned_date) - julianday(bl.due_date) AS Days_Late
        FROM book_loans bl
        JOIN book b ON bl.book_id = b.book_id
        WHERE bl.due_date BETWEEN ? AND ?
            AND bl.returned_date > bl.due_date
        ORDER BY Days_Late DESC;''', (date1, date2))
        return cursor.fetchall()

def get_lib_branches() -> list[tuple]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM library_branch')
        return cursor.fetchall()

def get_copies_branch(title: str) -> list[tuple]:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT 
          branch.branch_name, 
          IFNULL(SUM(copy.no_of_copies), 0) AS count
        FROM library_branch branch
        LEFT JOIN book_copies copy 
               ON branch.branch_id = copy.branch_id
        LEFT JOIN book b 
               ON copy.book_id = b.book_id
        WHERE b.title = ? OR b.title IS NULL
        GROUP BY branch.branch_id;''', (title,))
        return cursor.fetchall()
    
def create_book_loan(title: str, branch: str, card_no: int) -> None:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        
        book_id = cursor.execute('''
        SELECT book_id FROM book 
        WHERE title = ?''', (title,)).fetchone()[0]
        
        branch_id = cursor.execute('''
        SELECT branch_id FROM library_branch 
        WHERE branch_name = ?''', (branch,)).fetchone()[0]

        cursor.execute('''
        INSERT INTO book_loans (book_id, branch_id, card_no, date_out, due_date)
        VALUES (?, ?, ?, date('now'), date('now', '+7 days'));
        ''', (book_id, branch_id, card_no))
        cursor.execute('''
        UPDATE book_copies
        SET no_of_copies = no_of_copies - 1
        WHERE book_id = ? AND branch_id = ?;
        ''', (book_id, branch_id))
    
def create_borrower(name: str, address: str, phone: str) -> int:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO borrower (name, address, phone)
        VALUES (?, ?, ?);
        ''', (name, address, phone))
        borrower_id = cursor.lastrowid
        return borrower_id
    
def create_book(title: str, publisher: str) -> int:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO book (title, book_publisher)
        VALUES (?, ?);
        ''', (title, publisher))
        book_id = cursor.lastrowid
        return book_id

def create_author(book_id: int, title: str) -> None:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO book_authors (book_id, author_name)
        VALUES (?, ?);
        ''', (book_id, title))
        
def create_publisher(name: str, phone: str, address: str) -> None:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO publisher (publisher_name, phone, address)
        VALUES (?, ?, ?);
        ''', (name, phone, address))
        
def create_book_copy(book_id: int, branch_id: int, copies: int) -> None:
    with sqlite3.connect(_db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO book_copies (book_id, branch_id, no_of_copies)
        VALUES (?, ?, ?);
        ''', (book_id, branch_id, copies))