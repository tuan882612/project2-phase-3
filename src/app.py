import customtkinter as ct

from views.home import home_view
from views.borrower import borrower_view
from views.checkout import checkout_view
from views.new_book import entry_view
from views.loan_late import loan_late_view
from views.date_range import date_range_view

def load_nav_bar(app: ct.CTk) -> None:
    app.side_nav = []
    
    side_nav = ct.CTkFrame(master=app)
    app.side_nav.append(side_nav)
    side_nav.place(relx=0, rely=0, relwidth=0.2, relheight=2)
    
    veiws = [
        (lambda:home_view(app), "Home"), 
        (lambda:entry_view(app), "Add New Book"), 
        (lambda:borrower_view(app), "Add New Borrower"), 
        (lambda:checkout_view(app), "Checkout Book"),
        (lambda:date_range_view(app), "Date Range"),
        (lambda:loan_late_view(app), "Loans and Late Returns")
    ]
    
    for cmd, view in veiws:
        button = ct.CTkButton(
            master=side_nav, 
            text=view, 
            command=cmd)
        app.side_nav.append(button)
        button.pack(padx=5, pady=5, fill="x")

def main() -> None:
    ct.set_appearance_mode("dark") 
    ct.set_default_color_theme("blue") 
    app = ct.CTk()
    app.title("Library Management System")
    app.geometry("1000x600")
    app.resizable(width=False, height=False)
    
    home_view(app)
    load_nav_bar(app)

    app.mainloop()

if __name__ == '__main__':
    main()