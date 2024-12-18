import tkinter as tk
from app.ui import SequencerApp  # Asegúrate de que la clase correcta esté importada

if __name__ == "__main__":
    root = tk.Tk()
    app = SequencerApp(root)  # Asegúrate de usar la clase que corresponde
    root.mainloop()
