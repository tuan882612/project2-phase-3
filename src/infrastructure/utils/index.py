import customtkinter as ct

def clear(app: ct.CTk | ct.CTkScrollableFrame) -> None:
    for i in app.winfo_children():
        if (isinstance(app, ct.CTk) and i not in app.side_nav) \
            or isinstance(app, ct.CTkScrollableFrame):
            i.destroy()