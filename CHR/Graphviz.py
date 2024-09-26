import graphviz


def create_hypergraph_dot(hyperedges):
    """
    Создает строку в формате DOT для представления гиперграфа.

    Args:
      hyperedges: Список гиперребер. Каждое гиперребро - это список узлов.

    Returns:
      Строка в формате DOT.
    """

    dot_string = 'digraph G {\n'
    for i, edge in enumerate(hyperedges):
        # Добавляем гиперребро как узел
        dot_string += f'  E{i + 1} [shape=box, label="Hyperedge {i + 1}"];\n'
        # Соединяем узлы гиперребра с гиперребром
        for node in edge:
            dot_string += f'  {node} -> E{i + 1};\n'

    dot_string += '}'
    return dot_string


# Пример использования
hyperedges = [
    ['A', 'B', 'C'],
    ['B', 'D', 'E'],
    ['A', 'C', 'F'],
]

dot_string = create_hypergraph_dot(hyperedges)

# Создание и вывод графика
graph = graphviz.Source(dot_string)
graph.view()
