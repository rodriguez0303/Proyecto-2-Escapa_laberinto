import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk  # Usamos Pillow para cargar imágenes JPG
import os 
import random #se utilizará para ordenar las imágenes de forma aleatória
import winsound  # se utilizará para reproducir  la música  
import threading #  Se utilizará para ejecutar los hilos 


###########################################

# Evita que se presenten problemas al cargar las imagenes 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Clase que contiene la pantalla principal 
class PantallaPrincipal:

    def __init__(self, pantalla_principal):
        self.pantalla_principal = pantalla_principal
        self.pantalla_principal.title("Escapando del laberinto")
        
        # A la pantalla principal se le asigna un canvas para que pueda colocarse botones 
        self.canvas = Canvas(self.pantalla_principal, bg="white")
        
        #Se extiende el canvas al tamaño total de la ventana principal
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        #Carga el fondo de la pantalla principal solo cuando ya se tiene el tamaño del canvas
        self.pantalla_principal.after(200, self.tamano_pantalla_principal) 
        
        #Se llama a la función que contiene el botón juego y lo coloca en la pantalla principal 
        self.pantalla_principal.after(400, self.boton_juego)
        
        # Hace que el botón jugar se muestre sobre el fondo del canvas 
        self.canvas.tag_raise("boton_jugar")

#######
#Función que carga la imagen de la pantalla principal 

    def tamano_pantalla_principal(self):
        ruta = os.path.join(BASE_DIR, "Imagenes","Fondo2.jpg")
        imagen = Image.open(ruta)
        
        #Se actualiza el tamaño real del canvas antes de usarlo.
        self.canvas.update_idletasks()

        # Se obtiene el tamaño real del canvas
        ancho_pantalla_principal = self.canvas.winfo_width()
        alto_pantalla_principal = self.canvas.winfo_height()

        #Se ajusta la imagen al tamaño de la ventana
        imagen_ajustada = imagen.resize((ancho_pantalla_principal, alto_pantalla_principal), Image.LANCZOS)
        self.fondo = ImageTk.PhotoImage(imagen_ajustada)

        #Mantiene la imagen de fondo y evita que se borre 
        self.canvas.create_image(0, 0, image=self.fondo, anchor="nw")

#############################################
    # Función que contiene al botón jugar 
    def boton_juego(self):

        # Ruta de la imagen del botón
        ruta_boton = os.path.join(BASE_DIR, "Imagenes", "Fondo3.png")

        # Se abre la ruta donde se encuentra la imagen del botón 
        imagen_boton = Image.open(ruta_boton)

        # Tamaño máximo del botón
        max_ancho, max_alto = 150, 60

        # Obtiene el tamaño original de la imagen que se colocará de fondo en el botón 
        ancho_original, alto_original = imagen_boton.size
        proporcion = min(max_ancho / ancho_original, max_alto / alto_original)

        # Calcula el nuevo tamaño del botón de acuerdo a su proporcionalidad
        nuevo_ancho = int(ancho_original * proporcion)
        nuevo_alto = int(alto_original * proporcion)

        # Redimensiona la imagen del botón manteniendo proporción
        imagen_boton = imagen_boton.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
        imagen_boton_tk = ImageTk.PhotoImage(imagen_boton)

        # Creación del botón jugar
        boton_jugar = tk.Button(
            self.pantalla_principal,
            image=imagen_boton_tk,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2",
            command=self.ventana_nombre_jugador # Se llama a la función que contiene la ventana en la que el jugador digita su nombre
        )
        
        # evita que el botón se borre de memoria
        boton_jugar.image = imagen_boton_tk  

        # Coloca el botón jugar sobre el canvas de la pantalla principal 
        self.canvas.create_window(
            800,       # posición X en pantalla
            300,       # posición Y en pantalla
            window=boton_jugar,
            tags="boton_jugar" 
        )

#############################################
    # Función que solicita el nombre del jugador (servirá para registrar su puntaje)
    def ventana_nombre_jugador(self):
        
        #Toplevel: permite abrir una ventana secundaria sobre la ventana principal (para escribir el nombre del usuario) 
        ventana_nombre = tk.Toplevel(self.pantalla_principal)
        
        # Da el nombre a la ventana del nombre del jugador 
        ventana_nombre.title("Nombre del jugador") 
        
        # Se define el tamaño  de la ventana para que el usuario ingrese su nombre  + posición eje x + posición eje  
        ventana_nombre.geometry("300x200+900+200") 
        #ventana.geometry("300x200")
        
        # Evita que se pueda aumentar o disminuir el tamaño de la ventana 
        ventana_nombre.resizable(False, False)
        
        # mantiene esta ventana siempre al frente
        ventana_nombre.attributes('-topmost', True)

        # Se coloca una imagen a la pantalla de ingresar los datos del usuario 
        ruta_fondo = os.path.join(BASE_DIR, "Imagenes", "Fondo4.jpg")
        imagen_fondo = Image.open(ruta_fondo)
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo.resize((300, 200), Image.LANCZOS))

        # Se crea un Label para mostrar la imagen de fondo
        label_fondo = Label(ventana_nombre, image=imagen_fondo_tk)
        
        # Se coloca el laberl para que ocupe todo el fondo de la ventana
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)

        # Mantiene la imagen en memoria
        label_fondo.imagen_fondo = imagen_fondo_tk

        #Creación del label para indicarle al jugador que digite su nombre
        label_nombre = Label(
                                ventana_nombre,
                                text="Ingrese su nombre de jugador:",
                                bg="RoyalBlue4",
                                fg="white"
                            )
        label_nombre.pack(pady=10)

        #Creación de cuadro de texto para que el jugador digite su nombre 
        cuadro_texto_nombre = Entry(ventana_nombre, width=27, bg="white")
        cuadro_texto_nombre.pack(pady=10)
#####
        #Función que guarda u obtiene el nombre digitado por el jugador 
        def comenzar_juego():
            nombre_jugador = cuadro_texto_nombre.get().strip()
            if not nombre_jugador:
                messagebox.showwarning("Aviso", "Debe ingresar un nombre")
                return
            
            print(f"Jugador: {nombre_jugador}")  # Muestra el nombre en la consola
            
            # Se guarda el nombre del jugador en un archivo TXT 
            with open("JugadoresCHAT.txt", "a") as archivo:
                archivo.write(f"{nombre_jugador},0\n")

            # Cierra la ventana
            ventana_nombre.destroy()
            
            #Creación del botón comenzar (permite seleccionar entre los dos juegos de laberintos)
        boton_comenzar = tk.Button(
                                        ventana_nombre,
                                        text="Comenzar",
                                        bg="SpringGreen4",
                                        fg="black",
                                        command=comenzar_juego)
        boton_comenzar.pack(pady=10)