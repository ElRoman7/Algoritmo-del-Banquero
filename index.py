import itertools
import tkinter as tk

# Clase para representar una situación de bloqueo
class DeadLock(object):
    def __init__(self, assigned, maximums, available):
        # Inicializar con recursos asignados, máximos y disponibles
        self._assigned = assigned
        self._maximums = maximums
        self._available = available
        self._proc_count = len(assigned)
        self._calculate_needs()  # Calcular necesidades de recursos de cada proceso

    # Calcular necesidades de recursos de cada proceso
    def _calculate_needs(self):
        self._needs = [[i - j for i, j in zip(x, y)]
                       for x, y in zip(self._maximums, self._assigned)]

    # Verificar si una secuencia de procesos es segura
    def is_secure(self, sequence):
        final = [False for f in range(self._proc_count)]  # Inicializar una lista para rastrear el estado final
        work = self._available  # Inicializar vector de trabajo

        for m in sequence:
            if (final[m] is False) \
                    and self._less_equal(self._needs[m], work):
                final[m] = True
                work = [x + y for x, y in zip(work, self._assigned[m])]
            else:
                break

        try:
            final.index(False)
            secure = False
        except ValueError:
            secure = True

        return secure

    # Obtener secuencias seguras de procesos
    def get_secure_sequences(self):
        permutations = list(itertools.permutations(range(self._proc_count)))
        sequences = []

        for p in permutations:
            if self.is_secure(p):
                sequences.append(p)

        return sequences

    # Guardar estado actual de los recursos
    def _save_status(self):
        self._assigned_bkp = list(self._assigned)
        self._available_bkp = list(self._available)
        self._maximums_bkp = list(self._maximums)
        self._needs_bkp = list(self._needs)

    # Retroceder al estado guardado
    def _rollback(self):
        self._assigned = self._assigned_bkp
        self._available = self._available_bkp
        self._maximums = self._maximums_bkp
        self._needs = self._needs_bkp

    # Asignar recursos a un proceso
    def assign_resources(self, process_num, request, auto_rollback=True):
        cond1 = self._less_equal(request, self._needs[process_num])
        cond2 = self._less_equal(request, self._available)

        if cond1 and cond2:
            self._save_status()
            self._available = [x - y
                               for x, y
                               in zip(self._available, request)]
            self._assigned[process_num] = [a + b
                                           for a, b
                                           in zip(self._assigned[process_num],
                                                  request)]
            self._needs[process_num] = [c - d
                                         for c, d
                                         in zip(self._needs[process_num], request)]

            if auto_rollback:
                self._rollback()

            return True
        else:
            return False

    # Asignar recursos a un proceso y probar si hay bloqueo
    def assign_and_test(self, process_num, request, auto_rollback=True):
        secure = False
        if self.assign_resources(process_num, request, False):
            if self.get_secure_sequences():
                secure = True

            if auto_rollback:
                self._rollback()

        return secure

    # Comprobar si los elementos de iterable1 son menores o iguales que los de iterable2
    def _less_equal(self, iterable1, iterable2):
        res = [i for i, j in zip(iterable1, iterable2) if i > j]

        if res == []:
            return True
        else:
            return False

    # Obtener las necesidades
    def get_needs(self):
        return self._needs

    # Obtener los asignados
    def get_assigned(self):
        return self._assigned

    # Obtener los máximos
    def get_maximums(self):
        return self._maximums

    # Obtener los disponibles
    def get_available(self):
        return self._available

    # Obtener la cantidad de procesos
    def get_proc_count(self):
        return self._proc_count

    # Propiedades
    needs = property(get_needs)
    assigned = property(get_assigned)
    maximums = property(get_maximums)
    available = property(get_available)
    proc_count = property(get_proc_count)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.deadlock = DeadLock([[2, 1, 1, 1], [1, 0, 0, 1], [1, 0, 3, 1], [3, 0, 0, 1], [1, 2, 1, 3]],
                                 [[3, 2, 1, 1], [2, 1, 3, 3], [3, 1, 3, 3], [4, 2, 1, 2], [3, 3, 2, 5]],
                                 [2, 2, 3, 3])

        self.matrix_frame = tk.Frame(self)
        self.matrix_frame.pack()

        self.matrix_labels = []

        # Create labels for column headers
        for i in range(len(self.deadlock.assigned[0])):
            label = tk.Label(self.matrix_frame, text="Resource {}".format(i))
            label.grid(row=0, column=i + 1, padx=5, pady=5)

        # Create labels for process names and matrix data
        for i, process in enumerate(self.deadlock.assigned):
            process_labels = []
            for j, assignment in enumerate(process):
                label = tk.Label(self.matrix_frame, text=str(assignment), width=5, height=2, relief="ridge")
                label.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                process_labels.append(label)
            self.matrix_labels.append(process_labels)

        self.run_button = tk.Button(self, text="Run Tests", command=self.run_tests)
        self.run_button.pack()

    def run_tests(self):
        results = []
        results.append(self.deadlock.assign_and_test(4, [1, 2, 1, 3]))
        results.append(self.deadlock.assign_and_test(3, [1, 0, 0, 2]))
        results.append(self.deadlock.assign_and_test(2, [1, 1, 0, 1]))
        results.append(self.deadlock.assign_and_test(1, [1, 1, 3, 1]))
        results.append(self.deadlock.assign_and_test(0, [3, 2, 0, 0]))

        self.update_matrix(results)

    def update_matrix(self, results):
        for i, process in enumerate(self.deadlock.assigned):
            for j, assignment in enumerate(process):
                if results[i]:
                    self.matrix_labels[i][j].config(bg="green")
                else:
                    self.matrix_labels[i][j].config(bg="red")


root = tk.Tk()
app = Application(master=root)
app.mainloop()
