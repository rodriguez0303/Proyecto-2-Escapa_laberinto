import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk  # Usamos Pillow para cargar imágenes JPG
import os 
import random #se utilizará para generar el laberinto 
import winsound  # se utilizará para reproducir  la música  
import threading #  Se utilizará para ejecutar los hilos 
# Evita que se presenten problemas al cargar las imagenes 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

##########################################################
# Clases  que contiene los tipos de terrreno del laberinto 
 # Aplica tanto para el juego "Cazador" como "Escapar"

class Terreno:
    
    #Función que carga la imagen del terreno del laberinto 
    def __init__(self, ruta_imagen):
     
        # Se define la ruta donde esta la imagen
        imagen_terreno = os.path.join(BASE_DIR, "Imagenes", ruta_imagen)
        #Se abre la carpeta que contiene la imagen 
        imagen_pillow = Image.open(imagen_terreno).resize((64, 64), Image.LANCZOS)
        # convierte una imagen de PIL a un formato que Tkinter sí puede mostrar en canvas, label, button
        self.imagen = ImageTk.PhotoImage(imagen_pillow)
        
    # Función que permite caminar sobre la celda que es "Terreno"    
    def permite_paso_terreno(self):
        return True

##########################################################
class Camino(Terreno):
    
     #Función que carga la imagen del camino del laberinto 
    def __init__(self):
       
       # Se define la ruta donde esta la imagen
        imagen_completa = os.path.join(BASE_DIR, "Imagenes", "Camino.jpg")
        #Se abre la carpeta que contiene la imagen 
        imagen_pillow = Image.open(imagen_completa).resize((64, 64), Image.LANCZOS)
         # convierte una imagen de PIL a un formato que Tkinter sí puede mostrar en canvas, label, button
        self.imagen = ImageTk.PhotoImage(imagen_pillow)
    
    # Función que permite caminar sobre la celda que es "Camino"
    def permite_paso_camino(self):
        return True
##########################################################
class Muro(Terreno):

    #Función que carga la imagen del muro del laberinto 
    def __init__(self):
       
       # Se define la ruta donde esta la imagen
        imagen_completa = os.path.join(BASE_DIR, "Imagenes", "Muro.jpg")
        #Se abre la carpeta que contiene la imagen 
        imagen_pillow = Image.open(imagen_completa).resize((64, 64), Image.LANCZOS)
         # convierte una imagen de PIL a un formato que Tkinter sí puede mostrar en canvas, label, button
        self.imagen = ImageTk.PhotoImage(imagen_pillow)
        
    # Función que no permite caminar sobre la celda que es "Muro"
    def permite_paso_muro(self):
        return False
    
##########################################################
class Tunel(Terreno):
    
    #Función que carga la imagen del tunel del laberinto 
    def __init__(self):
    
        # Se define la ruta donde esta la imagen
        imagen_completa = os.path.join(BASE_DIR, "Imagenes", "Tunel.png")
        #Se abre la carpeta que contiene la imagen
        imagen_pillow = Image.open(imagen_completa).resize((64, 64), Image.LANCZOS)
        # convierte una imagen de PIL a un formato que Tkinter sí puede mostrar en canvas, label, button
        self.imagen = ImageTk.PhotoImage(imagen_pillow)
    
    # Función que permite caminar sobre la celda que es "Tunel"
    def permite_paso_tunel(self):
        return True
##########################################################
class Liana(Terreno):
    
    #Función que carga la imagen de liana del laberinto 
    def __init__(self):
       
        # Se define la ruta donde esta la imagen
        imagen_completa = os.path.join(BASE_DIR, "Imagenes", "Liana.jpg")
        #Se abre la carpeta que contiene la imagen
        imagen_pillow = Image.open(imagen_completa).resize((64, 64), Image.LANCZOS)
         # convierte una imagen de PIL a un formato que Tkinter sí puede mostrar en canvas, label, button
        self.imagen = ImageTk.PhotoImage(imagen_pillow)
        
        
    # Función que permite caminar sobre la celda que es "Liana"
    def permite_paso_liana(self):
        return True
    
##########################################################
# Clases  que contiene el mapa del juego 

