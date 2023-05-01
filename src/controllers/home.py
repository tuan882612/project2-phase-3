from infrastructure.database.db import get_all, get_by_title, get_copies_branch

def search_books(title: str) -> list[tuple]:
    if not title.strip():
        return get_all()
    data: list[str] = get_by_title(title)
    print(data)
    return [] if not data else data
    
def search_num_copies(title: str) -> list[tuple]:
    if not title.strip():
        return get_all()
    data: list[str] = get_copies_branch(title)
    print(data)
    return [] if not data else data
