import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear

def proccess_input(frame: ct.CTkFrame, entries: list[ct.CTkEntry]) -> None:
    missing = [label for label, input in entries if not input.get()]
    
    for child in frame.winfo_children():
        if isinstance(child, ct.CTkLabel) and\
            getattr(child, 'is_error', False) or\
            getattr(child, 'is_success', False):
            child.destroy()

    if missing:
        frame.error = ct.CTkLabel(master=frame, text=f"Missing {', '.join(missing)}")
        frame.error.is_error = True
        frame.error.pack()
        return
    else:
        frame.success = ct.CTkLabel(master=frame, text="Borrower successfully added")
        frame.success.is_success = True
        frame.success.pack()
        
        for label, input in entries:
            input.delete(0, tk.END)

def load_form(app: ct.CTk) -> None:
    frame = ct.CTkFrame(master=app)
    frame.place(relx=0.45, rely=0.2, relwidth=0.3, relheight=0.7)
    
    entries = ["name", "address", "phone"]
    capture = []
    
    for i, val in enumerate(entries):
        input_header = ct.CTkLabel(master=frame, text=val)
        input_header.pack(pady=(50 if i == 0 else 0, 0))
        input = ct.CTkEntry(master=frame, placeholder_text=f"Enter {val}")
        input.pack()
        capture.append((val, input))
        
    ct.CTkButton(
        master=frame, 
        text="Submit",
        command=lambda: proccess_input(frame, capture)
    ).pack(pady=50)

def borrower_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Enter New Borrower", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(190, 0))
    load_form(app)