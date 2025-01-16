from tkinter import Tk
from tkinterweb import HtmlFrame

root = Tk()
frame = HtmlFrame(root)
frame.pack(fill="both", expand=True)
frame.load_file("map.html")  # Replace "map.html" with any existing HTML file
root.mainloop()
