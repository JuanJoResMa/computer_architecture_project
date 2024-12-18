import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import app.protocol as protocol


class SequencerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Musical Note Sequencer")
        self.root.geometry("1000x800")  # Tamaño de la ventana

        self.notes = []
        self.port = None

        # Cargar la imagen de fondo
        self.bg_image = Image.open("./resources/background2.png")  # Ruta a tu imagen
        self.bg_image = self.bg_image.resize(
            # Ajustamos el tamaño de la imagen
            (1000, 800), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Crear un Canvas para mostrar la imagen de fondo
        self.canvas = tk.Canvas(root, width=1000, height=800)
        self.canvas.pack(fill="both", expand=True)

        # Añadir la imagen al canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Crear un marco para los widgets (esto asegura que los botones estén encima)
        frame = tk.Frame(self.root, bg='white', bd=5, relief=tk.RAISED)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=315,
                    height=600)  # Ajustamos el tamaño del marco

        # Crear los widgets
        self.label = tk.Label(
            frame, text="Enter a note (e.g., C4, D#4):", bg="white")
        self.entry = tk.Entry(frame)
        self.add_button = tk.Button(
            frame, text="Add Note", command=self.add_note)
        self.notes_display = tk.Listbox(frame, height=10, width=30)
        self.port_label = tk.Label(frame, text="Select Port:", bg="white")
        self.port_var = tk.StringVar(value="No port selected")
        self.port_menu = tk.OptionMenu(frame, self.port_var, "No ports found")
        self.update_ports_button = tk.Button(
            frame, text="Refresh Ports", command=self.update_ports)
        self.send_button = tk.Button(
            frame, text="Send Notes", command=self.send_notes)

        # Organizar los widgets con grid()
        self.label.grid(row=0, column=0, columnspan=2, pady=10)
        self.entry.grid(row=1, column=0, columnspan=2,
                        pady=10, padx=10, sticky="ew")
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.notes_display.grid(row=3, column=0, columnspan=2, pady=10)
        self.port_label.grid(row=4, column=0, pady=10, padx=10, sticky="e")
        self.port_menu.grid(row=4, column=1, pady=10, padx=10, sticky="w")
        self.update_ports_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.send_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Inicializar puertos
        self.update_ports()

    def update_ports(self):
        """Actualizar la lista de puertos disponibles."""
        ports = protocol.list_available_ports()
        menu = self.port_menu["menu"]
        menu.delete(0, "end")
        if ports:
            for port in ports:
                menu.add_command(
                    label=port, command=lambda p=port: self.port_var.set(p))
            self.port_var.set(ports[0])
        else:
            menu.add_command(label="No ports found")
            self.port_var.set("No ports found")

    def add_note(self):
        """Añadir una nota a la secuencia."""
        note = self.entry.get().strip()
        if self.validate_note(note):
            self.notes.append(note)
            self.notes_display.insert(tk.END, note)
            self.entry.delete(0, tk.END)
        else:
            messagebox.showerror(
                "Invalid Note", "Please enter a valid note (e.g., C4, D#4).")

    def validate_note(self, note):
        """Validar el formato de la nota."""
        import re
        pattern = r"^[A-G](#|b)?[0-8]$"
        return re.match(pattern, note) is not None

    def send_notes(self):
        """Enviar la secuencia de notas vía UART."""
        if not self.notes:
            messagebox.showwarning(
                "No Notes", "Please add some notes to send.")
            return

        port = self.port_var.get()
        if port == "No ports found" or not port:
            messagebox.showerror("No Port Selected",
                                 "Please select a valid serial port.")
            return

        try:
            protocol.send_strings_via_uart(self.notes, port=port)
            messagebox.showinfo("Success", "Notes sent successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send notes: {e}")
