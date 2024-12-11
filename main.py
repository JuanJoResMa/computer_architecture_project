import tkinter as tk

from ui import StepsApp  # Import the StepsApp class from ui.py

if __name__ == "__main__":
    root = tk.Tk()
    app = StepsApp(root)
    root.mainloop()