import tkinter as tk 
from tkinter import messagebox, simpledialog
from x_pyAPI import X_API

class TwitterApp:
    def __init__(self,root):
        self.root = root
        self.root.title("Twitter Schedular")
        
        self.Xapi = None  
        
        tk.Label(root, text="Consumer Key: ").grid(row=0, column=0, padx=10, pady=10)
        self.consumer_key_entry = tk.Entry(root)
        self.consumer_key_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Consumer Secret: ").grid(row=1, column=0, padx=10, pady=10)
        self.consumer_key_entry_secret = tk.Entry(root)
        self.consumer_key_entry_secret.grid(row=1, column=1, padx=10, pady=10)


