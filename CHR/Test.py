import tkinter as tk
from tkinter import ttk
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from hypernetx import Hypergraph as HnxHypergraph
import hypernetx as hnx


class HypergraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Визуализация гиперграфа")
        self.geometry("500x500")

        self.create_widgets()

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
        generate_button = tk.Button(self, text="Сгенерировать и визуализировать", command=self.generate_hypergraph)
        generate_button.pack(pady=10)

        # Нижняя часть для вывода графика
        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack()

    def generate_hypergraph(self):
        num_vertices = int(self.vertex_input.get())
        num_hyperedges = int(self.hyperedge_input.get())
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

        hypergraph = HnxHypergraph(hyperedges)
        articulation_points = self.find_articulation_points_in_hypergraph(hyperedges)
        print("Точки сочленения в гиперграфе:", articulation_points)
        self.visualize_hypergraph_with_articulation_points(hypergraph, articulation_points)

    def find_articulation_points_in_hypergraph(self, hyperedges):
        G = nx.Graph()
        for hyperedge in hyperedges:
            vertices = list(hyperedge)
            for i in range(len(vertices)):
                for j in range(i + 1, len(vertices)):
                    u, v = vertices[i], vertices[j]
                    G.add_edge(u, v)
        articulation_points = list(nx.articulation_points(G))
        return articulation_points

    def visualize_hypergraph_with_articulation_points(self, hypergraph, articulation_points):
        # Очищаем предыдущий график, если он есть
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Рисуем график
        B = hypergraph.incidence_matrix()
        hnx.drawing.draw(hypergraph, with_color=True)
        plt.title('Визуализация гиперграфа с выделенными точками сочленения')
        for point in articulation_points:
            plt.scatter([], [], color='red', label=f'Точка сочленения: {point}')
        plt.legend()

        # Создаем FigureCanvasTkAgg для Tkinter
        figure = plt.gcf()
        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(figure)


if __name__ == '__main__':
    app = HypergraphApp()
    app.mainloop()
