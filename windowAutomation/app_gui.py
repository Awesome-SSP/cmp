# app_gui.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def show_selection():
    name = name_entry.get()
    choice = dropdown.get()
    messagebox.showinfo("Selection", f"Name: {name}\nChoice: {choice}")

root = tk.Tk()
root.title("Input & Dropdown Example")
root.geometry("300x200+100+206")

tk.Label(root, text="Enter your name:").pack(pady=5)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

tk.Label(root, text="Select an option:").pack(pady=5)
options = ["Option 1", "Option 2", "Option 3"]
dropdown = ttk.Combobox(root, values=options)
dropdown.current(0)
dropdown.pack(pady=5)

submit_btn = tk.Button(root, text="Submit", command=show_selection)
submit_btn.pack(pady=10)

root.mainloop()
