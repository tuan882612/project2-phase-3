import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear
from controllers.loan_late import formated_book_infos, formated_fees

def load_fee(frame: ct.CTkFrame, data: list[tuple]) -> None:
    clear(frame)
    
    if not data:
        ct.CTkLabel(
            master=frame,
            text="No Results Found",
            font=("Calibri", 16)
        ).pack(anchor=tk.N)
        return
    
    for i in data:
        label = ct.CTkLabel(
            master=frame,
            text=f'card number: {i[0]}\n name: {i[1]}\n latefee: {i[2]}\n',
            font=("Calibri", 13))
        label.pack(anchor=tk.N)

def load_book(frame: ct.CTkFrame, data: list[tuple]) -> None:
    clear(frame)
    
    if not data:
        ct.CTkLabel(
            master=frame,
            text="No Results Found",
            font=("Calibri", 16)
        ).pack(anchor=tk.N)
        return
    
    for i in data:
        label = ct.CTkLabel(
            master=frame,
            text=f'book id: {i[0]} title: {i[1]}\n date due: {i[2]}\n latefee: {i[3]}\n',
            font=("Calibri", 13))
        label.pack(anchor=tk.N)
            

def load_tables(app: ct.CTk) -> None:
    frame = ct.CTkFrame(master=app)
    frame.place(relx=0.25, rely=0.15, relwidth=0.725, relheight=0.8)
    
    header_frame = ct.CTkFrame(master=frame)
    header_frame.grid(row=0, column=0, columnspan=2)
    borrower_label = ct.CTkLabel(
        master=header_frame,
        text="Late Fee Balance",
        font=("Calibri", 15))
    borrower_label.pack(side=tk.LEFT, padx=(133, 133))
    book_label = ct.CTkLabel(
        master=header_frame,
        text="Book Info",
        font=("Calibri", 15))
    book_label.pack(side=tk.LEFT, padx=(133, 133))
    
    borrower_entry = ct.CTkEntry(
        master=frame,
        placeholder_text="Search Card Number or Name", 
        width=200)
    borrower_entry.grid(row=1, column=0, padx=(20, 20), pady=(20, 20), sticky='n')
    book_entry = ct.CTkEntry(
        master=frame,
        placeholder_text="Search Book ID or Title", 
        width=200)
    book_entry.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky='n')

    borrower = ct.CTkScrollableFrame(
        master=frame,
        height=300,
        width=300)
    borrower.grid(row=2, column=0, padx=(20, 20), sticky='n')
    book = ct.CTkScrollableFrame(
        master=frame,
        height=300,
        width=300)
    book.grid(row=2, column=1, padx=(20, 20), sticky='n')
    
    borrower_submit = ct.CTkButton(
        master=frame,
        text="Search",
        command=lambda: load_fee(borrower, formated_fees(borrower_entry.get())))
    borrower_submit.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky='n')
    book_submit = ct.CTkButton(
        master=frame,
        text="Search",
        command=lambda: load_book(book, formated_book_infos(book_entry.get())))
    book_submit.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky='n')
    
    load_fee(borrower, formated_fees())
    load_book(book, formated_book_infos())
 
def loan_late_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="List the Loans and Late Fees", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(190, 0))
    load_tables(app)
