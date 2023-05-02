import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear

def date_range_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Enter a Date Range", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(190, 0))
