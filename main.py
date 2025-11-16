import tkinter as tk
from tkinter import *
##from Interfaz import interfaz # se pasa el nombre del archivo (Interfaz) y el nombre de la clase (interfaz) 
from Interfaz import PantallaPrincipal # se pasa el nombre del archivo (Interfaz) y el nombre de la clase (interfaz) 

# Función que Sirve para quitar el margen izquierdo y pone la ventanaal borde de la pantalla.
def ajustar_posicion():
    pantalla_principal.update_idletasks() # actualiza visualmente la ventana antes de usarla 
    pantalla_principal.geometry("+0+0") # Coloca la venta en la posición x,y (0,0)
    
if __name__ == "__main__":
    pantalla_principal= tk.Tk()

    #Se obtiene el ancho y alto de la ventana  
    ancho_pantalla_principal = pantalla_principal.winfo_screenwidth()
    alto_pantalla_principal = pantalla_principal.winfo_screenheight()

    print("ANCHO REAL =", ancho_pantalla_principal)
    print("ALTO REAL =", alto_pantalla_principal)
    
    #Se define el tamaño que tendrá la pantalla principal 
    pantalla_principal.state("zoomed")

    # no permite hacer la ventana ni más ancha ni más alta 
    pantalla_principal.resizable(width=NO,height=NO)
    
    #Se llama al método que crea la pantalla de juego 
    app = PantallaPrincipal(pantalla_principal) # se pasa el nombre de la clase  y los parámetros que esta contiene 
    pantalla_principal.mainloop()
    
    
 