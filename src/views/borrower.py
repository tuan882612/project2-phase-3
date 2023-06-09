import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear, clear_message
from controllers.borrower import insert_new_borrower

def proccess_input(frame: ct.CTkFrame, entries: tuple[ct.CTkEntry]) -> None:
    missing = [label for label, input in entries if not input.get()]
    clear_message(frame)

    if missing:
        frame.error = ct.CTkLabel(
            master=frame, 
            text=f"Missing {', '.join(missing)}",
            font=("Calibri", 14))
        frame.error.is_error = True
        frame.error.pack()
        return
    else:
        data = (input.get() for _, input in entries)
        borrower_id = insert_new_borrower(data)
        frame.success = ct.CTkLabel(
            master=frame, 
            text=f"Borrower successfully added\ncard_no: {borrower_id}",
            font=("Calibri", 14))
        frame.success.is_success = True
        frame.success.pack()
        
        for _, input in entries:
            input.delete(0, tk.END)

def load_form(app: ct.CTk) -> None:
    frame = ct.CTkFrame(master=app)
    frame.place(relx=0.45, rely=0.2, relwidth=0.3, relheight=0.6)
    
    capture = []
    for i, entry in enumerate(["name", "address", "phone"]):
        input_header = ct.CTkLabel(
            master=frame, 
            text=entry,
            font=("Calibri", 14))
        input_header.pack(pady=(30 if i == 0 else 0, 0))
        input = ct.CTkEntry(master=frame, placeholder_text=f"Enter {entry}")
        input.pack()
        capture.append((entry, input))
        
    ct.CTkButton(
        master=frame, 
        text="Submit",
        command=lambda: proccess_input(frame, capture)
    ).pack(pady=30)

def borrower_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Enter New Borrower", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(190, 0))
    load_form(app)