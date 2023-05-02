
from infrastructure.database.db import (
    create_author, 
    create_book, 
    create_publisher,
    create_book_copy,
    get_lib_branches
)


def insert_new_book(row: tuple[str]) -> int:
    title, author, publisher, phone, address = row
    
    create_publisher(publisher, phone, address)
    book_id = create_book(title, publisher)
    create_author(book_id, author)
    
    branches = get_lib_branches()
    for bId, _, _ in branches:
        create_book_copy(book_id, bId, 5)