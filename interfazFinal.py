import threading
import cv2
from ultralytics import YOLO
import tkinter as tk
from tkinter import ttk
from tkinter import*
from tkinter import messagebox
from PIL import Image, ImageTk
from threading import Thread

class VideoApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.menuBar = Menu(self.window)
        self.window.config(menu=self.menuBar)

        self.model = YOLO("best.pt")

        self.video_source_options = ["Cámara Web", "Archivo de Video"]
        self.selected_video_source = tk.StringVar(value=self.video_source_options[0])
        
        self.archivoMenu = Menu(self.menuBar, tearoff=0)
        self.archivoMenu.add_command(label="Nuevo")
        self.archivoMenu.add_command(label="Abrir")
        self.archivoMenu.add_command(label="Guardar")
        self.archivoMenu.add_command(label="Cerrar")
        self.archivoMenu.add_separator()
        self.archivoMenu.add_command(label="Salir")

        self.editMenu = Menu(self.menuBar, tearoff=0)

        self.editMenu.add_command(label="Cortar")
        self.editMenu.add_command(label="Copiar")
        self.editMenu.add_command(label="Pegar")

        self.ayudaMenu = Menu(self.menuBar, tearoff=0)

        self.ayudaMenu.add_command(label="Licencia")
        self.ayudaMenu.add_separator()
        
        self.is_playing = False
        self.create_ui()
        self.update()

        # Inicializar la captura de video desde la cámara web
        self.vid = None
        
        # Crear un lienzo para mostrar el video

        self.canvas = tk.Canvas(window, width=450, height=450)
        self.canvas.pack(padx=150, pady=150)
        
        # Botón de inicio
        self.btn_start = tk.Button(window, text="Iniciar", width=10, command=self.start_video)
        self.btn_start.pack(anchor=tk.CENTER, expand=True)
        
        self.window.mainloop()
        
    def create_ui(self):
        control_frame = tk.Frame(self.window)
        control_frame.pack(padx=10, pady=10)

        source_label = tk.Label(control_frame, text="Origen del Video:")
        source_label.grid(row=0, column=0, padx=(0, 5))

        video_source_menu = ttk.Combobox(control_frame, textvariable=self.selected_video_source, values=self.video_source_options, state="readonly")
        video_source_menu.grid(row=0, column=1)
        
        self.menuBar.add_cascade(label="Archivo", menu=self.archivoMenu)
        self.menuBar.add_cascade(label="Editar", menu=self.editMenu)
        self.menuBar.add_cascade(label="Ayuda", menu=self.ayudaMenu)


    
    def start_video(self):
        
        video_source = self.selected_video_source.get()
        if video_source == "Cámara Web":
            video_source = 0
        else:
            video_source = tk.filedialog.askopenfilename()
    
        self.vid = cv2.VideoCapture(video_source)

        self.is_playing = True
        
      
    def update(self):

        if self.is_playing:
            # Capturar un fotograma desde la cámara

            ret, frame = self.vid.read()
            if ret:

                # Convertir el fotograma de OpenCV a formato de imagen compatible con Tkinter
                resultados = self.model.predict(frame)
                annotated_frame = resultados[0].plot()
                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(annotated_frame)
                image = ImageTk.PhotoImage(image=image)
                
                # # Mostrar el fotograma en el lienzo

                self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
                self.canvas.image = image
                        
                
        # Llamar a esta función recursivamente después de 10 milisegundos
        self.window.after(10, self.update)
    
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        
    
    def start_detection(self):
        try:
            while True:
                ret, frame = self.vid.read()
                if not ret:
                    break

                resultados = self.model.predict(frame)
                annotated_frame = resultados[0].plot()
                annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(annotated_frame)
                image = ImageTk.PhotoImage(image)
                
                self.photo = ImageTk.PhotoImage(Image.fromarray(annotated_frame))
                self.update_video()

                if self.video_label is not None:
                    self.video_label.config(image=image)
                    self.video_label.image = image

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            self.cap.release()
            print("Bucle de lectura de video finalizado.")
        except Exception as e:
            print("Error:", e)
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    window = tk.Tk()
    app = VideoApp(window, "Sistema de Deteccion de Drones")

#Verificacion Github