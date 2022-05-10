# -*- coding: utf-8 -*-
"""
@author: Angel Martínez Romero
"""

import pyfirmata
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import Tk, Label, Button, ttk
import pandas as pd
import time

global X
global Y
global datazo
datazo="Desconectado"
Y=[]
X=[]
i=0
#(x=60, y=40, width=100, height=30)
class VentanaEjemplo:
    def __init__(self, master):
        self.master = master
        master.title("Medidor analogico")
        self.etiqueta = Label(master, text="Medidor Analogico para PicoAmperimetro",font=("Roboto Bold", 12))
        self.etiqueta.place(x=75, y=0,width=350, height=30)
        self.conectar = Button(master, text="Conectar", command=self.conectar)
        self.conectar.place(x=50, y=55,width=100, height=30)
        self.botonSaludo = Button(master, text="Medir", command=self.medir)
        self.botonSaludo.place(x=50, y=95,width=100, height=30)
        self.botonCerrar = Button(master, text="Graficar", command=self.graficar)
        self.botonCerrar.place(x=50, y=135,width=100, height=30)
        self.botonGuardar = Button(master, text="Guardar datos", command=self.guardar)
        self.botonGuardar.place(x=50, y=175,width=100, height=30)
        self.creditos = Label(master, text="Programa dise\xf1ado por: Angel Mart\xednez Romero (2021). Para el laboratorio de sisntesis y \ncaracterización durante el programa PEEES orientado por el Dr. Victor Romero Arellano.",font=("Roboto", 7))
        self.creditos.place(x=20, y=250,width=460, height=50)
        
        global etiqueta2
        etiqueta2 = Label(text=datazo,font=("Roboto Bold", 11), fg='#f00')
        etiqueta2.place(x=260, y=213,width=190, height=20)

        
        global entry 
        entry = ttk.Entry(root)
        entry.place(x=50, y=215,width=100, height=20)

        
    def medir(self):
            global datazo
            datazo = ("Medido por: " + str(entry.get()) + " Segundos")
            etiqueta2.config( text=datazo,font=("Roboto Bold", 11),fg='#000000')
            while True:
                x=0
                y=0
                global i
                analog_value = board.analog[0].read()
                y=analog_value
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                if i == 0:
                    i=timestamp
                x=timestamp-i
                Y.append(y)
                X.append(x)
                time.sleep(0.01) # espera en segundos
                if x>int(entry.get()):
                    i=-1
                    break
                print("Valor: " + str(y) + "\n Hora: "+ str(x))
            entry.delete(0,len(entry.get()))
            i=0
            
    def graficar(self):
        plt.plot(X, Y)
        plt.show()
    
    def conectar(self):
        global board
        global datazo
        global etiqueta2
        etiqueta2.config( text=datazo,font=("Roboto Bold", 11))
        board = pyfirmata.Arduino('COM5')
        it = pyfirmata.util.Iterator(board)
        etiqueta2.config( text=datazo,font=("Roboto Bold", 11))
        it.start()
        analog_input = board.get_pin('a:0:i')
        datazo="En linea"
        etiqueta2.config( text=datazo,font=("Roboto Bold", 11), fg='#00FF00')

        
        
    def guardar(self):
        global X
        global Y
        global datazo
        datazo = ("Guardado como: " + str(entry.get())+".csv")
        etiqueta2.config( text=datazo,font=("Roboto Bold", 11),fg='#000000')
        df = pd.DataFrame({'X': X, 'Y':Y})  
        df.to_csv(entry.get()+".csv")
        entry.delete(0,len(entry.get()))
        Y=[]
        X=[]



root = Tk()
root.geometry('500x300')
miVentana = VentanaEjemplo(root)
root.mainloop()