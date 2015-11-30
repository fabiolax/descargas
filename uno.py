import tkinter
from tkinter.constants import *
from tkinter import filedialog
from cProfile import label

#Declaracion del boton
babrir = tkinter.Button

#
#Creacion grafica
#

tk = tkinter.Tk()
#Se crea ventana

tk.title("Hadoop")
#Titulo de ventana
tk.geometry("400x400")
#Tamaño de ventana


#Si se van a llamar funciones deben de estar arriba
#
#Funciones
#


#
#Funcion pulsar boton
#

def Pulsarboton ():
    variableabrir = filedialog.askopenfile("r")



#
#Frames
#
framebotones = tkinter.Frame(tk, relief=RIDGE, borderwidth=1)
#Tamaño del frame. Agrega tk para señalar que es un objeto de la ventana
#en la que se  esta trabajondo
framebotones.pack(fill=BOTH)
framebotones.pack(side=TOP)
#Se crea el frame

framebotons = tkinter.Frame(tk, relief=RIDGE, borderwidth=1)
framebotons.pack(fill=BOTH)
framebotons.pack(side=BOTTOM)


#
#Creacion de los botones
#
babrir = tkinter.Button(framebotones, text="Open",command=Pulsarboton)
babrir.pack(side=LEFT)#Se pone ubicacion en ventana del boton
#babrir.pack(command=Pulsarboton)


bejecutar = tkinter.Button(framebotones,text="Run")#Se agrega al mismo frame del boton abrir
bejecutar.pack(side=LEFT)
#archivo_binario = open(file_name [(tkinter.Button(text="Open")), access_mode][, buffering])

bsalir = tkinter.Button(framebotons, text="Exit",command=tk.destroy)#Comando para salir de python
bsalir.pack(side=RIGHT)#Ubicacion del boton salir (fondo)







tk.mainloop()
#Finaliza el objeto tk es decir la ventana