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

class Salida(Terreno):

    # Función que coloca las imagenes de salida del laberinto 
    def __init__(self):
        imagen_salida = os.path.join(BASE_DIR, "Imagenes", "Exit.jpg")
        imagen_pillow = Image.open(imagen_salida).resize((64, 64), Image.LANCZOS)
        self.imagen = ImageTk.PhotoImage(imagen_pillow)

    def permite_paso_salida(self):
        return True

#########################################################
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

        # Tamaño de cada celda en el laberinto 
        self.tamano_celda = 64
        
        self.columnas_fijas = None
        self.filas_fijas = None
        
#################################
        
    # Función que genera los mapas aleatorios 
    def generar_mapas_aleatorios(self):

        # Se actualiza el canvas que contiene el laberinto 
        self.canvas_juego.update()
        self.canvas_juego.update_idletasks()

        # Se obtiene el tamaño del canvas (laberinto)
        ancho_canvas_laberinto = self.canvas_juego.winfo_width()
        alto_canvas_laberinto  = self.canvas_juego.winfo_height()

        # El tamaño de cada celda es de 64 pixeles 
        if ancho_canvas_laberinto < 64 or alto_canvas_laberinto < 64:
            print("El canvas aún no tiene tamaño suficiente.")
            return None

        # Se determina número de filas y columnas que tendrá el laberinto 
        if self.columnas_fijas is not None:
            cantidad_columnas_laberinto = self.columnas_fijas
        else:
            cantidad_columnas_laberinto = ancho_canvas_laberinto // self.tamano_celda

        if self.filas_fijas is not None:
            cantidad_filas_laberinto = self.filas_fijas
        else:
            cantidad_filas_laberinto = alto_canvas_laberinto // self.tamano_celda

        # Inicialmente se crea la matriz del laberinto lleno de 1 (Muro)
         # Evita que existan valores aleatorios que impida generar salidas o caminos 
        matriz = []
        for i in range(cantidad_filas_laberinto):
            fila = []
            for j in range(cantidad_columnas_laberinto):
                fila.append(1)  # 1 = muro
            matriz.append(fila)
            
#################################
        #Se crean las salidas del laberinto (arriba, abajo, izquierda o derecha)
        cantidad_salidas_por_borde = 2

        # Salidas izquierda
         # se coloca -2 para no usar ni la primer fila ni la última columna 
         # random.randint= genera un número entero aleatorio entre a y b
        for _ in range(cantidad_salidas_por_borde):
            fila_elegida = random.randint(1, cantidad_filas_laberinto - 2)
            matriz[fila_elegida][0] = 4  # posición #4 = salida

        # Salidas derecha
        for _ in range(cantidad_salidas_por_borde):
            #se coloca -2 para no usar ni la primer fila ni la última columna 
            # random.randint= genera un número entero aleatorio entre a y b
            fila_elegida = random.randint(1, cantidad_filas_laberinto - 2)
            matriz[fila_elegida][cantidad_columnas_laberinto - 1] = 4 # posición #4 = salida

        # Salida arriba
        columna_superior = random.randint(1, cantidad_columnas_laberinto - 2)
        matriz[0][columna_superior] = 4 # posición #4 = salida

        # Salida abajo
        columna_inferior = random.randint(1, cantidad_columnas_laberinto - 2)
        matriz[cantidad_filas_laberinto - 1][columna_inferior] = 4 # posición #4 = salida

#################################
        # Creación del camino en el laberinto (no esta obstruido por valores aleatorios)

        # Se toma la fila central del laberinto 
        fila_central = cantidad_filas_laberinto // 2

        # Se crea la fila horizontal (camino) sin interrupciones 
        for c in range(cantidad_columnas_laberinto):
            matriz[fila_central][c] = 0  # posición #0 = camino
            
#################################
        # Conexión entre la salidas y el camino central (sin obstrucciones)

            # Se rrecorre todas las filas y columnas del laberinto para encontrar las salidas (=4) 
        for fila in range(cantidad_filas_laberinto):
            for columna in range(cantidad_columnas_laberinto):

                # Se evalúa si la posición del laberinto es una salida = 4
                if matriz[fila][columna] == 4:  # posición #4 = salida

                    # Si la salida que se genera de forma aleatoria aparece en una posición diferente al camino 
                    if fila < fila_central:
                        # La salida está arriba del camino, hay que bajar
                        paso = 1
                    else:
                        # La salida está abajo del camino, hay que subir
                        paso = -1

                    fila_actual = fila

                    # Crear camino vertical desde la salida hacia el camino central
                    while fila_actual != fila_central:
                        fila_actual += paso
                        matriz[fila_actual][columna] = 0  # posición #0 = camino

#################################

        # Se completa el laberinto que no es camino con valores aleatorios (muro, tunel o liana)  
        for fila in range(cantidad_filas_laberinto):
            for columna in range(cantidad_columnas_laberinto):

                # Si el valor de la matriz es 0 (salida) o 4 (salida) No se debe modificar caminos ni salidas
                if matriz[fila][columna] == 0 or matriz[fila][columna] == 4:
                    continue

                matriz[fila][columna] = random.choice([1, 2, 3])
                # 1 = muro
                # 2 = tunel
                # 3 = liana
                
#################################
        # Se convierte los números de la matriz a objetos 
         # Se utilizará más adelante para definir si es un jugador cazador o jugador escapar puede moverse o no a traves del laberinto 

        matriz_de_objetos = []

        for fila_numerica in matriz:
            fila_convertida = []

            for valor_celda in fila_numerica:
                # 0 = camino
                # 1 = muro
                # 2 = tunel
                # 3 = liana
                # 4 = salida 
                
                if valor_celda == 0:
                    fila_convertida.append(Camino())
                elif valor_celda == 1:
                    fila_convertida.append(Muro())
                elif valor_celda == 2:
                    fila_convertida.append(Tunel())
                elif valor_celda == 3:
                    fila_convertida.append(Liana())
                elif valor_celda == 4:
                    fila_convertida.append(Salida())

            matriz_de_objetos.append(fila_convertida)

        # Retornar matriz lista
        return matriz_de_objetos

##########################################################

