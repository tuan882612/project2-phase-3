
from infrastructure.database.db import (
    get_all_late_fees, 
    get_all_books_late_fees,
    get_books_late_fees,
    get_borrowers_late_fees
)

def formated_book_infos(search: str = None) -> list[tuple]:
    if not search:
        data = get_all_books_late_fees()
        data = [
            (i[0], 
            i[1], 
            i[2].split()[0], 
            round(i[3], 3) if isinstance(i[3], float) else i[3]) 
            for i in data
        ]
        num = [i for i in data if type(i[3]) == float]
        none = [i for i in data if type(i[3]) != float]
        return sorted(num, key=lambda x: x[3], reverse=True) + none
    return get_books_late_fees(search)

    
def formated_fees(search: str = None) -> list[tuple]:
    if not search:
        return [i for i in get_all_late_fees() if i[2] > 0]
    return get_borrowers_late_fees(search)