class MapaJuego:
    
    # Valores de la matriz 
        # 0 = camino
        # 1 = muro
        # 2  = Tunel
        # 3 = Liana 

    def __init__(self, canvas_juego):
        
        # Ajusta el tamaño del mapa al canvas 
        self.canvas_juego = canvas_juego

        # Tamaño de cada celda en el laberint 
        self.tamano_celda = 64
        

    #Función que genera mapas aleatorios       
    def generar_mapas_aleatorios(self):
        
        #Se actualiza el tamaño real del canvas antes de usarlo.
        self.canvas_juego.update() 
        
        
        # Se determina el tamño del canvas laberinto 
        ancho_canvas_laberinto = self.canvas_juego.winfo_width()
        alto_canvas_laberinto  = self.canvas_juego.winfo_height()
        
        # Se convierte los pixeles del laberinto a celdas (cuadrantes)
        cantidad_columnas_laberinto = ancho_canvas_laberinto// self.tamano_celda
        cantidad_filas_laberinto  = alto_canvas_laberinto  // self.tamano_celda
        
        #Creación de matriz (inicialmente solo con muros =1)
        matriz = [] 
        for i in range(cantidad_filas_laberinto):
            fila = []
            for j in range(cantidad_columnas_laberinto):
                fila.append(1)  # 1 = Muro
            matriz.append(fila) # Se agrega la fila completa a la matriz 


    # Creación de varias salidas en el laberinto 
        
        # Cantidad de salidas que se tendrá en cada lado del laberinto 
        cantidad_salidas_por_borde = 2
#######
        
        # Creación de salidas al lado izquierdo del laberinto 
        for numero_de_salida in range(cantidad_salidas_por_borde):

            # Selección de  fila aleatoria, sin usar la primera ni la última
            fila_elegida = random.randint(1, cantidad_filas_laberinto- 2)

            # La salida siempre está en la primera columna (columna 0) porque es el borde del laberinto 
            columna_izquierda = 0

            # Se cambia el valor de la celda que inicialmente están en 1 a 0 (salida del laberinto)
            matriz[fila_elegida][columna_izquierda] = 0
            
#######            
        #Creación de salidas al lado derecho del laberinto 
        for numero_de_salida in range(cantidad_salidas_por_borde):

            fila_elegida = random.randint(1, cantidad_filas_laberinto - 2)

            #Como el indice incia en 0 y no en 1 para que no provoque el out of index se le resta 1 a la fila (columna final del laberinto)
            columna_derecha = cantidad_columnas_laberinto - 1  

            # Se cambia el valor de la celda que inicialmente están en 1 a 0 (salida del laberinto)
            matriz[fila_elegida][columna_derecha] = 0
#######
            
        # Creación de salida en la parte superior del laberinto 

        #Se selecciona una columna (superior) al azar para que sea una salida 
        columna_aleatoria_superior = random.randint(1, cantidad_columnas_laberinto - 2)
            
        # Se asgina el valor de la fila superior en 0 para que pueda salir del laberinto 
        fila_superior = 0

        # Se cambia el valor de la celda que inicialmente están en 1 a 0 (salida del laberinto)
        matriz[fila_superior][columna_aleatoria_superior] = 0
#######

        # Creación de salida en la parte inferior del laberinto 

         #Se selecciona una columna (inferior) al azar para que sea una salida 
        columna_aleatoria_inferior = random.randint(1, cantidad_columnas_laberinto - 2)
        
        #Como el indice incia en 0 y no en 1 para que no provoque el out of index se le resta 1 a la fila 
        fila_inferior = cantidad_filas_laberinto - 1

        # Se cambia el valor de la celda que inicialmente están en 1 a 0 (salida del laberinto)
        matriz[fila_inferior][columna_aleatoria_inferior] = 0
        
#######
        # Se rellena el laberinto con valores aleatorios (camino,muro,tunel,liana) dejando intacto las salidas del laberinto que se definieron previamente 

        # Se recorre el laberinto (filas) 
        for numero_fila in range(cantidad_filas_laberinto):
            # Se rrecorre el laberinto (columnas)
            for numero_columna in range(cantidad_columnas_laberinto):

                # Se valida que si la celda ya tiene un valor de 0 (camino o salida) y no se modifica 
                es_camino_o_salida = (matriz[numero_fila][numero_columna] == 0)

                # Si es 0 no se hace ninguna modificación (se ocupa que no se toque las salidas o camninos del laberinto)
                if es_camino_o_salida == True:
                    resultado = 0

                # Si NO es 0, se le asigna a la celda un valor aleatorio (camino =0, muro =1, tunel =2 y liana = 3)
                else:
                    nuevo_valor = random.choice([0, 1, 2, 3])

                    # Se reemplaza el valor por defecto de 1 por el nuevo valor
                    matriz[numero_fila][numero_columna] = nuevo_valor
                    
