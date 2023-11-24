import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class FaceDetectionApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_capture = tk.Button(window, text="Capture", width=10, height=2, bg='yellow', command=self.capture)
        self.btn_capture.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.E)

        self.btn_quit = tk.Button(window, text="Quit", width=10, height=2, bg='red', command=self.quit_app)
        self.btn_quit.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.E)

        self.is_capturing = False
        self.update()
        self.window.mainloop()

    def capture(self):
        ret, frame = self.vid.read()
        if ret:
            # Flip the frame horizontally before saving
            flipped_frame = cv2.flip(frame, 1)
            
            cv2.imwrite("./img/captured_face_original.jpg", flipped_frame)
            gray_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
            
            cv2.imwrite("./img/captured_face_gray.jpg", gray_frame)
            messagebox.showinfo("Capture", "Images captured successfully!")

    def quit_app(self):
        self.window.destroy()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Flip the frame horizontally (mirror effect)
            frame = cv2.flip(frame, 1)
            
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the FaceDetectionApp class
root = tk.Tk()
app = FaceDetectionApp(root, "Face Detection App")
