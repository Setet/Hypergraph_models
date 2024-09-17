def cover_with_stars(hypergraph):
    """ Реализует задачу о покрытии гиперграфа звездочками.
        Аргументы: гиперграф (dict): словарь, представляющий гиперграф. Ключами являются вершины,
    значениями - наборы ребер, к которым принадлежит вершина.
        Возвращает: список: список звездочек, покрывающих гиперграф.  """
    stars = []
    uncovered_edges = {frozenset(edge) for edge in hypergraph.values()}

    # Выбираем ребро с максимальным количеством непокрытых вершин
    while uncovered_edges:
        max_edge = max(uncovered_edges, key=lambda x: len(x - (x.union(*stars))))
        star = set(max_edge)
        # Добавьте ребро к звезде и удалите ее с незакрытых рёбер
        stars.append(star)
        uncovered_edges.remove(max_edge)

    return stars


hypergraph = {'A': {'A1', 'A2', 'A3'},
              'B': {'A1', 'B2', 'B3'},
              'C': {'B2', 'C3', 'C4'},
              'D': {'C3', 'D4', 'D5'}, }

stars = cover_with_stars(hypergraph)
print("Звезды, покрывающие гиперграф:")
for i, star in enumerate(stars):
    print(f"Звезда {i + 1}: {star}")
