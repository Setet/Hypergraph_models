import tkinter
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter.ttk import Style
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def cover_with_stars(hypergraph):
    """
    Функция реализует задачу покрытия гиперграфа звездами.
    """
    stars = []
    uncovered_edges = {frozenset(edge) for edge in hypergraph.values()}

    while uncovered_edges:
        max_edge = max(uncovered_edges, key=lambda x: len(x - (x.union(*stars))))
        star = set(max_edge)
        stars.append(star)
        uncovered_edges.remove(max_edge)

    return stars


def run_algorithm():
    # Получаем гиперграфа из текстового поля
    hypergraph = {}
    for i in range(len(vertex_entries)):
        vertex = vertex_entries[i].get()
        edges_str = edge_entries[i].get("1.0", tk.END).strip()
        edges = set(edges_str.split()) if edges_str else set()
        hypergraph[vertex] = edges

    # Запускаем алгоритм
    stars = cover_with_stars(hypergraph)

    # Отображаю результаты
    result_listbox.delete(0, tk.END)
    for i, star in enumerate(stars):
        result_listbox.insert(tk.END, f"Звезда {i + 1}: {star}")

    print("Гиперграф - " + str(hypergraph))
    print("Звёзды - " + str(stars))

    # Рисуем гиперграф
    draw_hypergraph(hypergraph, stars)


def draw_hypergraph(hypergraph, stars):
    """
    Рисует гиперграф и его звездное покрытие с помощью networkx,
    с разными цветами для каждого звездного покрытия.

    Args:
        hypergraph (dict): Словарь, представляющий гиперграф, где ключами являются вершины,
         а значениями - списки ребер, инцидентных вершине.
        stars (список): Список звездных покрытий, каждое звездное покрытие - это список ребер.

    Возвращает:
        None
    """

    # Создаёт объект графа
    graph = nx.Graph()

    # Добавляем вершины
    graph.add_nodes_from(hypergraph.keys())

    # Добавляем рёбра
    for vertex, edges in hypergraph.items():
        for edge in edges:
            graph.add_edge(vertex, edge)

    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']
    color_index = 0

    # Выделите рёбра звезд разными цветами
    for i, star in enumerate(stars):
        for edge in star:
            for vertex in hypergraph.keys():
                if edge in hypergraph[vertex]:
                    graph[edge][vertex]['color'] = colors[color_index]

        # Чередуем цвета
        color_index = (color_index + 1) % len(colors)

    # Рисуем график
    nx.draw(graph, with_labels=True, font_weight='bold', node_color='lightblue',
            edge_color=[graph[u][v].get('color', 'black') for u, v in graph.edges()])

    canvas_fig.draw()
    canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def add_vertex():
    """
    Добавляет новое поле ввода vertex в интерфейс.
    """
    global vertex_entries, edge_entries

    vertex_frame = tk.Frame(input_frame)
    vertex_frame.pack(fill=tk.X)

    # Добавьте метку вершины и запись
    vertex_label = tk.Label(vertex_frame, text=f"Вершины {len(vertex_entries) + 1}:", font=('Arial', 15))
    vertex_label.pack(side=tk.LEFT)

    vertex_entry = tk.Entry(vertex_frame, font=('Arial', 15))
    vertex_entry.pack(side=tk.LEFT)
    vertex_entries.append(vertex_entry)

    # Добавьте метку и текстовое поле
    edge_label = tk.Label(vertex_frame, text="Грани:", font=('Arial', 15))
    edge_label.pack(side=tk.LEFT)

    edge_entry = tk.Text(vertex_frame, height=1, width=20, font=('Arial', 15))
    edge_entry.pack(side=tk.LEFT)
    edge_entries.append(edge_entry)


window = Tk()
window.title("Покрытие гиперграфа звездами")

input_frame = tk.Frame(window)
input_frame.pack()

# Инициализируем списки записей вершин и ребер
vertex_entries = []
edge_entries = []

# Добавляем поле ввода начальной вершины
add_vertex()

add_vertex_button = tk.Button(window, text="Добавить вершину", command=add_vertex, font=('Arial', 15))
add_vertex_button.pack()

run_button = tk.Button(window, text="Запуск алгоритма", command=run_algorithm, font=('Arial', 15))
run_button.pack()

# Результат метка и поля списка
result_label = tk.Label(window, text="Звезды, покрывающие гиперграф:", font=('Arial', 15))
result_label.pack()
result_listbox = tk.Listbox(window, height=5, font=('Arial', 15))
result_listbox.pack()

# Рамка для отображения гиперграфа
graph_frame = tk.Frame(window)
graph_frame.pack()

fig = plt.figure(figsize=(7, 7))
canvas_fig = FigureCanvasTkAgg(fig, master=window)
canvas_fig.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

# Глобальная переменная для холста
canvas = None

window.mainloop()

# Example usage
# hypergraph = {
# 'A': {'A1', 'A2', 'A3', 'D5'},
# 'B': {'A1', 'B2', 'B3'},
# 'C': {'B2', 'C3', 'C4'},
# 'D': {'C3', 'D4', 'D5'}, }

# Stars covering the hypergraph:
# Star 1: {'A1', 'A3', 'A2'}
# Star 2: {'D5', 'C3', 'D4'}
# Star 3: {'B3', 'A1', 'B2'}
# Star 4: {'B2', 'C4', 'C3'}
