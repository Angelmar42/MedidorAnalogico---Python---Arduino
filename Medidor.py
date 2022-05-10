# -*- coding: utf-8 -*-

import pyfirmata
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import Tk, Label, Button


board = pyfirmata.Arduino('COM5')
it = pyfirmata.util.Iterator(board)
it.start()
analog_input = board.get_pin('a:0:i')
Y=[]
X=[]
i=0
class VentanaEjemplo:
    def __init__(self, master):
        self.master = master
        master.title("Medidor analogico")
        self.etiqueta = Label(master, text="Medición")
        self.etiqueta.pack()
        self.botonSaludo = Button(master, text="Medir", command=self.medir)
        self.botonSaludo.pack()
        self.botonCerrar = Button(master, text="Graficar", command=self.graficar)
        self.botonCerrar.pack()

        
    def medir(self):
            while True:
                x=0
                y=0
                global i
                analog_value = analog_input.read()
                y=analog_value
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                if i == 0:
                    i=timestamp
                x=timestamp-i
                Y.append(y)
                X.append(x)
                if x>4:
                    i=-1
                    break
                print("Valor: " + str(y) + "\n Hora: "+ str(x))

    def graficar(self):
        plt.plot(X, Y)
        
        
        plt.show()


root = Tk()
miVentana = VentanaEjemplo(root)
root.mainloop()


print(X)
print(Y)