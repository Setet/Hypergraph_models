def find_star_vertices(hypergraph):
    """
    Находит вершины звезды в гиперграфе.

    Args:
      hypergraph: Список множеств, представляющих ребра гиперграфа.

    Returns:
      Список вершин звезды.
    """

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


# Пример использования:
hypergraph = [{0, 1, 2, 3, 5, 6, 13, 14, 17},
              {1, 6, 9, 14, 16, 17},
              {2, 4, 6, 7, 9, 10, 15, 16, 17},
              {0, 1, 5},
              {2, 3, 6, 11, 12, 14, 16, 17, 19}]
star_vertices = find_star_vertices(hypergraph)
print("Вершины звезды:", star_vertices)
