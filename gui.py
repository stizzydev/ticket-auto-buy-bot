import tkinter as tk
from tkinter import messagebox
import config
import main

def start_bot():
    try:
        main.run_bot()
        messagebox.showinfo("Success", "Bot ran successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_gui():
    root = tk.Tk()
    root.title("Ticket Auto-Buy Bot")

    tk.Label(root, text="Ticket URL").pack()
    url_entry = tk.Entry(root, width=50)
    url_entry.insert(0, config.TICKET_URL)
    url_entry.pack()

    def update_config():
        config.TICKET_URL = url_entry.get()
        start_bot()

    tk.Button(root, text="Run Bot", command=update_config).pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    create_gui()
