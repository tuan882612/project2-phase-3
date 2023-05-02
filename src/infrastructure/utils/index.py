import customtkinter as ct

def clear(app: ct.CTk | ct.CTkScrollableFrame | ct.CTkFrame) -> None:
    for i in app.winfo_children():
        if (isinstance(app, ct.CTk) and i not in app.side_nav) or \
            isinstance(app, ct.CTkScrollableFrame) or \
            isinstance(app, ct.CTkFrame):
            i.destroy()
            
def clear_message(frame: ct.CTkFrame) -> None:
    for i in frame.winfo_children():
        if isinstance(i, ct.CTkLabel) and\
            getattr(i, 'is_error', False) or\
            getattr(i, 'is_success', False):
            i.destroy()
            