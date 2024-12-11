import random


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

    # Итеративный жадный алгоритм (простая эвристика)
    for _ in range(10):  # число итераций можно изменить для улучшения качества приближения
        ordering = list(range(num_nodes))
        random.shuffle(ordering)  # Перемешивание вершин для случайного старта

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


hypergraph = [{1, 3, 6, 7, 10, 12, 13, 16, 17},
              {0, 1, 6, 10, 12, 14, 18},
              {17, 4, 1, 7},
              {2, 6, 7, 8, 9, 11, 13, 15},
              {3, 5, 6, 10, 11, 12, 14, 15, 17},
              {8, 3, 4, 7},
              {0, 4, 8, 10, 11, 13, 16, 17, 18},
              {6, 7, 11, 15, 16},
              {8, 10, 13},
              {3, 5, 6}]

approximated_width = hypertree_width_approximation(hypergraph)
print(f"Приближенная древовидная ширина: {approximated_width}")
