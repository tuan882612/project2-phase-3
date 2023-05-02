import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear
from controllers.new_book import insert_new_book

def proccess_inputs(frame: ct.CTkFrame, entries: tuple[ct.CTkEntry]) -> None:
    missing = [label for label, input in entries if not input.get()]
    
    for child in frame.winfo_children():
        if isinstance(child, ct.CTkLabel) and\
            getattr(child, 'is_error', False) or\
            getattr(child, 'is_success', False):
            child.destroy()

    if missing:
        display = ', '.join(missing) if len(missing) < 4 else str(len(missing))+ " fields"
        frame.error = ct.CTkLabel(
            master=frame, 
            text=f"Missing {display}",
            font=("Calibri", 14))
        frame.error.is_error = True
        frame.error.pack()
        return
    else:
        data = (input.get() for _, input in entries)
        insert_new_book(data)
        frame.success = ct.CTkLabel(
            master=frame, 
            text=f"Book successfully added",
            font=("Calibri", 14))
        frame.success.is_success = True
        frame.success.pack()
        
        for _, input in entries:
            input.delete(0, tk.END)

def load_form(app: ct.CTk) -> None:
    frame = ct.CTkFrame(master=app)
    frame.place(relx=0.45, rely=0.175, relwidth=0.3, relheight=0.7)
    
    inputs = []
    fields = ["title", "author", "publisher", "phone", "address"]
    
    for i, entry in enumerate(fields):
        input_header = ct.CTkLabel(
            master=frame, 
            text=entry,
            font=("Calibri", 14))
        input_header.pack(pady=(15 if i == 0 else 0, 0))
        input = ct.CTkEntry(master=frame, placeholder_text=f"Enter {entry}")
        input.pack()
        inputs.append((entry, input))
        
    ct.CTkButton(
        master=frame, 
        text="Submit",
        command=lambda: proccess_inputs(frame, inputs)
    ).pack(pady=20)

def entry_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Enter an a new Book", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(190, 0))
    load_form(app)