import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import protocol


class StepsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COMPUTER ARCHITECTURE PROJECT")
        self.root.geometry("400x340")
        self.steps = []

        # Load the image
        self.bg_image = Image.open("background.png")  # Replace with your image path
        self.bg_image = self.bg_image.resize((400, 300), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas and set the image as background
        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Create widgets
        self.label = tk.Label(root, text="Enter a step:", bg="white")
        self.entry = tk.Entry(root)
        self.add_button = tk.Button(root, text="Add Step", command=self.add_step)
        self.send_button = tk.Button(root, text="Play", command=self.play)
        self.steps_frame = tk.Frame(root)
        self.steps_canvas = tk.Canvas(self.steps_frame, height=50)
        self.steps_inner_frame = tk.Frame(self.steps_canvas)

        # Add a horizontal scrollbar
        self.scrollbar = tk.Scrollbar(self.steps_frame, orient=tk.HORIZONTAL, command=self.steps_canvas.xview)
        self.steps_canvas.configure(xscrollcommand=self.scrollbar.set)

        # Place widgets on the canvas
        self.canvas.create_window(200, 20, window=self.label)
        self.canvas.create_window(200, 50, window=self.entry)
        self.canvas.create_window(200, 80, window=self.add_button)
        self.canvas.create_window(200, 110, window=self.send_button)
        self.canvas.create_window(200, 150, window=self.steps_frame)

        self.steps_frame.pack(fill=tk.X)
        self.steps_canvas.pack(side=tk.TOP, fill=tk.X, expand=True)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.steps_inner_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.steps_canvas.create_window((0, 0), window=self.steps_inner_frame, anchor="nw")
        self.steps_inner_frame.bind("<Configure>", lambda e: self.steps_canvas.configure(scrollregion=self.steps_canvas.bbox("all")))

    def add_step(self):
        step = self.entry.get()
        if step:
            if len(self.steps) < 30:
                self.steps.append(step)
                step_label = tk.Label(self.steps_inner_frame, text=step, borderwidth=1, relief="solid")
                step_label.pack(side=tk.LEFT, padx=5, pady=5)
                step_label.bind("<Button-1>", lambda e, lbl=step_label: self.edit_step(lbl))
                self.steps_inner_frame.update_idletasks()
                self.steps_canvas.config(scrollregion=self.steps_canvas.bbox("all"))
                self.entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Limit Reached", "You cannot add more than 30 steps")
        else:
            messagebox.showwarning("Input Error", "Step cannot be empty")

    def edit_step(self, label):
        step_index = list(self.steps_inner_frame.children.values()).index(label)
        new_step = simpledialog.askstring("Edit Step", "Modify the step:", initialvalue=label.cget("text"))
        if new_step:
            self.steps[step_index] = new_step
            label.config(text=new_step)

    def get_steps(self):
        print(self.steps)
        return self.steps

    def play(self):
        protocol.send_strings_via_uart(self.get_steps())