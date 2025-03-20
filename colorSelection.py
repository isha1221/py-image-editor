from tkinter import X, Frame, Button, Label, colorchooser, LEFT, TOP, BOTH
import cv2

class ColorSelector(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="#353b5a", bd=0, pady=10)
        self.current_color = (0, 0, 255)  # Default red in BGR
        self.current_color_rgb = "#FF0000"  # Default red in RGB hex
        self.current_size = 2  # Default size
        
        # Labels and color display
        self.color_label = Label(self, text="Brush Color", 
                               bg="#353b5a", fg="#edf2f4",
                               font=("Helvetica", 10, "bold"))
        self.color_display = Label(self, bg=self.current_color_rgb, 
                                 width=10, height=2, 
                                 bd=1, relief="solid")
        self.color_button = Button(self, text="Select Color", command=self.choose_color)
        
        
        
        # Layout with explicit packing
        self.color_label.pack(side=TOP, padx=5, pady=2, fill=X)
        self.color_display.pack(side=TOP, padx=5, pady=2)
        self.color_button.pack(side=TOP, padx=5, pady=5, fill=X)
       
        
       

        
    def choose_color(self):
        color = colorchooser.askcolor(initialcolor=self.current_color_rgb)
        if color[1]:
            self.current_color_rgb = color[1]
            r = int(color[1][1:3], 16)
            g = int(color[1][3:5], 16)
            b = int(color[1][5:7], 16)
            self.current_color = (b, g, r)  # Convert to BGR for OpenCV
            self.color_display.config(bg=self.current_color_rgb)
            