class PantallaPrincipal:
    
    # Función que definirá el tamaño de la pantalla principal del juego 
    def __init__(self, pantalla_principal):
        
        self.pantalla_principal = pantalla_principal
        
        # Se le da nombre a la pantalla principal del juego 
        self.pantalla_principal.title("Escapando o canzando en el laberinto")

        # Se crea un canvas del tamaño actual de la ventana
        ancho = self.pantalla_principal.winfo_width()
        alto = self.pantalla_principal.winfo_height()

        self.canvas = Canvas(
                                self.pantalla_principal,
                                width=ancho,
                                height=alto,
                                bg="white"
                            )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        #Carga el fondo de la pantalla principal solo cuando ya se tiene el tamaño del canvas
        self.pantalla_principal.after(200, self.tamano_pantalla_principal)
        
        #Se llama a la función que contiene el botón juego y lo coloca en la pantalla principal luego de 400 milisegundos
        self.pantalla_principal.after(400, self.boton_juego)

         # Hace que el botón jugar se muestre sobre el fondo del canvas 
        self.canvas.tag_raise("boton_jugar")

##########################################################

    #Función que carga la imagen de la pantalla principal 
    def tamano_pantalla_principal(self):
        
        # Ruta donde se encuentra la imagen de fondo de la pantalla principal 
        ruta = os.path.join(BASE_DIR, "Imagenes", "Fondo2.jpg")
       
        # Se abre la carpeta donde esta guardada la imagen 
        imagen = Image.open(ruta)

        #Se actualiza el tamaño real del canvas antes de usarlo.
        self.canvas.update_idletasks()
        
        # Se obtiene el tamaño real del canvas
        ancho_canvas = self.canvas.winfo_width()
        alto_canvas  = self.canvas.winfo_height()

        print(">>> Tamaño REAL canvas:", ancho_canvas, "x", alto_canvas)

        #Se ajusta la imagen al tamaño de la ventana
        imagen_ajustada = imagen.resize((ancho_canvas, alto_canvas), Image.LANCZOS)
        self.fondo = ImageTk.PhotoImage(imagen_ajustada)

        #Mantiene la imagen de fondo y evita que se borre 
        self.canvas.create_image(0, 0, anchor="nw", image=self.fondo)

        if imagen.size[1] < alto_canvas:
            print("El canvas es MÁS ALTO que la imagen → aparecerá espacio vacío.")

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
        ruta_fondo = os.path.join(BASE_DIR, "Imagenes", "Fondo6.jpg")
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

    # Funcionalidad que define el canvas del juego cazador 
    def canvas_juego_cazador(self):

        # Si esta abierta la ventana de selección, se cierra
        if hasattr(self, "ventana_juegos"):
            self.ventana_juegos.destroy()

        # Se crea ventana del modo cazador
        ventana_cazador = tk.Toplevel(self.pantalla_principal)
        ventana_cazador.title("Modo Cazador")

        # Actualiza la ventana que contiene el juego cazador
        ventana_cazador.update_idletasks()

        # Se obtiene el ancho y alto de la pantalla del  juego
        Ancho_pantalla = ventana_cazador.winfo_screenwidth()
        Alto_pantalla = ventana_cazador.winfo_screenheight()  # ← pantalla completa

        # Restar al tamaño de la pantalla del juego un margen para ver la bara de tareas 
        Margen_barra_tareas = 90     # Se puede incrementar o reducir el tamaño que se deje en la parte inferior de la pantalla 

        Alto_usable = Alto_pantalla - Margen_barra_tareas

        tamano_celda = 64

        # Se calcula cuantas celdas se necesita para cubrir la pantalla del laberinto 
        columnas = Ancho_pantalla // tamano_celda
        filas    = Alto_usable     // tamano_celda

        print(f"Filas generadas: {filas}, Columnas generadas: {columnas}")

#########
        # Se ajusa el laberinto al tamaño de la venta 
        ancho_final = columnas * tamano_celda
        alto_final  = filas    * tamano_celda

        ventana_cazador.geometry(f"{ancho_final}x{alto_final}+0+0")
        ventana_cazador.resizable(False, False)

#########
        # Se ajusta el tamaño del canvas al laberinto 
        self.canvas_cazador = tk.Canvas(
                                            ventana_cazador,
                                            width=ancho_final,
                                            height=alto_final,
                                            bg="black"
                                        )
        self.canvas_cazador.pack()

#########
        # Se genera un laberinto ajustado al tamaño a la pantalla de juego 
        laberinto = MapaJuego(self.canvas_cazador)

        # Ajuste manual: forzar dimensiones dentro del mapa
        laberinto.columnas_fijas = columnas
        laberinto.filas_fijas    = filas

        matriz_diferentes_terrenos = laberinto.generar_mapas_aleatorios()
        self.matriz_terrenos_cazador = matriz_diferentes_terrenos      

        # Guardar imágenes
        self.imagenes_terreno_guardadas = []

#########
        # Se dibuja el laberinto 
        for fila in range(filas):
            for columna in range(columnas):

                terreno = matriz_diferentes_terrenos[fila][columna]
                self.imagenes_terreno_guardadas.append(terreno.imagen)

                self.canvas_cazador.create_image(
                    columna * tamano_celda,
                    fila    * tamano_celda,
                    image=terreno.imagen,
                    anchor="nw"
                )

        print(" Laberinto dibujado a pantalla completa (con barra de tareas visible).")
        
        # Posición inicial del cazador (se llama a la función buscar_casilla_valida_jugador que valida que el jugador pueda moverse al iniciar el juego)
        posicion_inicial_jugador_ejex, posicion_inicial_jugador_ejey = self.buscar_casilla_valida_jugador()

        # Se guarda la posición REAL del cazador
        self.posicion_inicial_cazador_ejey = posicion_inicial_jugador_ejey  
        self.posicion_inicial_cazador_ejex = posicion_inicial_jugador_ejex

        # Se crea al jugador cazador  
        self.cazador = Cazador(
                                posicion_inicial_jugador_ejex,
                                posicion_inicial_jugador_ejey,
                                self.canvas_cazador,
                                self.matriz_terrenos_cazador
                                 )
        
        
        # Activar movimiento del jugador en el teclado 
        self.canvas_cazador.focus_set()
        self.canvas_cazador.bind("<KeyPress>", self.mueve_cazador)

        print("Cazador colocado en pantalla.")
        
        # Se Crea el enemigo #1 del juego cazador
        
        pos_enemigo1_x, pos_enemigo1_y = self.buscar_casilla_valida_jugador()

        # Crear enemigo 1
        self.enemigo1 = enemigoscazador1(
                                        self.canvas_cazador,
                                        self.matriz_terrenos_cazador
                                        ) 
        
        #se le asinga al enemigo la posición real del cazador 
        self.enemigo1.posicion_inicial_cazador_ejey = self.posicion_inicial_cazador_ejey
        self.enemigo1.posicion_inicial_cazador_ejex = self.posicion_inicial_cazador_ejex

        #Se llama a la función que mueve el enemigo 
        self.enemigo1.mover_enemigo1()



 ##################################################################
 
    # Función que permite mover al jugador usando las teclas de direcciones 
    def mueve_cazador(self, event):
        
        # Evento que le permite al juego saber cual tecla esta presionando el jugador 
        tecla = event.keysym

        if tecla == "Up":
            self.cazador.cambia_direccion_jugador("arriba")
            self.cazador.mover_jugador_cazador(0, -1)

        elif tecla == "Down":
            self.cazador.cambia_direccion_jugador("abajo")
            self.cazador.mover_jugador_cazador(0, +1)

        elif tecla == "Left":
            self.cazador.cambia_direccion_jugador("izquierda")
            self.cazador.mover_jugador_cazador(-1, 0)

        elif tecla == "Right":
            self.cazador.cambia_direccion_jugador("derecha")
            self.cazador.mover_jugador_cazador(+1, 0)
            
        
 ##################################################################  
 
    # Función que valida que el jugador aparezca de forma aleatoria en una posición que le sea válida para moverse  
    def celda_para_mover_jugador(self, fila, columna):

        # Toma la celda donde se quiere colocar el jugador
        celda_actual = self.matriz_terrenos_cazador[fila][columna]

        # Se valida que el jugador aparezca en una posición válida (camino o tunel) de manera tal que le permita moverse 
        if not isinstance(celda_actual, Camino) and not isinstance(celda_actual, Tunel):
            return False  # Si aparece en liana o muro, NO sirve la ubicación debe elegirse otra 

        # Se obtiene el tamaño del laberinto 
        total_filas = len(self.matriz_terrenos_cazador)
        total_columnas = len(self.matriz_terrenos_cazador[0])
        
