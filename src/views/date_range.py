import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear
from infrastructure.database.db import get_date_range

def display_late_book_loans(frame: ct.CTkScrollableFrame, data: list[tuple]) -> None:
    clear(frame)
    frame._parent_canvas.yview_moveto(0)

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
            text=f'Book ID: {i[0]}\nTitle: {i[1]}\nDate Out: {i[2]}\nDue Date: {i[3]}\nReturned Date: {i[4]}\nDays Late: {i[5]:.2f}\n',
            font=("Calibri", 13))
        label.pack(anchor=tk.N)


def date_range_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Enter a Date Range", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(190, 0))
    
    start_date_entry = ct.CTkEntry(
        master=app,
        placeholder_text="Start Date (YYYY-MM-DD)", 
        width=200)
    start_date_entry.pack(padx=(220, 20), anchor=tk.N)
    end_date_entry = ct.CTkEntry(
        master=app,
        placeholder_text="End Date (YYYY-MM-DD)", 
        width=200)
    end_date_entry.pack(padx=(220, 20), anchor=tk.N)

    result_frame = ct.CTkScrollableFrame(master=app)
    result_frame.place(relx=0.35, rely=0.3, relwidth=0.5, relheight=0.4)

    submit_button = ct.CTkButton(
        master=app,
        text="Submit",
        command=lambda: display_late_book_loans(result_frame, get_date_range(start_date_entry.get(), end_date_entry.get())))
    submit_button.place(relx=0.55, rely=0.75, relwidth=0.1, relheight=0.05)
