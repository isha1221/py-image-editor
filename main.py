import tkinter as tk
from tkinter import ttk, BOTTOM, TOP, LEFT, BOTH, RIGHT
import cv2
from editBar import EditBar
from imageViewer import ImageViewer
from colorSelection import ColorSelector

class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1000x600")
        self.filename = ""
        self.original_image = None
        self.processed_image = None
        self.is_image_selected = False
        self.is_draw_state = False
        self.is_crop_state = False

        self.filter_frame = None
        self.adjust_frame = None

        self.configure(bg="#2b2d42")
        self.title("Image Editor Pro")
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TButton", 
                       background="#4ecca3",
                       foreground="white",
                       font=("Helvetica", 10, "bold"),
                       padding=5)
        style.map("TButton",
                 background=[('active', '#45b592')])

        self.editbar = EditBar(master=self)
        self.image_viewer = ImageViewer(master=self)
        self.color_selector = ColorSelector(master=self)
        
        self.status_bar = tk.Label(self, 
                                 text="Ready | Open an image to begin", 
                                 bg="#1d1e2c", 
                                 fg="#edf2f4",
                                 font=("Helvetica", 9),
                                 bd=0,
                                 relief="flat",
                                 anchor="w",
                                 padx=10)
        
        self.editbar.pack(side=LEFT, fill="y", padx=5, pady=5)
        self.image_viewer.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.status_bar.pack(side=BOTTOM, fill="x")
        
        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        if event.widget == self and self.is_image_selected:
            self.after_cancel(self.resize_job) if hasattr(self, 'resize_job') else None
            self.resize_job = self.after(200, self.image_viewer.show_image)
            
    def update_status(self, message):
        self.status_bar.config(text=message)

if __name__ == "__main__":
    root = Main()
    root.mainloop()