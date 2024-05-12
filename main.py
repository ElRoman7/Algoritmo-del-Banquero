import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time

class BankerAlgorithmGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Algoritmo del Banquero")
        self.master.geometry("400x300")

        self.canvas = tk.Canvas(self.master, width=380, height=200, bg="white")
        self.canvas.pack(padx=10, pady=10)

        # Definir valores
        self.available_resources = [6, 3, 3]
        self.max_claims = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
        self.allocation = [[0, 1, 2], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
        self.requests = [[1, 3, 1], [3, 0, 2], [1, 2, 1], [1, 0, 0], [0, 0, 2]]

        self.process_button = tk.Button(self.master, text="Iniciar Proceso", command=self.start_process)
        self.process_button.pack(pady=10)

    def start_process(self):
        self.canvas.delete("all")
        banker = BankerAlgorithm(self.available_resources, self.max_claims, self.allocation)
        for i in range(len(self.requests)):
            request = self.requests[i]
            is_approved = banker.request_resources(i, request)
            color = "green" if is_approved else "red"
            self.draw_square(i, color)
            time.sleep(1)

    def draw_square(self, index, color):
        x = 50 + (index % 3) * 100
        y = 50 + (index // 3) * 100
        self.canvas.create_rectangle(x, y, x + 80, y + 80, fill=color)

class BankerAlgorithm:
    def __init__(self, available, max_claim, allocation):
        self.available = available
        self.max_claim = max_claim
        self.allocation = allocation
        self.n_processes = len(allocation)
        self.n_resources = len(available)

    def is_safe_state(self, process, need, work, finish):
        for i in range(self.n_resources):
            if need[process][i] > work[i]:
                return False
        return True

    def request_resources(self, process, request):
        for i in range(self.n_resources):
            if request[i] > self.max_claim[process][i]:
                return False

        if request[0] > self.available[0] or request[1] > self.available[1] or request[2] > self.available[2]:
            return False

        for i in range(self.n_resources):
            self.available[i] -= request[i]
            self.allocation[process][i] += request[i]

        finish = [False] * self.n_processes
        work = self.available[:]
        need = [[self.max_claim[i][j] - self.allocation[i][j] for j in range(self.n_resources)] for i in range(self.n_processes)]

        while True:
            safe_sequence_found = False
            for i in range(self.n_processes):
                if not finish[i] and self.is_safe_state(i, need, work, finish):
                    for j in range(self.n_resources):
                        work[j] += self.allocation[i][j]
                    finish[i] = True
                    safe_sequence_found = True
                    break
            if not safe_sequence_found:
                break

        if all(finish):
            return True
        else:
            for i in range(self.n_resources):
                self.available[i] += request[i]
                self.allocation[process][i] -= request[i]
            return False


def main():
    root = tk.Tk()
    app = BankerAlgorithmGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