#########
        # Se valida que el jugador pueda moverse al menos un espacio hacia arriba
        if fila - 1 >= 0:
            # Se determina la posición de la celda superior 
            celda_arriba = self.matriz_terrenos_cazador[fila - 1][columna]
            # Se evalúa si la celda es válida para moverse 
            if isinstance(celda_arriba, Camino) or isinstance(celda_arriba, Salida) or isinstance(celda_arriba, Tunel):
                return True
            
#########
        #Se valida que el jugador pueda moverse al menos un espacio hacia abajo
        if fila + 1 < total_filas:
            # Se determina la posición de la celda de abajo
            celda_abajo = self.matriz_terrenos_cazador[fila + 1][columna]
            # Se evalúa si la celda es válida para moverse 
            if isinstance(celda_abajo, Camino) or isinstance(celda_abajo, Salida) or isinstance(celda_abajo, Tunel):
                return True
            
#########
        #Se valida que el jugador pueda moverse al menos un espacio hacia la izquierda
        if columna - 1 >= 0:
            # Se determina la posición de la celda izquierda
            celda_izq = self.matriz_terrenos_cazador[fila][columna - 1]
            # Se evalúa si la celda es válida para moverse 
            if isinstance(celda_izq, Camino) or isinstance(celda_izq, Salida) or isinstance(celda_izq, Tunel):
                return True
#########

        ##Se valida que el jugador pueda moverse al menos un espacio hacia la derecha
        if columna + 1 < total_columnas:
            # Se determina la posición de la celda derecha 
            celda_der = self.matriz_terrenos_cazador[fila][columna + 1]
            # Se evalúa si la celda es válida para moverse 
            if isinstance(celda_der, Camino) or isinstance(celda_der, Salida) or isinstance(celda_der, Tunel):
                return True

        # Si no encontró salida, se está atrapado y se busca otra posición para colocar al jugador 
        return False

 ##################################################################    
    
    # #Función que valida el lugar en el que se coloca  el jugador (solo lo coloca si es una posición válida para moverse) 
    def buscar_casilla_valida_jugador(self):

        # Se obtiene la cantidad de filas y columnas del laberinto 
        filas = len(self.matriz_terrenos_cazador)
        columnas = len(self.matriz_terrenos_cazador[0])

        # Se valida hasta que encuentre una posición válida aleatoria (True) que permita mover el jugador 
        while True:
            fila = random.randint(1, filas - 2)
            columna = random.randint(1, columnas - 2)

            celda_actual = self.matriz_terrenos_cazador[fila][columna]

            # Si el jugador no aparece en el camino se vuelve a intentar colocarlo en otra posición 
            if not isinstance(celda_actual, Camino):
                continue   

            # Se revia las 4 posiciones alrededor del jugador y valida que al menos una de ellas permite el movimiento del jugador
            vecinos = [
                        (fila - 1, columna),
                        (fila + 1, columna),
                        (fila, columna - 1),
                        (fila, columna + 1)
                    ]

            movilidad = False

            for fila_vecina, columna_vecina in vecinos:
                if 0 <= fila_vecina < filas and 0 <= columna_vecina < columnas:
                    celda_vecina = self.matriz_terrenos_cazador[fila_vecina][columna_vecina]

                    # El jugador solo puede caminar en "camino" o "salida"
                    if isinstance(celda_vecina, Camino) or isinstance(celda_vecina, Salida):
                        movilidad = True
                        break

            if movilidad:
                return columna, fila
    
##################################################################
 
