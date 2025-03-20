from tkinter import Frame, Button, LEFT, RIGHT, TOP, BOTTOM, X, Y, BOTH, Label, GROOVE, FLAT
from tkinter import filedialog
from filterFrame import FilterFrame
from adjustFrame import AdjustFrame
import cv2

class EditBar(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="#353b5a", bd=0, relief=FLAT)
        
        self.file_frame = Frame(self, bg="#353b5a", bd=0, pady=10)
        self.edit_frame = Frame(self, bg="#353b5a", bd=0, pady=10)
        
        Label(self.file_frame, 
              text="File Operations", 
              bg="#353b5a", 
              fg="#edf2f4",
              font=("Helvetica", 11, "bold")).pack(pady=5)
              
        self.new_button = Button(self.file_frame, text="Open Image")
        self.save_button = Button(self.file_frame, text="Save")
        self.save_as_button = Button(self.file_frame, text="Save As")
        
        Label(self.edit_frame, 
              text="Edit Tools", 
              bg="#353b5a", 
              fg="#edf2f4",
              font=("Helvetica", 11, "bold")).pack(pady=5)
              
        self.draw_button = Button(self.edit_frame, text="Draw")
        self.crop_button = Button(self.edit_frame, text="Crop")
        self.filter_button = Button(self.edit_frame, text="Filter")
        self.adjust_button = Button(self.edit_frame, text="Adjust")
        self.clear_button = Button(self.edit_frame, text="Reset")

        self.new_button.bind("<ButtonRelease>", self.new_button_released)
        self.save_button.bind("<ButtonRelease>", self.save_button_released)
        self.save_as_button.bind("<ButtonRelease>", self.save_as_button_released)
        self.draw_button.bind("<ButtonRelease>", self.draw_button_released)
        self.crop_button.bind("<ButtonRelease>", self.crop_button_released)
        self.filter_button.bind("<ButtonRelease>", self.filter_button_released)
        self.adjust_button.bind("<ButtonRelease>", self.adjust_button_released)
        self.clear_button.bind("<ButtonRelease>", self.clear_button_released)

        for btn in [self.new_button, self.save_button, self.save_as_button]:
            btn.pack(fill=X, padx=10, pady=3)
            
        for btn in [self.draw_button, self.crop_button, self.filter_button, 
                   self.adjust_button, self.clear_button]:
            btn.pack(fill=X, padx=10, pady=3)
        
        self.file_frame.pack(side=TOP, fill=X)
        self.edit_frame.pack(side=TOP, fill=X)

    def new_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.new_button:
            if self.master.is_draw_state:
                self.master.image_viewer.deactivate_draw()
            if self.master.is_crop_state:
                self.master.image_viewer.deactivate_crop()

            filename = filedialog.askopenfilename(
                filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
            )
            
            if filename:
                image = cv2.imread(filename)
                if image is not None:
                    self.master.filename = filename
                    self.master.original_image = image.copy()
                    self.master.processed_image = image.copy()
                    self.master.image_viewer.show_image()
                    self.master.is_image_selected = True
                    self.master.title(f"Image Editor Pro - {filename.split('/')[-1]}")
                    self.master.update_status(f"Opened: {filename.split('/')[-1]}")

    def save_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_button:
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                save_image = self.master.processed_image
                image_filename = self.master.filename
                cv2.imwrite(image_filename, save_image)
                self.master.update_status(f"Saved: {image_filename.split('/')[-1]}")

    def save_as_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.save_as_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                original_file_type = self.master.filename.split('.')[-1]
                filename = filedialog.asksaveasfilename(
                    defaultextension=f".{original_file_type}",
                    filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("All files", "*.*")]
                )
                if filename:
                    save_image = self.master.processed_image
                    cv2.imwrite(filename, save_image)
                    self.master.filename = filename
                    self.master.title(f"Image Editor Pro - {filename.split('/')[-1]}")
                    self.master.update_status(f"Saved as: {filename.split('/')[-1]}")

    def draw_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.draw_button:
            if self.master.is_image_selected:
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                    self.draw_button.config(relief="raised")
                    self.master.color_selector.pack_forget()
                else:
                    self.master.image_viewer.activate_draw()
                    self.draw_button.config(relief="sunken")
                    self.master.color_selector.pack(side=TOP, fill=X, padx=5, pady=5)

    def crop_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.crop_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                    self.draw_button.config(relief="raised")
                    self.master.color_selector.pack_forget()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                    self.crop_button.config(relief="raised")
                else:
                    self.master.image_viewer.activate_crop()
                    self.crop_button.config(relief="sunken")

    def filter_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.filter_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                    self.draw_button.config(relief="raised")
                    self.master.color_selector.pack_forget()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                    self.crop_button.config(relief="raised")
                self.master.filter_frame = FilterFrame(master=self.master)
                self.master.filter_frame.grab_set()

    def adjust_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.adjust_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                    self.draw_button.config(relief="raised")
                    self.master.color_selector.pack_forget()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                    self.crop_button.config(relief="raised")
                self.master.adjust_frame = AdjustFrame(master=self.master)
                self.master.adjust_frame.grab_set()

    def clear_button_released(self, event):
        if self.winfo_containing(event.x_root, event.y_root) == self.clear_button:
            if self.master.is_image_selected:
                if self.master.is_draw_state:
                    self.master.image_viewer.deactivate_draw()
                    self.draw_button.config(relief="raised")
                    self.master.color_selector.pack_forget()
                if self.master.is_crop_state:
                    self.master.image_viewer.deactivate_crop()
                    self.crop_button.config(relief="raised")
                self.master.processed_image = self.master.original_image.copy()
                self.master.image_viewer.show_image()
                self.master.update_status("Image reset to original")