import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import ImageTk, Image

class CalculadoraCircuitos:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Calculadora de Circuitos')
        self.root.geometry('400x300')

        # Cargar la imagen de fondo
        image = Image.open("background_image.jpg")
        self.background_image = ImageTk.PhotoImage(image)

        # Crear un widget Label para mostrar la imagen de fondo
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.circuito_var = tk.StringVar()

        self.label_circuito = tk.Label(self.root, text='Selecciona el tipo de circuito:')
        self.label_circuito.pack()

        self.radio_button_RC = tk.Radiobutton(self.root, text='RC', variable=self.circuito_var, value='RC')
        self.radio_button_RC.pack()

        self.radio_button_RL = tk.Radiobutton(self.root, text='RL', variable=self.circuito_var, value='RL')
        self.radio_button_RL.pack()

        self.label_resistencia = tk.Label(self.root, text='Resistencia:')
        self.label_resistencia.pack()

        self.entry_resistencia = tk.Entry(self.root)
        self.entry_resistencia.pack()

        self.label_capacitancia = tk.Label(self.root, text='Capacitancia:')
        self.label_capacitancia.pack()

        self.entry_capacitancia = tk.Entry(self.root)
        self.entry_capacitancia.pack()

        self.label_inductancia = tk.Label(self.root, text='Inductancia:')
        self.label_inductancia.pack()

        self.entry_inductancia = tk.Entry(self.root)
        self.entry_inductancia.pack()

        self.label_frecuencia = tk.Label(self.root, text='Frecuencia:')
        self.label_frecuencia.pack()

        self.entry_frecuencia = tk.Entry(self.root)
        self.entry_frecuencia.pack()

        self.button_calcular_respuesta = tk.Button(self.root, text='Mostrar gráfica', command=self.calcular_respuesta)
        self.button_calcular_respuesta.pack()

        self.button_calcular_impedancia = tk.Button(self.root, text='Calcular Impedancia', command=self.calcular_impedancia)
        self.button_calcular_impedancia.pack()

        self.button_calcular_ohm = tk.Button(self.root, text='Cálculo de Ohm', command=self.calcular_ohm)
        self.button_calcular_ohm.pack()

    def run(self):
        self.root.mainloop()

    def calcular_respuesta(self):
        circuito = self.circuito_var.get()

        if circuito == 'RC':
            R = float(self.entry_resistencia.get())
            C = float(self.entry_capacitancia.get())

            # Cálculo de la respuesta en frecuencia para el circuito RC
            f = np.logspace(0, 6, num=1000)
            w = 2 * np.pi * f
            H = 1 / np.sqrt(1 + (w * R * C)**2)
            titulo = 'Respuesta en frecuencia de un circuito RC'

        elif circuito == 'RL':
            R = float(self.entry_resistencia.get())
            L = float(self.entry_inductancia.get())

            # Cálculo de la respuesta en frecuencia para el circuito RL
            f = np.logspace(0, 6, num=1000)
            w = 2 * np.pi * f
            H = R / np.sqrt(R**2 + (w * L)**2)
            titulo = 'Respuesta en frecuencia de un circuito RL'

        else:
            messagebox.showerror("Error", "Tipo de circuito no válido.")
            return

        # Gráfico de la respuesta en frecuencia
        plt.figure()
        plt.semilogx(f, 20 * np.log10(H))
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Ganancia (dB)')
        plt.title(titulo)
        plt.grid(True)
        plt.show()

    def calcular_impedancia(self):
        circuito = self.circuito_var.get()

        if circuito == 'RC':
            if self.entry_capacitancia.get() == '':
                messagebox.showerror("Error", "Debes ingresar un valor para la capacitancia.")
                return

            C = float(self.entry_capacitancia.get())
            if C == 0:
                messagebox.showerror("Error", "La capacitancia debe ser mayor que cero.")
                return

            frecuencia = float(self.entry_frecuencia.get())
            impedancia = 1 / (C*frecuencia)
            messagebox.showinfo("Impedancia", "El valor de la impedancia es: " + str(-impedancia)+'j')

        elif circuito == 'RL':
            if self.entry_inductancia.get() == '':
                messagebox.showerror("Error", "Debes ingresar un valor para la inductancia.")
                return

            L = float(self.entry_inductancia.get())
            if L == 0:
                messagebox.showerror("Error", "La inductancia debe ser mayor que cero.")
                return

            frecuencia = float(self.entry_frecuencia.get())
            impedancia = frecuencia * L
            messagebox.showinfo("Impedancia", "El valor de la impedancia es: " + str(impedancia)+'j')

        else:
            messagebox.showerror("Error", "Tipo de circuito no válido.")

    def calcular_ohm(self):
        ohm_window = tk.Toplevel(self.root)
        ohm_window.title('Cálculo de Ohm')
        ohm_window.geometry('300x200')

        label_calculo = tk.Label(ohm_window, text='Selecciona qué deseas calcular:')
        label_calculo.pack()

        seleccion_var = tk.StringVar()

        def abrir_calculo():
            seleccion = seleccion_var.get()

            if seleccion == 'Resistencia':
                valor_V = simpledialog.askfloat('Valor del Voltaje', 'Ingresa el valor del voltaje:')
                valor_I = simpledialog.askfloat('Valor de la Corriente', 'Ingresa el valor de la corriente:')
                if valor_V is not None and valor_I is not None:
                    resultado = valor_V / valor_I
                    messagebox.showinfo("Resultado", "El valor de la resistencia es: " + str(resultado)+' Ohm')

            elif seleccion == 'Voltaje':
                valor_R = simpledialog.askfloat('Valor de la Resistencia', 'Ingresa el valor de la resistencia:')
                valor_I = simpledialog.askfloat('Valor de la Corriente', 'Ingresa el valor de la corriente:')
                if valor_R is not None and valor_I is not None:
                    resultado = valor_R * valor_I
                    messagebox.showinfo("Resultado", "El valor del voltaje es: " + str(resultado)+' V')

            elif seleccion == 'Corriente':
                valor_V = simpledialog.askfloat('Valor del Voltaje', 'Ingresa el valor del voltaje:')
                valor_R = simpledialog.askfloat('Valor de la Resistencia', 'Ingresa el valor de la resistencia:')
                if valor_V is not None and valor_R is not None:
                    resultado = valor_V / valor_R
                    messagebox.showinfo("Resultado", "El valor de la corriente es: " + str(resultado)+' A')

            else:
                messagebox.showerror("Error", "Selecciona una opción válida.")

        opciones = ['Resistencia', 'Voltaje', 'Corriente']
        for opcion in opciones:
            radio_button = tk.Radiobutton(ohm_window, text=opcion, variable=seleccion_var, value=opcion)
            radio_button.pack()

        button_calcular = tk.Button(ohm_window, text='Calcular', command=abrir_calculo)
        button_calcular.pack()

if __name__ == '__main__':
    calculadora = CalculadoraCircuitos()
    calculadora.run()