####################################################################
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
            
            # Se llama a la función que tiene las imagenes del cazador (arriba, abajo, izquierda y derecha) 
            self.cargar_imagenes_cazador()
            
            # Define que la imagen inicial del jugador estará en la posición  hacia"abajo"
            self.imagen_actual = self.imagen_cazador_abajo
            
            # Se convierte la posición del jugador en el laberinto (fila, columna) a pixeles 
            posicion_ejex_pixeles= self.posicion_inicial_cazador_ejex *tamano_celda
            posicion_ejey_pixeles = self.posicion_inicial_cazador_ejey * tamano_celda
            
            #Coloca al jugador en el mapa 
            self.cazador_objeto = self.canvas_juego.create_image(
                                                                    posicion_ejex_pixeles,
                                                                    posicion_ejey_pixeles,
                                                                    anchor="nw",
                                                                    image=self.imagen_actual
                                                                )

            print("Cazador creado en:", self.posicion_inicial_cazador_ejex, self.posicion_inicial_cazador_ejey)
            
              
 ###############################################      
        # Función que carga las imagenes del cazador en diferentes direcciones     
    def cargar_imagenes_cazador(self):
            
            ruta_cazador_arriba = os.path.join("Imagenes", "jugador_arriba.png")
            ruta_cazador_abajo = os.path.join("Imagenes", "jugador_abajo.png")
            ruta_cazador_izquierda = os.path.join("Imagenes", "jugador_izquierda.png")
            ruta_cazador_derecha = os.path.join("Imagenes", "jugador_derecha.png")

            self.imagen_cazador_arriba = ImageTk.PhotoImage(Image.open(ruta_cazador_arriba).resize((64, 64), Image.LANCZOS))
            self.imagen_cazador_abajo = ImageTk.PhotoImage(Image.open(ruta_cazador_abajo).resize((64, 64), Image.LANCZOS))
            self.imagen_cazador_izquierda = ImageTk.PhotoImage(Image.open(ruta_cazador_izquierda).resize((64, 64), Image.LANCZOS))
            self.imagen_cazador_derecha = ImageTk.PhotoImage(Image.open(ruta_cazador_derecha).resize((64, 64), Image.LANCZOS))

            print(" Las imágenes del cazador cargadas correctamente.")

 ############################################### 
    
    #Función que permite cambiar de dirección del jugador 
    
    def cambia_direccion_jugador(self, nueva_direccion):

        # Guarda la dirección actual
        self.direccion_actual = nueva_direccion

        # Cambia la dirección del jugador hacia arriba 
        if nueva_direccion == "arriba":
            self.imagen_actual = self.imagen_cazador_arriba

        # Cambia la dirección del jugador hacia abajo
        elif nueva_direccion == "abajo":
            self.imagen_actual = self.imagen_cazador_abajo

        # Cambia la dirección del jugador hacia la izquierda
        elif nueva_direccion == "izquierda":
            self.imagen_actual = self.imagen_cazador_izquierda

        # Cambia la dirección del jugador hacia la derecha
        elif nueva_direccion == "derecha":
            self.imagen_actual = self.imagen_cazador_derecha

        # Actualiza la imagen mostrada en pantalla
        self.canvas_juego.itemconfig(self.cazador_objeto, image=self.imagen_actual)
        
 ###############################################
    # Función que valida si el cazador se puede o no mover en el laberinto 
     
    def cazador_puede_pasar(self, celda):

        # Si la celda es un muro el jugador - cazador no puede pasar 
        if isinstance(celda, Muro):
            return False  
        
        # Si la celda es una liana el jugador - cazador no puede pasar 
        if isinstance(celda, Liana):
            return False

        # Si la celda es un tunel el jugador - cazador puede pasar 
        if isinstance(celda, Tunel):
            return True 
        
        # Si la celda es un camnioi el jugador - cazador puede pasar
        if isinstance(celda, Camino):
            return True
        
        # Si la celda es la salida el jugador - cazador puede pasar
        if isinstance(celda, Salida):
            return True

        # Si la celda es un camino, liana y Salida si puede pasar 
        return False       
 ###############################################
    # Función que permite el movimiento del jugador - cazador 
    
    def mover_jugador_cazador(self, movimiento_jugador_ejex, movimiento_jugador_ejey):

        # Se determina la posición actual del jugador en el laberinto 
        columna_actual = self.posicion_inicial_cazador_ejex
        fila_actual    = self.posicion_inicial_cazador_ejey

        nueva_columna = columna_actual + movimiento_jugador_ejex
        nueva_fila    = fila_actual + movimiento_jugador_ejey

        # Se define la cantidad de filas y columnas del laberinto 
        total_filas    = len(self.mapa_terrenos)
        total_columnas = len(self.mapa_terrenos[0])

        # Validaciones de borde si son negativos o mayores a la cantidad de filas y columnas detiene el movimiento con un return vacío 
        if nueva_fila < 0:
            return
        if nueva_fila >= total_filas:
            return
        if nueva_columna < 0:
            return
        if nueva_columna >= total_columnas:
            return

        # Determina el movimiento del jugador en el tablero 
        celda_destino = self.mapa_terrenos[nueva_fila][nueva_columna]

        # Si el jugador quiera pasar encima de un muro, salida o un tunel detiene el movimiento con un retrun vacío 
        if not self.cazador_puede_pasar(celda_destino):
            return

        # Actualizar posición en la matriz
        self.posicion_inicial_cazador_ejex = nueva_columna
        self.posicion_inicial_cazador_ejey = nueva_fila

        # Se define el tamaño de la celda 
        tamano_celda = 64
        
        # Convertir a pixeles la posición de la fila y columna que tiene el jugador - cazador en el laberinto 
        nueva_posicion_x = nueva_columna * tamano_celda
        nueva_posicion_y = nueva_fila    * tamano_celda

        # Mover sprite
        self.canvas_juego.coords(
                                    self.cazador_objeto,
                                    nueva_posicion_x,
                                    nueva_posicion_y
                                )
 ###############################################
    # Clase que contiene a los enemigos del juego - cazador
 ###############################################

