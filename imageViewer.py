from tkinter import Frame, Canvas, CENTER, ROUND
from PIL import Image, ImageTk
import cv2

class ImageViewer(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=master, bg="#2b2d42", width=600, height=400)
        self.shown_image = None
        self.x = 0
        self.y = 0
        self.crop_start_x = 0
        self.crop_start_y = 0
        self.crop_end_x = 0
        self.crop_end_y = 0
        self.draw_ids = list()
        self.rectangle_id = 0
        self.ratio = 0
        self.crop_guides = []

        self.canvas = Canvas(self, bg="#2b2d42", width=600, height=400, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

    def show_image(self, img=None):
        self.clear_canvas()
        if img is None:
            image = self.master.processed_image.copy()
        else:
            image = img

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channels = image.shape
        ratio = height / width

        new_width = width
        new_height = height

        if height > self.winfo_height() or width > self.winfo_width():
            if ratio < 1:
                new_width = self.winfo_width()
                new_height = int(new_width * ratio)
            else:
                new_height = self.winfo_height()
                new_width = int(new_height * (width / height))

        self.shown_image = cv2.resize(image, (new_width, new_height))
        self.shown_image = ImageTk.PhotoImage(Image.fromarray(self.shown_image))
        self.ratio = height / new_height

        self.canvas.config(width=new_width, height=new_height)
        self.canvas.create_image(new_width / 2, new_height / 2, anchor=CENTER, image=self.shown_image)

    def activate_draw(self):
        self.canvas.bind("<ButtonPress>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.master.is_draw_state = True

    def activate_crop(self):
        self.canvas.bind("<ButtonPress>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.crop)
        self.canvas.bind("<ButtonRelease>", self.end_crop)
        self._show_crop_guides()
        self.master.is_crop_state = True

    def deactivate_draw(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.master.is_draw_state = False

    def deactivate_crop(self):
        self.canvas.unbind("<ButtonPress>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease>")
        self._hide_crop_guides()
        self.master.is_crop_state = False

    def start_draw(self, event):
        self.x = event.x
        self.y = event.y

    def draw(self, event):
        color_rgb = self.master.color_selector.current_color
        size = self.master.color_selector.current_size
        b, g, r = color_rgb
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        
        self.draw_ids.append(self.canvas.create_line(
            self.x, self.y, event.x, event.y,
            width=size,  # Use the current_size directly
            fill=hex_color,
            capstyle=ROUND,
            smooth=True
        ))

        cv2.line(
            self.master.processed_image,
            (int(self.x * self.ratio), int(self.y * self.ratio)),
            (int(event.x * self.ratio), int(event.y * self.ratio)),
            color_rgb,
            thickness=max(1, int(self.ratio * size)),  # Ensure minimum thickness of 1
            lineType=cv2.LINE_AA
        )
        self.x = event.x
        self.y = event.y

    def start_crop(self, event):
        self.crop_start_x = event.x
        self.crop_start_y = event.y

    def crop(self, event):
        if self.rectangle_id:
            self.canvas.delete(self.rectangle_id)

        self.crop_end_x = event.x
        self.crop_end_y = event.y

        self.rectangle_id = self.canvas.create_rectangle(
            self.crop_start_x, self.crop_start_y,
            self.crop_end_x, self.crop_end_y,
            outline="#4ecca3",
            width=2,
            stipple="gray50"
        )

        width = abs(self.crop_end_x - self.crop_start_x)
        height = abs(self.crop_end_y - self.crop_start_y)
        
        x_pos = min(self.crop_start_x, self.crop_end_x) + 5
        y_pos = min(self.crop_start_y, self.crop_end_y) + 5
        
        if hasattr(self, 'dimension_text') and self.dimension_text:
            self.canvas.delete(self.dimension_text)
            
        self.dimension_text = self.canvas.create_text(
            x_pos, y_pos,
            text=f"{int(width * self.ratio)} × {int(height * self.ratio)}",
            fill="#edf2f4",
            anchor="nw",
            font=("Helvetica", 9)
        )

    def end_crop(self, event):
        if self.crop_start_x <= self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x > self.crop_end_x and self.crop_start_y <= self.crop_end_y:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_start_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_end_y * self.ratio)
        elif self.crop_start_x <= self.crop_end_x and self.crop_start_y > self.crop_end_y:
            start_x = int(self.crop_start_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_end_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)
        else:
            start_x = int(self.crop_end_x * self.ratio)
            start_y = int(self.crop_end_y * self.ratio)
            end_x = int(self.crop_start_x * self.ratio)
            end_y = int(self.crop_start_y * self.ratio)

        if end_x - start_x < 10 or end_y - start_y < 10:
            return

        x = slice(start_x, end_x, 1)
        y = slice(start_y, end_y, 1)
        self.master.processed_image = self.master.processed_image[y, x]

        if hasattr(self, 'dimension_text'):
            self.canvas.delete(self.dimension_text)
        self._hide_crop_guides()
        self.show_image()

    def _show_crop_guides(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        for i in range(1, 3):
            line = self.canvas.create_line(
                width * i/3, 0, width * i/3, height,
                dash=(4, 4), fill="#edf2f4", width=1
            )
            self.crop_guides.append(line)
            line = self.canvas.create_line(
                0, height * i/3, width, height * i/3,
                dash=(4, 4), fill="#edf2f4", width=1
            )
            self.crop_guides.append(line)

    def _hide_crop_guides(self):
        for guide in self.crop_guides:
            self.canvas.delete(guide)
        self.crop_guides = []

    def clear_canvas(self):
        self.canvas.delete("all")

    def clear_draw(self):
        for id_item in self.draw_ids:
            self.canvas.delete(id_item)
        self.draw_ids = []