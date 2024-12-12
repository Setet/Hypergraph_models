import tkinter as tk
import random
import matplotlib.pyplot as plt
import hypernetx as hnx

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from hypernetx import Hypergraph as HnxHypergraph


def hypertree_width_approximation(hypergraph):
    """
    Приближенное вычисление древовидной ширины гиперграфа.

    Args:
        hypergraph: Список множеств, представляющих гиперграф.

    Returns:
        Приближенное значение древовидной ширины.
    """

    nodes = set()

    for edge in hypergraph:
        nodes.update(edge)

    nodes = list(nodes)
    num_nodes = len(nodes)

    best_width = float('inf')

    # Число итераций
    interactions = 100

    # Итеративный жадный алгоритм
    for _ in range(interactions):
        ordering = list(range(num_nodes))

        # Перемешиваю вершины для случайного старта
        random.shuffle(ordering)

        width = 0
        for i in range(num_nodes):
            node_index = ordering[i]
            node_neighbors = set()
            for edge in hypergraph:
                if node_index in edge:
                    node_neighbors.update(edge)

            width = max(width, len(node_neighbors) - 1)  # -1 так как сама вершина включается в neighbours

        best_width = min(best_width, width)

    return best_width


class HypergraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.graph_frame = None
        self.manual_hyperedges_input = None
        self.hyperedge_input = None
        self.vertex_input = None

        self.title("Вычисление древовидной ширины гиперграфа")
        self.geometry("500x500")

        self.create_widgets()

    # Создание интерфейса
    def create_widgets(self):
        # Верхняя часть для ввода данных
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        # Количество вершин
        vertex_label = tk.Label(input_frame, text="Количество вершин:")
        vertex_label.pack(side=tk.LEFT)
        self.vertex_input = tk.Spinbox(input_frame, from_=1, to=100, width=5)
        self.vertex_input.pack(side=tk.LEFT, padx=5)

        # Количество гиперребер
        hyperedge_label = tk.Label(input_frame, text="Количество гиперребер:")
        hyperedge_label.pack(side=tk.LEFT)
        self.hyperedge_input = tk.Spinbox(input_frame, from_=1, to=100, width=5)
        self.hyperedge_input.pack(side=tk.LEFT, padx=5)

        # Ввод гиперребер вручную
        manual_hyperedges_label = tk.Label(input_frame, text="Введите гиперребра вручную (например, {1,2,3}):")
        manual_hyperedges_label.pack(pady=5)
        self.manual_hyperedges_input = tk.Text(input_frame, height=5, width=30)
        self.manual_hyperedges_input.pack()

        # Кнопка генерации
        generate_button = tk.Button(self, text="Сгенерировать и посчитать", command=self.generate_and_cover)
        generate_button.pack(pady=10)

        # Нижняя часть для вывода графика
        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack()

    def generate_and_cover(self):
        num_vertices = int(self.vertex_input.get())
        num_hyperedges = int(self.hyperedge_input.get())

        # Поле ручного ввода
        manual_hyperedges_text = self.manual_hyperedges_input.get("1.0", tk.END).strip()

        hyperedges = []

        if manual_hyperedges_text:
            try:
                for line in manual_hyperedges_text.splitlines():
                    hyperedge = set(map(int, line.strip().strip('{}').split(',')))
                    hyperedges.append(hyperedge)

            except ValueError:
                print("Ошибка ввода гиперребер. Убедитесь, что они заданы в правильном формате.")
                return
        else:
            for _ in range(num_hyperedges):
                hyperedge_size = random.randint(2, min(10, num_vertices))
                hyperedge = set(random.sample(range(num_vertices), hyperedge_size))
                hyperedges.append(hyperedge)

        # print("Гиперграф: ", str(hyperedges))

        hypertree_width = hypertree_width_approximation(hyperedges)
        # print("Древовидная ширина графа: ", hypertree_width)

        # Визуализируем гиперграф
        self.visualize_hypergraph(hyperedges, hypertree_width)

    def visualize_hypergraph(self, hypergraph, hypertree_width):
        # Очищаем предыдущий график, если он есть
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        h = HnxHypergraph(hypergraph)

        hnx.drawing.draw(h, with_color=True)

        plt.title('Визуализация гиперграфа')
        plt.scatter([], [], color='blue', marker='.', label=f'Приближенная древовидная ширина: {hypertree_width}')
        plt.legend(title="Вывод")

        # Создаем FigureCanvasTkAgg для Tkinter
        figure = plt.gcf()
        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        plt.close(figure)


if __name__ == '__main__':
    app = HypergraphApp()
    app.mainloop()