class enemigoscazador1: 
     
    def __init__(self,canvas_juego, mapa_terrenos):

            # Referencia al canvas donde se dibuja el laberinto
            self.canvas_juego = canvas_juego
            
            # Referencia al mapa del laberinto  (camino/muro/salida/liana)
            self.mapa_terrenos_cazador = mapa_terrenos
            self.mapa_terrenos = mapa_terrenos
            
            # Tamaño de cada celda del laberinto 
            self.tamano_celda = 64
            
            #Se crea una posición inicial para cada enemigo 
            columna_enemigo1, fila_enemigo1 = self.buscar_posicion_inicial_enemigo()
            columna_enemigo2, fila_enemigo2 = self.buscar_posicion_inicial_enemigo()
            columna_enemigo3, fila_enemigo3 = self.buscar_posicion_inicial_enemigo()

            self.posicion_inicial_enemigo1_ejex = columna_enemigo1
            self.posicion_inicial_enemigo1_ejey = fila_enemigo1

            self.posicion_inicial_enemigo2_ejex = columna_enemigo2
            self.posicion_inicial_enemigo2_ejey = fila_enemigo2

            self.posicion_inicial_enemigo3_ejex = columna_enemigo3
            self.posicion_inicial_enemigo3_ejey = fila_enemigo3
            
            #Se define la posición inicial del cazador por defecto en None 
            self.posicion_inicial_cazador_ejex = None
            self.posicion_inicial_cazador_ejey = None
    
            
            # # Posición inicial del enemigo en la matriz
            # self.posicion_inicial_enemigo1_ejey = 0
            # self.posicion_inicial_enemigo1_ejex = 0 

            # # se llama a la función que busca la posición inicial válida para colocar al enemigo 
            # columna_valida, fila_valida = self.buscar_posicion_inicial_enemigo()
            # self.posicion_inicial_enemigo1_ejex = columna_valida
            # self.posicion_inicial_enemigo1_ejey = fila_valida

            # # Dirección inicial del cazador en el laberinto 
            # self.direccion_actual = "abajo"
            
            # Se llama a la función que tiene las imagenes del enemigo1 (arriba, abajo, izquierda y derecha) 
            self.cargar_imagenes_enemigo1()
            # Se llama a la función que tiene las imagenes del enemigo2 (arriba, abajo, izquierda y derecha) 
            self.cargar_imagenes_enemigo2()
            # Se llama a la función que tiene las imagenes del enemigo3 (arriba, abajo, izquierda y derecha) 
            self.cargar_imagenes_enemigo3()
            
            # Se define la posición inicial que tendrá cada enemigo en el laberinto 
            
                # Se define la Imagen inicial del enemigo 1,2 y 3 
            self.imagen_actual1 = self.imagen_enemigo1_abajo
                # Imagen inicial del enemigo 2
            self.imagen_actual2 = self.imagen_enemigo2_abajo
                # Imagen inicial del enemigo 3
            self.imagen_actual3 = self.imagen_enemigo3_abajo
            
            
            # Define que la imagen inicial del jugador estará en la posición  hacia"abajo"
            #self.imagen_actual = self.imagen_enemigo1_abajo
            
            # Se convierte la posición del jugador en el laberinto (fila, columna) a pixeles 
            #posicion_ejex_pixeles= self.posicion_inicial_enemigo1_ejex *self.tamano_celda
            #posicion_ejey_pixeles = self.posicion_inicial_enemigo1_ejey * self.tamano_celda
            
            # Se coloca el enemigo 1 en el canvas 
            self.enemigo1_objeto = self.canvas_juego.create_image(
                                                                    self.posicion_inicial_enemigo1_ejex * self.tamano_celda,
                                                                    self.posicion_inicial_enemigo1_ejey * self.tamano_celda,
                                                                    anchor="nw",
                                                                    image=self.imagen_actual1
                                                                )

            print("Enemigo 1 creado en:", self.posicion_inicial_enemigo1_ejex, self.posicion_inicial_enemigo1_ejey)

            # Se coloca el enemigo 2 en el canvas 
            self.enemigo2_objeto = self.canvas_juego.create_image(
                                                                    self.posicion_inicial_enemigo2_ejex * self.tamano_celda,
                                                                    self.posicion_inicial_enemigo2_ejey * self.tamano_celda,
                                                                    anchor="nw",
                                                                    image=self.imagen_actual2
                                                                )

            print("Enemigo 2 creado en:", self.posicion_inicial_enemigo2_ejex, self.posicion_inicial_enemigo2_ejey)

            # Se coloca el enemigo 3 en el canvas 
            self.enemigo3_objeto = self.canvas_juego.create_image(
                                                                    self.posicion_inicial_enemigo3_ejex * self.tamano_celda,
                                                                    self.posicion_inicial_enemigo3_ejey * self.tamano_celda,
                                                                    anchor="nw",
                                                                    image=self.imagen_actual3
                                                                )

            print("Enemigo 3 creado en:", self.posicion_inicial_enemigo3_ejex, self.posicion_inicial_enemigo3_ejey)

