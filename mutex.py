import tkinter as tk
import threading
import random
import time

class CarreraDeHilos:
    def __init__(self, ventana):
        # Creación de la ventana principal
        self.ventana = ventana
        self.ventana.title("Simulador de Carrera de Hilos")
        self.ventana.geometry("600x400")

        # Creación del lienzo (canvas) para la carrera
        self.canvas = tk.Canvas(ventana, width=600, height=300, bg="white")
        self.canvas.pack()

        # Inicialización de listas para los corredores y sus posiciones
        self.corredores = []
        self.posiciones = []
        self.mutex = threading.Lock()  # Mutex para la exclusión mutua
        self.crear_corredores()

        # Creación del botón para comenzar la carrera
        self.btn_comenzar = tk.Button(ventana, text="Comenzar Carrera", command=self.comenzar_carrera)
        self.btn_comenzar.pack()

    def crear_corredores(self):
        # Creación de los corredores (rectángulos) en el lienzo
        for i in range(5):
            corredor = self.canvas.create_rectangle(10, (i+1)*50, 40, (i+1)*50 + 30, fill=self.color_aleatorio(), outline="")
            self.corredores.append(corredor)
            self.posiciones.append(0)

    def color_aleatorio(self):
        # Generación de colores aleatorios para los corredores
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def comenzar_carrera(self):
        # Deshabilita el botón para evitar múltiples clics
        self.btn_comenzar.config(state="disabled")
        self.hilos_corredores = []
        for i in range(5):
            # Creación de hilos para cada corredor
            hilo = threading.Thread(target=self.correr, args=(i,))
            self.hilos_corredores.append(hilo)
            hilo.start()

    def correr(self, indice):
        while self.posiciones[indice] < 550:
            # Simulación de movimiento de los corredores
            time.sleep(random.uniform(0.1, 0.5))
            with self.mutex:  # Bloquea el mutex para exclusión mutua
                self.canvas.move(self.corredores[indice], 10, 0)
                self.posiciones[indice] += 10

        # Mostrar mensaje cuando un corredor termina la carrera
        self.canvas.create_text(300, 50 + indice * 50, text=f"Corredor {indice + 1} ha terminado la carrera", fill="black", font=("Arial", 12, "bold"))

if __name__ == "__main__":
    ventana = tk.Tk()
    app = CarreraDeHilos(ventana)
    ventana.mainloop()