#######  
        # Se convierte la matriz numérica [0,1,2,3] a objetos 

        # Se guarda la nueva matriz ya convertida a objetos
        matriz_de_objetos = []

        # Se rrecore todas las filas de la matriz 
        for numero_fila in matriz:

            # Se crea una nueva fila vacía para almacenar los objetos
            fila_convertida = []

            # Se recorre cada fila de la matriz 
            for valor_celda in numero_fila:

                # Si la celda es 0 → Camino
                if valor_celda == 0:
                    fila_convertida.append(Camino())

                # Si es 1 → Muro
                elif valor_celda == 1:
                    fila_convertida.append(Muro())

                # Si es 2 → Tunel
                elif valor_celda == 2:
                    fila_convertida.append(Tunel())

                # Si es 3 → Liana
                elif valor_celda == 3:
                    fila_convertida.append(Liana())

            # Se agrega la fila convertida a la matriz final
            matriz_de_objetos.append(fila_convertida)

        # Se devuelve la matriz convertida
        return matriz_de_objetos

                        

##########################################################



#Clase que contiene la pantalla principal 
class PantallaPrincipal:

    def __init__(self, pantalla_principal):
        self.pantalla_principal = pantalla_principal
        self.pantalla_principal.title("Escapando del laberinto")
    
    
        ancho_pantalla = self.pantalla_principal.winfo_screenwidth()
        alto_pantalla = self.pantalla_principal.winfo_screenheight()
        
        # Se resta unos píxeles al alto (80 px deja ver la barra de tareas)
        self.pantalla_principal.geometry(f"{ancho_pantalla}x{alto_pantalla - 80}+0+1")
        
        #nuevo_ancho = ancho_pantalla - 20
        #nuevo_alto  = alto_pantalla - 100  # deja espacio para barra y evita fullscreen
        #self.pantalla_principal.geometry(f"{nuevo_ancho}x{nuevo_alto}+10+10")
        #self.pantalla_principal.geometry("1200x700+50+50")
        #self.pantalla_principal.geometry(f"{ancho_pantalla}x{alto_pantalla - 80}+0+0")
        #self.pantalla_principal.geometry(f"{ancho_pantalla}x{alto_pantalla - 80}+0+20")
        
        #nuevo_ancho = int(ancho_pantalla * 0.90)   # 90% del ancho real
        #nuevo_alto  = int(alto_pantalla * 0.85)    # 85% del alto real
        #self.pantalla_principal.geometry(f"{nuevo_ancho}x{nuevo_alto}+50+0")
        
        
        # A la pantalla principal se le asigna un canvas para que pueda colocarse botones 
        self.canvas = Canvas(self.pantalla_principal, 
                             bg="white")
        # self.canvas = Canvas(self.pantalla_principal,
        #              width=500, height=750,  
        #              bg="white")
        
        #Se extiende el canvas al tamaño total de la ventana principal
        self.canvas.pack(fill=tk.BOTH, expand=True)
        #self.canvas.pack()
        
        #Carga el fondo de la pantalla principal solo cuando ya se tiene el tamaño del canvas
        self.pantalla_principal.after(200, self.tamano_pantalla_principal) 
        
        #Se llama a la función que contiene el botón juego y lo coloca en la pantalla principal 
        self.pantalla_principal.after(400, self.boton_juego)
        
        # Hace que el botón jugar se muestre sobre el fondo del canvas 
        self.canvas.tag_raise("boton_jugar")
        

