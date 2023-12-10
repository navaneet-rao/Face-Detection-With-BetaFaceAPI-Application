import cv2
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import BetaFaceApi as BFapi
import re
class FaceDetectionApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 350) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 350) 
        
        # self.window.state('zoomed')
        
        self.canvas_width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.canvas_height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        
        #canvas
        
        self.canvas_frame = tk.Frame(window)

        self.canvas_top = tk.Canvas(self.canvas_frame, bg='grey', width=self.canvas_width, height=self.canvas_height )
        self.canvas_top.grid(row=0, column=0)        
        self.canvas_captured_image = tk.Canvas(self.canvas_frame, bg='grey', width=self.canvas_width, height=self.canvas_height)
        self.canvas_captured_image.grid(row=0, column=1)        
        
        self.canvas_frame.pack(side=tk.LEFT, padx=10, pady=10, anchor=tk.NW )
        
        #buttons
                
        self.btn_frame = tk.Frame(window)
        
        self.btn_capture = tk.Button(self.btn_frame, text="Capture", width=10, height=2, bg='yellow', command=self.capture)
        self.btn_capture.grid(row=0, column=0, padx=5, pady=5)
        self.btn_upload_image = tk.Button(self.btn_frame, text="Upload different Image", width=20, height=2, bg='yellow', command=self.users_upload_image)
        self.btn_upload_image.grid(row=1, column=0, padx=5, pady=5)
        self.btn_upload = tk.Button(self.btn_frame, text="Upload Capture Image", width=20, height=2, bg='yellow', command=self.upload_image)
        self.btn_upload.grid(row=2, column=0, padx=5, pady=5)
        
        self.btn_frame.pack(side=tk.TOP)
        
        #quit button

        self.btn_quit = tk.Button(window, text="Quit", width=10, height=2, bg='red', command=self.quit_app)
        self.btn_quit.pack(side=tk.RIGHT, padx=10, pady=10, anchor=tk.SE)

        self.is_capturing = False
        self.update()
        self.window.mainloop()

    def capture(self):
        ret, frame = self.vid.read()
        if ret:
            flipped_frame = cv2.flip(frame, 1)

            cv2.imwrite("./img/captured_face_original.jpg", flipped_frame)
            original_image = cv2.imread("./img/captured_face_original.jpg")
            
            original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

            face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
            faces = face_classifier.detectMultiScale(original_image_rgb, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

            for (x, y, w, h) in faces:
                cv2.rectangle(original_image_rgb, (x, y), (x+w, y+h), (0, 255, 0), 2)

            image_with_detection = Image.fromarray(original_image_rgb)
            photo_with_detection = ImageTk.PhotoImage(image_with_detection)

            self.canvas_captured_image.delete("all")  
            self.canvas_captured_image.create_image(0, 0, image=photo_with_detection, anchor=tk.NW)
            self.canvas_captured_image.image = photo_with_detection

    def upload_image(self):
        image_path = ".\\img\\captured_face_original.jpg"

        api_instance = BFapi.BetaFaceApi(image_path)
        
        encoded_image_string = api_instance.image_to_base64(api_instance.image_path)
        response_json = api_instance.send_image_to_API(encoded_image_string)

        data = api_instance.faceData_race(response_json)

        print(data)
        print("________________________________________________")

        messagebox.showinfo("Upload", 'Image uploaded')
        

    def users_upload_image(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File",filetype=(("jpeg","*.jpg"),("png","*.png")))
        print(self.fileName)
        file = re.sub(r'/', '\\', self.fileName)
        print(file)
        self.canvas_captured_image.delete("all")  
        self.canvas_captured_image.create_image(0, 0, image=file)
        self.canvas_captured_image.image = file
        
    def quit_app(self):
        self.window.destroy()
        os.remove("./img/captured_face_original.jpg")

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas_top.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
        self.window.after(10, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

root = tk.Tk()
app = FaceDetectionApp(root, "Face Detection App")


