import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear

def loan_late_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="List the Loans and Late Fees", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(170, 0))