from tkinter import Toplevel, Label, Scale, Button, HORIZONTAL, RIGHT
import cv2

class AdjustFrame(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.configure(bg="#2b2d42")
        self.title("Adjust Image")
        self.geometry("300x400")

        self.brightness_value = 0
        self.previous_brightness_value = 0
        self.original_image = self.master.processed_image
        self.processing_image = self.master.processed_image

        self.brightness_label = Label(self, text="Brightness", bg="#2b2d42", fg="#edf2f4",
                                    font=("Helvetica", 10, "bold"))
        self.brightness_scale = Scale(self, from_=0, to_=2, length=250, resolution=0.1,
                                    orient=HORIZONTAL, bg="#2b2d42", fg="#edf2f4",
                                    highlightthickness=0, troughcolor="#4ecca3")
        self.r_label = Label(self, text="Red", bg="#2b2d42", fg="#edf2f4",
                           font=("Helvetica", 10, "bold"))
        self.r_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                           orient=HORIZONTAL, bg="#2b2d42", fg="#edf2f4",
                           highlightthickness=0, troughcolor="#ef476f")
        self.g_label = Label(self, text="Green", bg="#2b2d42", fg="#edf2f4",
                           font=("Helvetica", 10, "bold"))
        self.g_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                           orient=HORIZONTAL, bg="#2b2d42", fg="#edf2f4",
                           highlightthickness=0, troughcolor="#06d6a0")
        self.b_label = Label(self, text="Blue", bg="#2b2d42", fg="#edf2f4",
                           font=("Helvetica", 10, "bold"))
        self.b_scale = Scale(self, from_=-100, to_=100, length=250, resolution=1,
                           orient=HORIZONTAL, bg="#2b2d42", fg="#edf2f4",
                           highlightthickness=0, troughcolor="#118ab2")
        self.apply_button = Button(self, text="Apply")
        self.preview_button = Button(self, text="Preview")
        self.cancel_button = Button(self, text="Cancel")

        self.brightness_scale.set(1)

        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.preview_button.bind("<ButtonRelease>", self.show_button_release)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        for widget in [self.brightness_label, self.brightness_scale,
                      self.r_label, self.r_scale,
                      self.g_label, self.g_scale,
                      self.b_label, self.b_scale]:
            widget.pack(pady=5, padx=10)
            
        self.preview_button.pack(side=RIGHT, padx=5, pady=10)
        self.cancel_button.pack(side=RIGHT, padx=5)
        self.apply_button.pack(side=RIGHT, padx=5)

    def apply_button_released(self, event):
        self.master.processed_image = self.processing_image
        self.close()

    def show_button_release(self, event):
        self.processing_image = cv2.convertScaleAbs(self.original_image, alpha=self.brightness_scale.get())
        b, g, r = cv2.split(self.processing_image)

        for b_value in b:
            cv2.add(b_value, self.b_scale.get(), b_value)
        for g_value in g:
            cv2.add(g_value, self.g_scale.get(), g_value)
        for r_value in r:
            cv2.add(r_value, self.r_scale.get(), r_value)

        self.processing_image = cv2.merge((b, g, r))
        self.show_image(self.processing_image)

    def cancel_button_released(self, event):
        self.close()

    def show_image(self, img=None):
        self.master.image_viewer.show_image(img=img)

    def close(self):
        self.show_image()
        self.destroy()