import matplotlib.pyplot as plt
import networkx as nx


def plot_hypergraph(hypergraph, node_labels=None, edge_labels=None):
    """
    Визуализирует гиперграф с помощью matplotlib.

    Args:
      hypergraph: Словарь, представляющий гиперграф. Ключи - узлы, значения - списки ребер,
        к которым принадлежит узел.
      node_labels: Словарь, сопоставляющий узлам метки.
      edge_labels: Словарь, сопоставляющий ребрам метки.
    """

    # Создаем объект графа NetworkX
    graph = nx.Graph()

    # Добавляем узлы
    graph.add_nodes_from(hypergraph.keys())

    # Добавляем ребра
    for node, edges in hypergraph.items():
        for edge in edges:
            graph.add_edge(node, edge)

    # Рисуем граф
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, labels=node_labels, node_size=500, node_color='skyblue')

    # Рисуем ребра
    for edge in set(sum(hypergraph.values(), [])):
        edge_nodes = [node for node in hypergraph.keys() if edge in hypergraph[node]]
        nx.draw_networkx_edges(graph, pos,
                               edgelist=[(edge_nodes[i], edge_nodes[i + 1]) for i in range(len(edge_nodes) - 1)],
                               width=2, edge_color='red')

    # Добавляем метки ребер
    if edge_labels:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)

    # Отображаем график
    plt.show()


# Пример использования
hypergraph = {
    'A': [1, 2, 3],
    'B': [2, 4, 5],
    'C': [3, 5, 6],
    'D': [1, 4, 6],
}

plot_hypergraph(hypergraph)