#############################################
#Función que carga la imagen de la pantalla principal 

    def tamano_pantalla_principal(self):
        ruta = os.path.join(BASE_DIR, "Imagenes","Fondo2.jpg")
        imagen = Image.open(ruta)
        
        print(">>> Tamaño ORIGINAL de la imagen:", imagen.size)
        
        #Se actualiza el tamaño real del canvas antes de usarlo.
        self.canvas.update_idletasks()

        # Se obtiene el tamaño real del canvas
        ancho_pantalla_principal = self.canvas.winfo_width()
        alto_pantalla_principal = self.canvas.winfo_height()
        
        print(">>> Tamaño REAL del canvas:", ancho_pantalla_principal, "x", alto_pantalla_principal)

        #Se ajusta la imagen al tamaño de la ventana
        imagen_ajustada = imagen.resize((ancho_pantalla_principal, alto_pantalla_principal), Image.LANCZOS)
        self.fondo = ImageTk.PhotoImage(imagen_ajustada)

        #Mantiene la imagen de fondo y evita que se borre 
        self.canvas.create_image(0, 0, anchor="nw", image=self.fondo)
        
                # Validación del problema
        if imagen.size[1] < alto_pantalla_principal:
            print("⚠ AVISO: El canvas ES MÁS ALTO que la imagen → aparecerá espacio vacío ABAJO.")
        else:
            print("✔ La imagen cubre correctamente el alto del canvas.")

#############################################

    # # Función que determina el tamaño de la ventana 
    # def ajustar_tamano_ventana(self):
        
    #     # Ahora tkinter ya construyó la ventana y los valores son correctos
    #     ancho_real = self.pantalla_principal.winfo_screenwidth()
    #     alto_real = self.pantalla_principal.winfo_screenheight()

    #     # Restamos 80 px para dejar visible la barra de tareas
    #     self.pantalla_principal.geometry(f"{ancho_real}x{alto_real - 80}+0+0")

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
            
             # Guarda el tamaño y posición actuales para reutilizarlos en la ventana de seleccionar el juego 
            self.posicion_nombre = ventana_nombre.geometry()
           
            # Se guarda el nombre del jugador en un archivo TXT 
            with open("JugadoresCHAT.txt", "a") as archivo:
                archivo.write(f"{nombre_jugador},0\n")

            # Cierra la ventana
            ventana_nombre.destroy()

            # Se llama a la venta que permite la selección del juego
            self.ventana_seleccion_juego()
                
            #Creación del botón comenzar (permite seleccionar entre los dos juegos de laberintos)
        boton_comenzar = tk.Button(
                                            ventana_nombre,
                                            text="Comenzar",
                                            bg="SpringGreen4",
                                            fg="black",
                                            command=comenzar_juego)
        boton_comenzar.pack(pady=10)
        

#############################################

    # Función que permite seleccionar entre el juego cazador y el juego escapar 
    
    def ventana_seleccion_juego(self):
        #Toplevel: permite abrir una ventana secundaria sobre la ventana principal (para seleccionar entre los dos juegos) 
        ventana_juegos = tk.Toplevel(self.pantalla_principal)
        
        # Se crea la ventana de juegos 
        self.ventana_juegos = ventana_juegos
        
        # Da el nombre a la ventana de juegos
        ventana_juegos.title("Seleccione el modo de juego")
        
        # Usa el mismo tamaño y posición que tenía la ventana para ingresar el nombre del jugador 
        try:
            ventana_juegos.geometry(self.posicion_nombre)
        except:
            ventana_juegos.geometry("300x200+900+200")
            
        # Se define el tamaño  de la ventana para seleccionar el juego 
        ventana_juegos.resizable(False, False)
        
        # mantiene esta ventana siempre al frente
        ventana_juegos.attributes("-topmost", True)

        # Se coloca una imagen a la pantalla de juegos
        ruta_fondo = os.path.join(BASE_DIR, "Imagenes", "Fondo5.jpg")
        imagen_fondo = Image.open(ruta_fondo)
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo.resize((300, 200), Image.LANCZOS))

        # Se crea un Label para mostrar la imagen de fondo
        label_fondo = Label(ventana_juegos, image=imagen_fondo_tk)
        
        # Se coloca el laberl para que ocupe todo el fondo de la ventana
        label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        
        #Mantiene la imagen en memoria
        label_fondo.imagen_fondo = imagen_fondo_tk

