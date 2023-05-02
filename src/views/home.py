import tkinter as tk
import customtkinter as ct

from controllers.home import search_books, search_num_copies
from infrastructure.database.db import get_all
from infrastructure.utils.index import clear

def load_info(books: ct.CTkScrollableFrame, title: str) -> None:
    clear(books)
    books._parent_canvas.yview_moveto(0)

    header = ct.CTkLabel(
        master=books, 
        text=f"Book Copies Loaned Out Per Branch \n '{title}'", 
        font=("Calibri", 16), height=50)
    header.pack(anchor=tk.N)

    data: list[tuple] = search_num_copies(title)
    if len(data) < 3: 
        ct.CTkLabel(
            master=books, 
            text="No copies were loaned out", font=("Calibri", 16)
        ).pack(anchor=tk.NE, padx=(0, 190))
        return
        
    for branch_name, num_copies in data:
        ct.CTkLabel(
            master=books,
            text=f"{branch_name} \t {num_copies} {'copy' if num_copies == 1 else 'copies'}",
            font=("Calibri", 16)
        ).pack(anchor=tk.W, padx=20, pady=(0, 10))

def load_books(
    books: ct.CTkScrollableFrame, 
    results: list[tuple] | list, 
) -> None:
    clear(books)

    if not results:
        ct.CTkLabel(
            master=books, 
            text="No Results Found", 
            font=("Calibri", 20)
        ).pack(anchor=tk.NE, padx=(0, 190))
        return 
    
    for i, book in enumerate(results):
        ct.CTkButton(
            master=books, 
            text=f'{i}) "{book[1]}" by {book[2]}', 
            width=550, height=50,
            command=lambda x=book:load_info(books, x[1])
        ).pack(pady=(len(results) if i == 0 else 0, len(results)))


def books_container(app: ct.CTk, books: ct.CTkScrollableFrame) -> None:
    search_bar = ct.CTkEntry(master=app, placeholder_text="Search")
    search_bar.place(relx=0.3, rely=0.2, relwidth=0.35, relheight=0.07)
    
    search_button = ct.CTkButton(
        master=app, text="Search", 
        command=lambda:load_books(books, search_books(search_bar.get())))
    search_button.place(relx=0.665, rely=0.2, relwidth=0.12, relheight=.07)
    
    reset_button = ct.CTkButton(
        master=app, text="Reset", 
        command=lambda:home_view(app))
    reset_button.place(relx=0.8, rely=0.2, relwidth=0.12, relheight=.07)

def home_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Welcome To Library Management System, \n\
            Please Select or Search For a Book for more information.", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(170, 0))
    
    books = ct.CTkScrollableFrame(master=app)
    books.place(relx=0.3, rely=0.3, relwidth=0.625, relheight=0.6)
    
    load_books(books, get_all())
    books_container(app, books)
    