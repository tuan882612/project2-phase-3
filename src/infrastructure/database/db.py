import sqlite3

def get_all():
    with sqlite3.connect('./src/infrastructure/database/library-ms.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM book')
        return cursor.fetchall()
    
def get_by_title(title: str):
    with sqlite3.connect('./src/infrastructure/database/library-ms.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM book WHERE title = ?', (title,))
        return cursor.fetchall()

def get_copies_branch(title: str):
    with sqlite3.connect('./src/infrastructure/database/library-ms.db') as conn:
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