##################
        # Creación de botón que permitirá acceder al juego "Cazador"
        
        #Se indica donde esta la ruta que contendra la imagen del botón 
        ruta_cazador = os.path.join(BASE_DIR, "Imagenes", "Cazador.png")
        
        # se abre la carpeta que contiene la imagen del boton 
        img_cazador = Image.open(ruta_cazador)
        
        # Se ajusta el tamaño de la imagen del botón 
        img_cazador_tk = ImageTk.PhotoImage(img_cazador.resize((100, 50), Image.LANCZOS))

        boton_cazador = tk.Button(
                                    ventana_juegos,
                                    image=img_cazador_tk,
                                    borderwidth=0,
                                    relief="flat",
                                    cursor="hand2",
                                    command=self.canvas_juego_cazador   #Se llama a la función que contiene el juego de "Cazador"
                                )
        boton_cazador.image = img_cazador_tk  # evita el borrado de la imagen 
        #boton_cazador.pack(pady=10)
        # Se le da ubicación al botón 
        boton_cazador.place(x=20, y=40)

#################
        #Creación de botón que permitirá acceder al juego "Escapar"
        
        #Se indica donde esta la ruta que contendra la imagen del botón 
        ruta_escapar = os.path.join(BASE_DIR, "Imagenes", "Escapar.png")
        
        # se abre la carpeta que contiene la imagen del boton 
        img_escapar = Image.open(ruta_escapar)
        
         # Se ajusta el tamaño de la imagen del botón 
        img_escapar_tk = ImageTk.PhotoImage(img_escapar.resize((100, 50), Image.LANCZOS))

        boton_escapar = tk.Button(
                                ventana_juegos,
                                image=img_escapar_tk,
                                borderwidth=0,
                                relief="flat",
                                cursor="hand2",
                                command=self.canvas_juego_escapar   #Se llama a la función que contiene el juego de "Escapar"
                                )
        boton_escapar.image = img_escapar_tk # evita el borrado de la imagen 
        #boton_escapar.pack(pady=5)
        # Se le da ubicación al botón 
        boton_escapar.place(x=20, y=100)
        
 ##################################################################
 
    # Función que crea el canvas donde se colocará la matriz del juego cazador 
    def canvas_juego_cazador(self):
        
            # Se cierra la ventana de selección del juego
            if hasattr(self, "ventana_juegos"):
                self.ventana_juegos.destroy()
                
                
            #Toplevel: permite abrir una ventana secundaria sobre la ventana del juego "Cazador"
            ventana_cazador = tk.Toplevel(self.pantalla_principal)
            
            # Da el nombre a la ventana del juego Cazador 
            ventana_cazador.title("Modo Cazador")

            #Se define el tamaño  de la ventana del juego cazador 
            #ventana_cazador.geometry("300x200+900+200")
            ventana_cazador.geometry(self.pantalla_principal.geometry())
            
            # Evita que se pueda aumentar o disminuir el tamaño de la ventana 
            ventana_cazador.resizable(False, False)

            # Creación del canvas donde se dibujará el laberinto del juego cazador 
            self.canvas_cazador = tk.Canvas(
                                                ventana_cazador,
                                                width=800,
                                                height=600,
                                                bg="black"      #
                                            )
            # Se actualiza el canvas para saber su tamaño antes de dibujar las filas y columnas
            self.canvas_cazador.pack(fill="both", expand=True)
            self.canvas_cazador.update() 

            # Mensaje en consola para confirmar que se abrió correctamente
            print("Juego Cazador iniciado: canvas creado")
            
            # A la variable laberinto se le asigna la clase MapaJuego (que define el tamaño de las celdas, la creación del mapa aleatorio y las entradas y salidas del laberinto)
             # self.canvas_cazador: Hace que la clase MapaJuego tome el tamaño del canvas que esta definido para el juego de cazador 
            laberinto = MapaJuego(self.canvas_cazador)
            
            # De la clase "MapaJuego" se llama a la función "generar_mapas_aleatorios" que retorna una matriz de objetos  
    
                #[[Camino(), Muro(), Liana()],
                # [Tunel(), Camino(), Muro()],
                #[Liana(), Liana(), Camino()]]
            
            matriz_diferentes_terrenos = laberinto.generar_mapas_aleatorios()
            
            # Se guarda la matriz del laberinto dentro de la clase
            self.matriz_terrenos_cazador = matriz_diferentes_terrenos      

            # Tamaño de cada celda del laberinto 
            tamano_celda = 64
            
