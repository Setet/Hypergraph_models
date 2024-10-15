def cover_hypergraph_with_stars(hypergraph):
    """
    Алгоритм покрытия гиперграфа звёздами.

    Args:
        hypergraph: Список множеств, представляющих гиперребра.

    Returns:
        Список звезд, покрывающих все вершины.
    """

    # Список звезд
    stars = []
    # Множество непокрытых вершин
    uncovered_vertices = set().union(*hypergraph)
    i = 0

    # Цикл, пока есть непокрытые вершины
    while uncovered_vertices:
        # Выбираем произвольную непокрытую вершину
        vertex = uncovered_vertices.pop()

        # Находим гиперребра, содержащие выбранную вершину
        star = [edge for edge in hypergraph if vertex in edge]

        # Добавляем звезду в список звезд
        stars.append(star)

        # Удаляем покрытые вершины из множества непокрытых вершин
        uncovered_vertices.difference_update(set().union(*star))

        # Увеличиваем счетчик
        i += 1

    return stars


hypergraph = [{8, 17, 14},
              {4, 5, 6, 17, 19},
              {19, 6, 15},
              {1, 3, 14, 6},
              {2, 6, 7, 8, 10, 12, 17}]

stars = cover_hypergraph_with_stars(hypergraph)

# print(str(stars))

for i, star in enumerate(stars):
    print(f"Звезда {i + 1}: {star}")
