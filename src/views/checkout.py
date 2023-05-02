import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear, clear_message
from infrastructure.database.db import (
    get_all_copies,
    get_copies_by_title,
    get_copies_info_by_title,
    create_book_loan
)

def update_branch(frame: ct.CTkFrame, title: str) -> None:
    branchs = get_copies_info_by_title(title)
    branch_labels = []
    for child in frame.winfo_children(): 
        if getattr(child, 'is_branch_label', False):
            branch_labels.append(child)
            
    for branch, label in zip(branchs, branch_labels):
        copy_text = 'copy' if branch[1] == 1 else 'copies'
        label.configure(text=f"{branch[0]} \t {branch[1]} {copy_text}")

def checkout_book(frame: ct.CTkFrame, card_no: str, branch: str, title: str) -> None:
    clear_message(frame)

    if card_no.get() == '':
        frame.error = ct.CTkLabel(
            master=frame,
            text=f"Missing card number field",
            font=("Calibri", 14))
        frame.error.is_error = True
        frame.error.pack(side=tk.BOTTOM, pady=(0, 30))
    else:
        create_book_loan(title, branch, card_no.get())
        frame.success = ct.CTkLabel(
            master=frame,
            text=f"Successfully checked out book",
            font=("Calibri", 14))
        frame.success.is_success = True
        frame.success.pack(side=tk.BOTTOM, pady=(0, 30))
        update_branch(frame, title)
        card_no.delete(0, tk.END)

def load_info_confirmation(app: ct.CTk, title: str) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Confirm Checkout", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(190, 0))
    
    frame = ct.CTkFrame(master=app)
    frame.place(relx=0.35, rely=0.2, relwidth=0.5, relheight=0.7)
    
    table_header = ct.CTkLabel(
        master=frame,
        text=f"Book Copies for '{title}' Per Branch",
        font=("Calibri", 16))
    table_header.pack(anchor=tk.N, pady=(10, 10))
    
    branchs = get_copies_info_by_title(title)
    for branch in branchs:
        label = ct.CTkLabel(
            master=frame,
            text=f"{branch[0]} \t {branch[1]} {'copy' if branch[1] == 1 else 'copies'}",
            font=("Calibri", 16))
        label.is_branch_label = True
        label.pack(anchor=tk.W, padx=40, pady=(10, 5))
        
    bottom_frame = ct.CTkFrame(master=frame)
    bottom_frame.place(x=20, y=300)

    options = ct.CTkComboBox(
        master=bottom_frame,
        values=[branch[0] for branch in branchs if branch[1] > 0])
    options.pack(side=tk.LEFT, padx=(0, 10))

    cardno_entry = ct.CTkEntry(
        master=bottom_frame,
        placeholder_text="Enter Card Number")
    cardno_entry.pack(side=tk.LEFT, padx=(0, 10))

    submit = ct.CTkButton(
        master=bottom_frame,
        text="submit",
        command=lambda: checkout_book(frame, cardno_entry, options.get(), title))
    submit.pack(side=tk.LEFT)

def load_books(
    app: ct.CTk,
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
        button_info = f'"{book[1]}" by {book[2]}\ntotal copies: {book[3]}'
        ct.CTkButton(
            master=books, 
            text=button_info, 
            width=550, height=50,
            command=lambda x=book:load_info_confirmation(app, x[1])
        ).pack(pady=(len(results) if i == 0 else 0, len(results)))

def books_container(app: ct.CTk, books: ct.CTkScrollableFrame) -> None:    
    search_bar = ct.CTkEntry(master=app, placeholder_text="Search")
    search_bar.place(relx=0.3, rely=0.2, relwidth=0.35, relheight=0.07)
    
    search_button = ct.CTkButton(
        master=app, text="Search", 
        command=lambda: load_books(app, books, get_copies_by_title(search_bar.get())))
    search_button.place(relx=0.665, rely=0.2, relwidth=0.12, relheight=.07)
    
    reset_button = ct.CTkButton(
        master=app, text="Reset", 
        command=lambda:checkout_view(app))
    reset_button.place(relx=0.8, rely=0.2, relwidth=0.12, relheight=.07)

def checkout_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Checkout a Book", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(170, 0))
    
    books = ct.CTkScrollableFrame(master=app)
    books.place(relx=0.3, rely=0.3, relwidth=0.625, relheight=0.6)
    load_books(app, books, get_all_copies())
    books_container(app, books)