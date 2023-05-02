import customtkinter as ct
import tkinter as tk

from infrastructure.utils.index import clear

def checkout_view(app: ct.CTk) -> None:
    clear(app)
    header = ct.CTkLabel(
        master=app, 
        text="Checkout a Book", 
        font=("Calibri", 20), height=100)
    header.pack(anchor=tk.CENTER, padx=(170, 0))