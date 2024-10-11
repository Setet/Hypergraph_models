import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QSpinBox, QFormLayout, \
    QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import hypernetx as hnx
import networkx as nx
import matplotlib.pyplot as plt

# Предопределённый набор цветов
COLORS = ['red', 'blue', 'yellow', 'darkgreen', 'lime', 'purple', 'pink']


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class HypergraphApp(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hypergraph Coloring")
        self.setMinimumSize(1000, 600)

        # Поля для ввода количества вершин и гиперрёбер
        self.vertices_input = QSpinBox()
        self.vertices_input.setMinimum(1)
        self.hyperedges_input = QSpinBox()
        self.hyperedges_input.setMinimum(1)
        self.hyperedges_input.valueChanged.connect(self.update_hyperedge_fields)

        # Динамически создаваемые поля для вершин гиперрёбер
        self.hyperedge_inputs = []

        # Кнопка для запуска
        self.run_button = QPushButton("Запустить")
        self.run_button.clicked.connect(self.run_hypergraph_coloring)

        # Метка для отображения результата
        self.result_label = QLabel("Минимальное количество цветов:")

        # Настраиваем область для графика
        self.graph_canvas = MplCanvas(self, width=8, height=6, dpi=100)

        # Вертикальный макет для формы ввода данных
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Введите количество вершин:"), self.vertices_input)
        form_layout.addRow(QLabel("Введите количество гиперрёбер:"), self.hyperedges_input)

        # Поля для ввода вершин гиперрёбер
        self.hyperedges_form_layout = QFormLayout()

        # Вертикальный макет для панели слева
        left_panel_layout = QVBoxLayout()
        left_panel_layout.addLayout(form_layout)
        left_panel_layout.addLayout(self.hyperedges_form_layout)

        # Пробел перед кнопкой
        left_panel_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка и метка внизу
        left_panel_layout.addWidget(self.run_button)
        left_panel_layout.addWidget(self.result_label)

        # Основной горизонтальный макет: панель слева, график справа
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_panel_layout)  # Панель слева
        main_layout.addWidget(self.graph_canvas)  # График справа

        self.setLayout(main_layout)

    def update_hyperedge_fields(self):
        # Удаляем старые поля ввода для гиперрёбер
        while self.hyperedge_inputs:
            field = self.hyperedge_inputs.pop()
            self.hyperedges_form_layout.removeRow(field)

        # Добавляем новые поля для гиперрёбер
        for i in range(self.hyperedges_input.value()):
            hyperedge_input = QLineEdit()
            self.hyperedge_inputs.append(hyperedge_input)
            self.hyperedges_form_layout.addRow(f"Вершины для гиперрёбра e{i + 1}:", hyperedge_input)

    def run_hypergraph_coloring(self):
        # Получаем вершины
        vertices = [f'V{i + 1}' for i in range(self.vertices_input.value())]

        # Получаем гиперрёбра
        hyperedges = []
        for input_field in self.hyperedge_inputs:
            hyperedge_input = input_field.text().strip()
            if not hyperedge_input:
                self.result_label.setText("Ошибка: одно из гиперрёбер не задано.")
                return
            try:
                hyperedge = {f'V{int(v.strip())}' for v in hyperedge_input.split(',')}
                hyperedges.append(hyperedge)
            except ValueError:
                self.result_label.setText("Ошибка: некорректный ввод вершин в гиперребре.")
                return

        # Проверяем, чтобы гиперрёбра не были пустыми
        if not hyperedges:
            self.result_label.setText("Ошибка: необходимо задать хотя бы одно гиперребро.")
            return

        # Создаем Обычный граф G
        G = nx.Graph()
        G.add_nodes_from(vertices)
        for hyperedge in hyperedges:
            # Добавляем ребра между всеми парами вершин в гиперребре
            for v1 in hyperedge:
                for v2 in hyperedge:
                    if v1 != v2:
                        G.add_edge(v1, v2)

        # Выполняем раскраску гиперграфа
        vertex_colors, num_colors = color_hypergraph(G)

        # Обновляем метку с минимальным количеством цветов
        self.result_label.setText(f"Минимальное количество цветов: {num_colors}")

        # Отрисовываем гиперграф внутри PyQt
        self.plot_colored_hypergraph(vertices, hyperedges, vertex_colors, num_colors)

    def plot_colored_hypergraph(self, vertices, hyperedges, vertex_colors, num_colors):
        self.graph_canvas.axes.clear()  # Очищаем старый график

        # Создание гиперграфа
        H = hnx.Hypergraph({f"e{i + 1}": list(hyperedge) for i, hyperedge in enumerate(hyperedges)})

        # Создание графа для рисования
        G = nx.Graph()
        G.add_nodes_from(vertices)
        for hyperedge in hyperedges:
            for v1 in hyperedge:
                for v2 in hyperedge:
                    if v1 != v2:
                        G.add_edge(v1, v2)

        pos = nx.spring_layout(G)  # Получаем позиции вершин

        # Рисуем гиперрёбра с помощью hypernetx
        hnx.draw(H, pos=pos, with_node_labels=False, edges_kwargs={"linewidth": 2}, ax=self.graph_canvas.axes)

        # Настраиваем цветовую карту для вершин на основе их цветов
        node_colors = [COLORS[vertex_colors[v] % len(COLORS)] for v in vertices]

        # Рисуем вершины
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=300, ax=self.graph_canvas.axes)

        # Рисуем метки вершин
        nx.draw_networkx_labels(G, pos, labels={v: v for v in vertices}, font_size=12, ax=self.graph_canvas.axes)

        self.graph_canvas.draw()  # Отображаем график на экране


def color_hypergraph(G):
    # Инициализация цветов для вершин
    vertex_colors = {}

    # Получаем список вершин графа
    vertices = list(G.nodes())

    # Перебираем вершины в порядке их количества соседей (наибольшее число сначала)
    vertices_sorted = sorted(vertices, key=lambda v: len(G[v]), reverse=True)

    for vertex in vertices_sorted:
        # Находим все цвета соседей
        neighbor_colors = {vertex_colors[neighbor] for neighbor in G[vertex] if neighbor in vertex_colors}

        # Присваиваем вершине минимальный возможный цвет, который еще не использован соседями
        color = 0
        while color in neighbor_colors:
            color += 1

        vertex_colors[vertex] = color

    # Максимальный цвет + 1 будет количеством используемых цветов
    num_colors = max(vertex_colors.values()) + 1

    return vertex_colors, num_colors


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HypergraphApp()
    window.show()
    sys.exit(app.exec_())
