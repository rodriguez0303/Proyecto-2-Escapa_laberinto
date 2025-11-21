import tkinter as tk
from tkinter import *
##from Interfaz import interfaz # se pasa el nombre del archivo (Interfaz) y el nombre de la clase (interfaz) 
from Interfaz import PantallaPrincipal # se pasa el nombre del archivo (Interfaz) y el nombre de la clase (interfaz) 


if __name__ == "__main__":
    pantalla_principal= tk.Tk()
    
    #Se le da el nombre a la pantalla prinicipal del juego 
    pantalla_principal.title("Escapando del laberinto")
    
    # Se actualiza los componentes de la ventana principal 
    pantalla_principal.update_idletasks()

    #Se obtiene el ancho y alto de la ventana (para que no incluya la barra de tareas)  
    ancho_pantalla_principal = pantalla_principal.winfo_screenwidth()
    #alto_pantalla_principal = pantalla_principal.winfo_screenheight()
    alto_pantalla_principal = pantalla_principal.winfo_vrootheight()

    # Se define el tamaño de cada celda del laberinto 
    tamano_celda = 64
    
    # Se calcula cuantas filas y columnas caben sobre la pantalla principal 
    columnas = ancho_pantalla_principal // tamano_celda
    filas = alto_pantalla_principal // tamano_celda 
    
    ancho_final = columnas * tamano_celda
    alto_final  = filas    * tamano_celda - 15
    
    # Se aplica el tamaño exacto a la pantalla principal 
    pantalla_principal.geometry(f"{ancho_final}x{alto_final}+0+0")
    pantalla_principal.resizable(False, False)
    
    print("Pantalla principal ajustada a:", ancho_final, alto_final)
    
    #Se llama al método que crea la pantalla de juego 
    app = PantallaPrincipal(pantalla_principal) # se pasa el nombre de la clase  y los parámetros que esta contiene 
    pantalla_principal.mainloop()
    
    
 