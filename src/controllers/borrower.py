from infrastructure.database.db import create_borrower

def insert_new_borrower(row: tuple[str]) -> int:
    name, address, phone = row
    return create_borrower(name, address, phone)