###############################################    
    def cargar_imagenes_enemigo1(self):
        
        #Se define las rutas donde se encuentran las imagenes del enemigo 1 - cazador 
        ruta_enemigo1_arriba = os.path.join("Imagenes", "enemigo1_arriba.png")
        ruta_enemigo1_abajo = os.path.join("Imagenes", "enemigo1_abajo.png")
        ruta_enemigo1_izquierda = os.path.join("Imagenes", "enemigo1_izquierda.png")
        ruta_enemigo1_derecha = os.path.join("Imagenes", "enemigo1_derecha.png")

        #Se abre la carpeta donde se encuentra la imagen del enemigo1- cazador 
        self.imagen_enemigo1_arriba = ImageTk.PhotoImage(Image.open(ruta_enemigo1_arriba).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo1_abajo = ImageTk.PhotoImage(Image.open(ruta_enemigo1_abajo).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo1_izquierda = ImageTk.PhotoImage(Image.open(ruta_enemigo1_izquierda).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo1_derecha = ImageTk.PhotoImage(Image.open(ruta_enemigo1_derecha).resize((64, 64), Image.LANCZOS))
        
        print(" Las imágenes del enemigo cargadas correctamente.")
        
###############################################    
    def cargar_imagenes_enemigo2(self):
        
        #Se define las rutas donde se encuentran las imagenes del enemigo 2 - cazador 
        ruta_enemigo2_arriba = os.path.join("Imagenes", "enemigo2_arriba.png")
        ruta_enemigo2_abajo = os.path.join("Imagenes", "enemigo2_abajo.png")
        ruta_enemigo2_izquierda = os.path.join("Imagenes", "enemigo2_izquierda.png")
        ruta_enemigo2_derecha = os.path.join("Imagenes", "enemigo2_derecha.png")

        #Se abre la carpeta donde se encuentra la imagen del enemigo1- cazador 
        self.imagen_enemigo2_arriba = ImageTk.PhotoImage(Image.open(ruta_enemigo2_arriba).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo2_abajo = ImageTk.PhotoImage(Image.open(ruta_enemigo2_abajo).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo2_izquierda = ImageTk.PhotoImage(Image.open(ruta_enemigo2_izquierda).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo2_derecha = ImageTk.PhotoImage(Image.open(ruta_enemigo2_derecha).resize((64, 64), Image.LANCZOS))
        
        print(" Las imágenes del enemigo #2 cargadas correctamente.")
        
###############################################    
    def cargar_imagenes_enemigo3(self):
        
        #Se define las rutas donde se encuentran las imagenes del enemigo 1 - cazador 
        ruta_enemigo3_arriba = os.path.join("Imagenes", "enemigo3_arriba.png")
        ruta_enemigo3_abajo = os.path.join("Imagenes", "enemigo3_abajo.png")
        ruta_enemigo3_izquierda = os.path.join("Imagenes", "enemigo3_izquierda.png")
        ruta_enemigo3_derecha = os.path.join("Imagenes", "enemigo3_derecha.png")

        #Se abre la carpeta donde se encuentra la imagen del enemigo1- cazador 
        self.imagen_enemigo3_arriba = ImageTk.PhotoImage(Image.open(ruta_enemigo3_arriba).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo3_abajo = ImageTk.PhotoImage(Image.open(ruta_enemigo3_abajo).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo3_izquierda = ImageTk.PhotoImage(Image.open(ruta_enemigo3_izquierda).resize((64, 64), Image.LANCZOS))
        self.imagen_enemigo3_derecha = ImageTk.PhotoImage(Image.open(ruta_enemigo3_derecha).resize((64, 64), Image.LANCZOS))
        
        print(" Las imágenes del enemigo #3 cargadas correctamente.")
        
###############################################

    #Función que coloca al enemigo en una celda válida (camino o túnesl)
    def buscar_posicion_inicial_enemigo(self):
        
        
        #Se determina la cantidad de filas y columnas del laberinto 
        filas = len(self.mapa_terrenos_cazador)
        columnas = len(self.mapa_terrenos_cazador[0])
        #Determina donde esta el camino central del mapa 
        fila_central = len(self.mapa_terrenos_cazador) // 2

        while True:
            # Se selecciona una fila y columna al azar 
            fila = random.randint(1, filas - 2)
            columna = random.randint(1, columnas - 2)

            # Se guarda la posición escogida al azar 
            celda = self.mapa_terrenos_cazador[fila][columna]
            
            #Se valida que la celda donde aparezca el enemigo sea un caminio 
            if isinstance(celda, Camino):
                return columna, fila

            #Se valida que la celda donde aparezca el enemigo sea un tunel 
            if isinstance(celda, Tunel):
                
                #Valida que el tunel se encuentre junto al camnino 
                if fila == fila_central:
                    return columna, fila
                
                if fila == fila_central - 1 or fila == fila_central + 1:

                    # Se corrobora que la celda alrededor donde aparece el enemigo le permita moverse y salir de ese lugar al camino  
                    vecinos = [
                        (fila - 1, columna),
                        (fila + 1, columna),
                        (fila, columna - 1),
                        (fila, columna + 1)
                    ]

                    for posicion_vecina in vecinos:
                        # Se obtiene las coordenadas del enemigo fila, columna 
                        fila_vecina = posicion_vecina[0]
                        columna_vecina = posicion_vecina[1]

                        # Se comprueba si la fila está dentro del rango permitido
                        fila_dentro_de_rango = fila_vecina >= 0 and fila_vecina < filas

                        # Se comprueba si la columna está dentro del rango permitido
                        columna_dentro_de_rango = columna_vecina >= 0 and columna_vecina < columnas

                        # Si la fila y columna son válidas, entonces la casilla es válida para el enemigo
                        if fila_dentro_de_rango and columna_dentro_de_rango:

                            # Se asigna la casilla del laberinto 
                            celda_vecina = self.mapa_terrenos_cazador[fila_vecina][columna_vecina]

                            #Solo se acepta como válido un tunel que aparece junto al camino 
                            if isinstance(celda_vecina, Camino):
                                return columna, fila
    
###################################################

    #Función que valida que la posición que toma el enemigo 1 es válida (es camino, o tuneles)
    def es_posicion_valida(self, fila, columna):
    
        # Total de filas y columnas del laberinto
        total_filas = len(self.mapa_terrenos_cazador)
        total_columnas = len(self.mapa_terrenos_cazador[0])

        # Se revisa si la fila está dentro del rango permitido
        if fila < 0 or fila >= total_filas:
            return False # Si no esta dentro del rango se coloca False 
        
        # Se revisa si la columna está dentro del rango permitido
        if columna < 0 or columna >= total_columnas:
            return False # Si no esta dentro del rango se coloca False 
        
        # Se obtiene el tipo de celda (muro, salida, camino, tunel)
        tipo_celda = self.mapa_terrenos_cazador[fila][columna]

        if isinstance(tipo_celda, Tunel):

            # revisar si alrededor de donde esta el enemigo  hay algún camino
            vecinos = [
                (fila-1, columna),
                (fila+1, columna),
                (fila, columna-1),
                (fila, columna+1)
            ]

            tiene_salida = False

            for f, c in vecinos:
                if 0 <= f < total_filas and 0 <= c < total_columnas:
                    celda_vecina = self.mapa_terrenos_cazador[f][c]
                    if isinstance(celda_vecina, Camino) or isinstance(celda_vecina, Salida):
                        tiene_salida = True
                        break

            if not tiene_salida:
                return False   # ← Túnel sin salida, no se debe entrar 
        
        #Si el tipo de celda e CAMINO, SALIDA o TUNEL el enemigo se puede mover 

        return (
                isinstance(tipo_celda, Camino) or
                isinstance(tipo_celda, Tunel)  or
                isinstance(tipo_celda, Salida)
                )
###################################################

    #Función que mueve al enemigo #1 y actualiza su imagen conforme cambia de dirección 
    def actualizar_posicion1(self, fila_nueva, columna_nueva, direccion):

        #Se obtiene la posición actual del enemigo 1 en el laberinto 
        self.posicion_inicial_enemigo1_ejey = fila_nueva
        self.posicion_inicial_enemigo1_ejex = columna_nueva

        # Se cambia la imagen del enemigo según su dirección
        if direccion == "arriba":
            self.imagen_actual = self.imagen_enemigo1_arriba
        elif direccion == "abajo":
            self.imagen_actual = self.imagen_enemigo1_abajo
        elif direccion == "izquierda":
            self.imagen_actual = self.imagen_enemigo1_izquierda
        elif direccion == "derecha":
            self.imagen_actual = self.imagen_enemigo1_derecha

        # Actualizar la imagen del enemigo conforme se mueve 
        self.canvas_juego.coords(
                                    self.enemigo1_objeto,
                                    columna_nueva * self.tamano_celda,
                                    fila_nueva * self.tamano_celda
                                )

        self.canvas_juego.itemconfig(self.enemigo1_objeto, image=self.imagen_actual1)


###############################################
    #Función que mueve al enemigo #2 y actualiza su imagen conforme cambia de dirección 
    def actualizar_posicion2(self, fila_nueva, columna_nueva, direccion):

        #Se obtiene la posición actual del enemigo 1 en el laberinto 
        self.posicion_inicial_enemigo2_ejey = fila_nueva
        self.posicion_inicial_enemigo2_ejex = columna_nueva

        # Se cambia la imagen del enemigo según su dirección
        if direccion == "arriba":
            self.imagen_actual = self.imagen_enemigo2_arriba
        elif direccion == "abajo":
            self.imagen_actual = self.imagen_enemigo2_abajo
        elif direccion == "izquierda":
            self.imagen_actual = self.imagen_enemigo2_izquierda
        elif direccion == "derecha":
            self.imagen_actual = self.imagen_enemigo2_derecha

        # Actualizar la imagen del enemigo conforme se mueve 
        self.canvas_juego.coords(
                                    self.enemigo2_objeto,
                                    columna_nueva * self.tamano_celda,
                                    fila_nueva * self.tamano_celda
                                )

        self.canvas_juego.itemconfig(self.enemigo2_objeto, image=self.imagen_actual2)



###############################################
    #Función que mueve al enemigo #3 y actualiza su imagen conforme cambia de dirección 
    def actualizar_posicion3(self, fila_nueva, columna_nueva, direccion):

        #Se obtiene la posición actual del enemigo 1 en el laberinto 
        self.posicion_inicial_enemigo3_ejey = fila_nueva
        self.posicion_inicial_enemigo3_ejex = columna_nueva

        # Se cambia la imagen del enemigo según su dirección
        if direccion == "arriba":
            self.imagen_actual = self.imagen_enemigo3_arriba
        elif direccion == "abajo":
            self.imagen_actual = self.imagen_enemigo3_abajo
        elif direccion == "izquierda":
            self.imagen_actual = self.imagen_enemigo3_izquierda
        elif direccion == "derecha":
            self.imagen_actual = self.imagen_enemigo3_derecha

        self.canvas_juego.coords(
                                    self.enemigo3_objeto,
                                    columna_nueva * self.tamano_celda,
                                    fila_nueva * self.tamano_celda
                                )

        self.canvas_juego.itemconfig(self.enemigo3_objeto, image=self.imagen_actual3)


###############################################

# Función que permite mover al enemigo del juego del cazador de forma aleatoria 
      
    def mover_enemigo1(self):

        #Evita que el enemigo quede atrapado entre dos casillas (se encicle a reconocer que son casillas para moverse pero no sale de ahí)
        if not hasattr(self, "ultima_posicion_enemigo1"):
            self.ultima_posicion_enemigo1 = None

        # Se obtiene la posición actual del enemigo, para luego definir hacia donde se debe mover 
        fila_actual = self.posicion_inicial_enemigo1_ejey
        columna_actual = self.posicion_inicial_enemigo1_ejex

########
        #Se identifica de que tipo de celda esta el enemigo encima (muro, camino, salida, liana)
        celda_actual = self.mapa_terrenos_cazador[fila_actual][columna_actual]

        # Si la celda sobre la que se esta es una salida 
        if isinstance(celda_actual, Salida):

            print(f" El enemigo #1 ha encontrado una salida y sale de este en {fila_actual} {columna_actual}")
            
            # El enemigo ha logrado salir del laberinto y se elimina de este 
            self.canvas_juego.delete(self.enemigo1_objeto)  
            # Se detiene el movimiento del enemigo #1
            return  

        print(f"\n>>> ENEMIGO #1 EN: {fila_actual} {columna_actual}")

########
        # El enemigo busca todas las salidas que aparecen en el laberinto 
        salidas = [] # se agregan la salidas a la lista 
        for f in range(len(self.mapa_terrenos_cazador)):
            for c in range(len(self.mapa_terrenos_cazador[0])):
                if isinstance(self.mapa_terrenos_cazador[f][c], Salida):
                    salidas.append((f, c))

        print("Salidas detectadas:", salidas)

        # Elección de la salida más cercana usando minimo (min)
        salida_objetivo = min( salidas,
                                key=lambda s: abs(s[0] - fila_actual) + abs(s[1] - columna_actual)
                            )

        print("→ SALIDA OBJETIVO:", salida_objetivo)

        # Se identifica la fila y columna que estén mas cerca de la salida con respecto al enemigo 
        fila_obj, col_obj = salida_objetivo

########
        # Generación de movimientos 
        intentos = [
            ("arriba",    fila_actual - 1, columna_actual),
            ("abajo",     fila_actual + 1, columna_actual),
            ("izquierda", fila_actual, columna_actual - 1),
            ("derecha",   fila_actual, columna_actual + 1)
        ]

        movimientos_validos = [] # Son los movimientos que puede hacer el enmigo y que no chocan contra un muro 
        movimientos_directos = [] # son los movimientos que se acercan a la salida o el enemigo 

########
        # Se hace una copia de la posición actual del cazador (el enemigo debe evitar acercarse a este)
        cazador_f = self.posicion_inicial_cazador_ejey
        cazador_c = self.posicion_inicial_cazador_ejex

        for direccion, f, c in intentos:

            # Se verifica si la posición es valida (no sea un muro)
            if self.es_posicion_valida(f, c):

                # Se valida si la dirección a la que se mueve el enemigo es la misma que tiene el cazado (para evitarlo, porque si lo toca desaparece)
                if (f, c) == (cazador_f, cazador_c):
                    continue  # No se genera el movimiento hacia el cazador 
########
                # Se valida si la posición que debe seguir el enemigo de forma aleatoria ya la piso porque esto evita que se encicle (bucle)
                if self.ultima_posicion_enemigo1 == (f, c):
                    continue
                
                #Se guarda los movimientos válidos (no es un muro, no es la posición del cazador ni se encicla "celda repetida")
                movimientos_validos.append((direccion, f, c))

                # Movimiento que acerca a la salida
                dist_actual = abs(fila_actual - fila_obj) + abs(columna_actual - col_obj)
                dist_nueva  = abs(f - fila_obj) + abs(c - col_obj)

                if dist_nueva < dist_actual:
                    movimientos_directos.append((direccion, f, c))

        print("Movimientos directos:", movimientos_directos)

########
        # Se establece prioridad de moverse hacia donde se encuentre la salida más cercana 
        if movimientos_directos:
            direccion, f_nueva, c_nueva = movimientos_directos[0]
            print("Movimiento directo mas cercano a la salida aceptado")

        else:
            print("No existe un movimiento directo que lleve a la salida  Sin movimiento directo → tratando de salir del túnel")

            #Si el enemigo cayo aleatoriamente en una posición donde no es válido su movimiento lo detiene 
            if not movimientos_validos:
                print("No hay movimientos válidos— el enemigo queda quieto")
                self.canvas_juego.after(350, self.mover_enemigo1)
                return
########
            # Priorización de enemigo por buscar una celda que sea "camino" y no un "Tunel" para moverse 
            elegido = None
            for direccion, f, c in movimientos_validos:
                #Evalúa si la celda seleccionada para moverse es un camino 
                celda = self.mapa_terrenos_cazador[f][c]
                
                # Si la celda es un camino hace que el enemigo se mueva hacia este (da una prioridad al camino antes del tunel)
                if isinstance(celda, Camino):
                    elegido = (direccion, f, c)
                    print("Prioridad: camino encontrado")
                    break
            
            # Si no hay un camino cerca se hace un movimiento aleatorio, se evita moverse donde esta el cazador, vecinos prohibidos (muros, lianas), o celdas que ya piso   
            if elegido:
                direccion, f_nueva, c_nueva = elegido
            else:
                # último recurso (sin retrocesos)
                direccion, f_nueva, c_nueva = random.choice(movimientos_validos)
                print("→ Movimiento aleatorio seguro")

        # ============================================
        #   GUARDAR PARA EVITAR BUCLES
        # ============================================
        self.ultima_posicion_enemigo1 = (fila_actual, columna_actual)

        # ============================================
        #   MOVER ENEMIGO EN EL MAPA
        # ============================================
        self.actualizar_posicion1(f_nueva, c_nueva, direccion)

        # ============================================
        #   SIGUIENTE MOVIMIENTO
        # ============================================
        self.canvas_juego.after(350, self.mover_enemigo1)
        
##################################################################################################
###################################################################################################

    # def mover_enemigo2(self):

    #     if not hasattr(self, "ultima_posicion_enemigo2"):
    #         self.ultima_posicion_enemigo2 = None

    #     fila_actual = self.posicion_inicial_enemigo2_ejey
    #     columna_actual = self.posicion_inicial_enemigo2_ejex

    #     celda_actual = self.mapa_terrenos_cazador[fila_actual][columna_actual]

    #     if isinstance(celda_actual, Salida):
    #         print(f"✔ Enemigo #2 salió en {fila_actual},{columna_actual}")
    #         self.canvas_juego.delete(self.enemigo2_objeto)
    #         return

    #     salidas = []
    #     for f in range(len(self.mapa_terrenos_cazador)):
    #         for c in range(len(self.mapa_terrenos_cazador[0])):
    #             if isinstance(self.mapa_terrenos_cazador[f][c], Salida):
    #                 salidas.append((f, c))

    #     salida_objetivo = min(
    #         salidas,
    #         key=lambda s: abs(s[0] - fila_actual) + abs(s[1] - columna_actual)
    #     )

    #     fila_obj, col_obj = salida_objetivo

    #     intentos = [
    #         ("arriba",    fila_actual - 1, columna_actual),
    #         ("abajo",     fila_actual + 1, columna_actual),
    #         ("izquierda", fila_actual, columna_actual - 1),
    #         ("derecha",   fila_actual, columna_actual + 1)
    #     ]

    #     movimientos_validos = []
    #     movimientos_directos = []

    #     cazador_f = self.posicion_inicial_cazador_ejey
    #     cazador_c = self.posicion_inicial_cazador_ejex

    #     for intento in intentos:

    #         direccion = intento[0]
    #         f = intento[1]
    #         c = intento[2]

    #         if not self.es_posicion_valida(f, c):
    #             continue

    #         if (f, c) == (cazador_f, cazador_c):
    #             continue

    #         if self.ultima_posicion_enemigo2 == (f, c):
    #             continue

    #         movimientos_validos.append((direccion, f, c))

    #         distancia_actual = abs(fila_actual - fila_obj) + abs(columna_actual - col_obj)
    #         distancia_nueva  = abs(f - fila_obj) + abs(c - col_obj)

    #         if distancia_nueva < distancia_actual:
    #             movimientos_directos.append((direccion, f, c))

    #     if movimientos_directos:
    #         direccion, f_nueva, c_nueva = movimientos_directos[0]
    #     else:
    #         if not movimientos_validos:
    #             self.canvas_juego.after(250, self.mover_enemigo2)
    #             return

    #         elegido = None
    #         for direccion, f, c in movimientos_validos:
    #             if isinstance(self.mapa_terrenos_cazador[f][c], Camino):
    #                 elegido = (direccion, f, c)
    #                 break

    #         if elegido:
    #             direccion, f_nueva, c_nueva = elegido
    #         else:
    #             direccion, f_nueva, c_nueva = random.choice(movimientos_validos)

    #     self.ultima_posicion_enemigo2 = (fila_actual, columna_actual)
    #     self.actualizar_posicion2(f_nueva, c_nueva, direccion)
    #     self.canvas_juego.after(250, self.mover_enemigo2)
        
##################################################################################################
###################################################################################################

# def mover_enemigo3(self):

#     if not hasattr(self, "ultima_posicion_enemigo3"):
#         self.ultima_posicion_enemigo3 = None

#     fila_actual = self.posicion_inicial_enemigo3_ejey
#     columna_actual = self.posicion_inicial_enemigo3_ejex

#     celda_actual = self.mapa_terrenos_cazador[fila_actual][columna_actual]

#     if isinstance(celda_actual, Salida):
#         print(f"✔ Enemigo #3 salió en {fila_actual},{columna_actual}")
#         self.canvas_juego.delete(self.enemigo3_objeto)
#         return

#     salidas = []
#     for f in range(len(self.mapa_terrenos_cazador)):
#         for c in range(len(self.mapa_terrenos_cazador[0])):
#             if isinstance(self.mapa_terrenos_cazador[f][c], Salida):
#                 salidas.append((f, c))

#     salida_objetivo = min(
#         salidas,
#         key=lambda s: abs(s[0] - fila_actual) + abs(s[1] - columna_actual)
#     )

#     fila_obj, col_obj = salida_objetivo

#     intentos = [
#         ("arriba",    fila_actual - 1, columna_actual),
#         ("abajo",     fila_actual + 1, columna_actual),
#         ("izquierda", fila_actual, columna_actual - 1),
#         ("derecha",   fila_actual, columna_actual + 1)
#     ]

#     movimientos_validos = []
#     movimientos_directos = []

#     cazador_f = self.posicion_inicial_cazador_ejey
#     cazador_c = self.posicion_inicial_cazador_ejex

#     for intento in intentos:

#         direccion = intento[0]
#         f = intento[1]
#         c = intento[2]

#         if not self.es_posicion_valida(f, c):
#             continue

#         if (f, c) == (cazador_f, cazador_c):
#             continue

#         if self.ultima_posicion_enemigo3 == (f, c):
#             continue

#         movimientos_validos.append((direccion, f, c))

#         distancia_actual = abs(fila_actual - fila_obj) + abs(columna_actual - col_obj)
#         distancia_nueva  = abs(f - fila_obj) + abs(c - col_obj)

#         if distancia_nueva < distancia_actual:
#             movimientos_directos.append((direccion, f, c))

#     if movimientos_directos:
#         direccion, f_nueva, c_nueva = movimientos_directos[0]
#     else:
#         if not movimientos_validos:
#             self.canvas_juego.after(250, self.mover_enemigo3)
#             return

#         elegido = None
#         for direccion, f, c in movimientos_validos:
#             if isinstance(self.mapa_terrenos_cazador[f][c], Camino):
#                 elegido = (direccion, f, c)
#                 break

#         if elegido:
#             direccion, f_nueva, c_nueva = elegido
#         else:
#             direccion, f_nueva, c_nueva = random.choice(movimientos_validos)

#     self.ultima_posicion_enemigo3 = (fila_actual, columna_actual)
#     self.actualizar_posicion3(f_nueva, c_nueva, direccion)
#     self.canvas_juego.after(250, self.mover_enemigo3)





            


 


    