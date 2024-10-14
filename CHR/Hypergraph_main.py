import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from hypernetx import Hypergraph as HnxHypergraph
import hypernetx as hnx


# Функция покрытие гиперграфа звездами с помощью жадного алгоритма.
def find_star_vertices(hypergraph):
    # Создаем словарь для хранения количества ребер, содержащих каждую вершину.
    vertex_counts = {}
    for edge in hypergraph:
        for vertex in edge:
            if vertex not in vertex_counts:
                vertex_counts[vertex] = 0
            vertex_counts[vertex] += 1

    # Находим вершины, которые принадлежат максимальному количеству ребер.
    max_count = max(vertex_counts.values())
    star_vertices = [vertex for vertex, count in vertex_counts.items() if count == max_count]

    return star_vertices


class HypergraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.graph_frame = None
        self.manual_hyperedges_input = None
        self.hyperedge_input = None
        self.vertex_input = None

        self.title("Покрытие гиперграфа звездами")
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
        generate_button = tk.Button(self, text="Сгенерировать и найти покрытие", command=self.generate_and_cover)
        generate_button.pack(pady=10)

        # Нижняя часть для вывода графика
        self.graph_frame = tk.Frame(self)
        self.graph_frame.pack()

    # Создание гиперграфа
    def generate_and_cover(self):
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

        #         h = HnxHypergraph(hypergraph)
        #         print(h)
        print("Гиперграф: ", str(hyperedges))

        # Находим покрытие звездами
        star_covering = find_star_vertices(hyperedges)
        print("Покрытие звездами: ", star_covering)

        # Визуализируем гиперграф с покрытием звездами
        self.visualize_hypergraph_with_star_covering(hyperedges, star_covering)

    # Визуализация гиперграфа
    def visualize_hypergraph_with_star_covering(self, hypergraph, star_covering):
        # Очищаем предыдущий график, если он есть
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        # Создаем объект гиперграфа из списка ребер
        h = HnxHypergraph(hypergraph)
        print(str(h))

        # Рисуем гиперграф
        hnx.drawing.draw(h, with_color=True)

        plt.title('Визуализация гиперграфа с покрытием звездами')

        # Выделяем звезды (окрашиваем центральные вершины в голубой)
        for center_vertex in star_covering:
            plt.scatter([], [], color='blue', marker='*', label=f'Вершина №{center_vertex}')
            # plt.plot(B[center_vertex].nonzero()[0], B[center_vertex].nonzero()[1], 'bo', markersize=10)
        plt.legend(title="Звёзды")

        # Создаем FigureCanvasTkAgg для Tkinter
        figure = plt.gcf()
        canvas = FigureCanvasTkAgg(figure, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(figure)


if __name__ == '__main__':
    app = HypergraphApp()
    app.mainloop()