#############
            # Se dibuja el laberinto 
            
            # Mantiene vivas la imagenes del laberinto en memoria para que no sean borradas por tkinter 
            self.imagenes_terreno_guardadas = []  

            # Se rrecorre las filas del laberinto 
            for fila in range(len(matriz_diferentes_terrenos)):
                 # Se corrre las columnas del laberinto 
                for columna in range(len(matriz_diferentes_terrenos[0])):

                    terreno = matriz_diferentes_terrenos[fila][columna]

                    # Guarda la referencia para que no sea borrada por Tkinter 
                    self.imagenes_terreno_guardadas.append(terreno.imagen)

                    self.canvas_cazador.create_image(
                                                        columna * tamano_celda,
                                                        fila * tamano_celda,
                                                        image=terreno.imagen,
                                                        anchor="nw"
                                                    )

            print("✔ Laberinto dibujado correctamente.")
            

 ##################################################################
 
    # Función que permite mover al jugador usando las teclas de direcciones 
    def mueve_cazador(self, event):
        
        # Evento que le permite al juego saber cual tecla esta presionando el jugador 
        tecla = event.keysym

        if tecla == "Up":
            self.cazador.cambiar_direccion("arriba")
            self.cazador.mover(0, -1)

        elif tecla == "Down":
            self.cazador.cambiar_direccion("abajo")
            self.cazador.mover(0, +1)

        elif tecla == "Left":
            self.cazador.cambiar_direccion("izquierda")
            self.cazador.mover(-1, 0)

        elif tecla == "Right":
            self.cazador.cambiar_direccion("derecha")
            self.cazador.mover(+1, 0)
            
        #Actualiza la imagen del jugador conforme se presione la tecla de dirección 
        self.canvas_cazador.itemconfig(
                                        self.self.cazador.imagen_id,
                                        image=self.cazador.img[self.cazador.direccion]
                                    )

 ##################################################################
    def canvas_juego_escapar(self):
            messagebox.showinfo("Escapar", "El modo Escapar aún no está implementado.")
            print("Juego Escapar iniciado")
 
        
 ###############################################
    # Creación de clase para el juego CAZADOR
 ###############################################
 
class Cazador:
    def __init__(self, posicion_inicial_cazador_ejex , posicion_inicial_cazador_eje, canvas_juego, mapa_terrenos):

            # Tamaño de cada celda del laberinto 
            tamano_celda = 64
            
            # Posición inicial del cazador dentro de la matriz
            self.posicion_inicial_cazador_ejex = posicion_inicial_cazador_ejex        # posición en la columna
            self.posicion_inicial_cazador_ejey = posicion_inicial_cazador_eje       # posición en la fila

            # Referencia al canvas donde se dibuja el personaje
            self.canvas_juego = canvas_juego

            # Referencia a la matriz de terrenos (camino/muro/etc.)
            self.mapa_terrenos = mapa_terrenos

            # Dirección inicial del cazador en el laberinto 
            self.direccion_actual = "abajo"

        
############        
        # Función que carga las imagenes del cazador en diferentes direcciones     
    def cargar_imagenes_cazador(self):
            
            ruta_cazador_arriba = os.path.join("Imagenes", "cazador_arriba.png")
            ruta_cazador_abajo = os.path.join("Imagenes", "cazador_abajo.png")
            ruta_cazador_izquierda = os.path.join("Imagenes", "cazador_izquierda.png")
            ruta_cazador_derecha = os.path.join("Imagenes", "cazador_derecha.png")

            self.imagen_cazador_arriba = ImageTk.PhotoImage(Image.open(ruta_cazador_arriba).resize((64, 64), Image.LANCZOS))
            self.imagen_cazador_abajo = ImageTk.PhotoImage(Image.open(ruta_cazador_abajo).resize((64, 64), Image.LANCZOS))
            self.imagen_cazador_izquierda = ImageTk.PhotoImage(Image.open(ruta_cazador_izquierda).resize((64, 64), Image.LANCZOS))
            self.imagen_cazador_derecha = ImageTk.PhotoImage(Image.open(ruta_cazador_derecha).resize((64, 64), Image.LANCZOS))

            print(" Las imágenes del cazador cargadas correctamente.")

        
        
 ###############################################
    # Clase del juego ESCAPAR
 ###############################################
 


    