from collections import defaultdict


def hypergraph_star_covering(hypergraph):
    """
    Решает задачу покрытия гиперграфа звёздами.

    Args:
        hypergraph: Список множеств, представляющий гиперграф.

    Returns:
        Словарь, где ключи - номера звёзд, а значения - кортежи из
        списка гиперрёбер звезды и её центра.
    """

    stars = {}
    used_edges = set()

    # Проходим по всем гиперрёбрам
    for i, edge in enumerate(hypergraph):
        # Если гиперрёбро ещё не использовано
        if i not in used_edges:
            # Находим центр звезды
            center = list(edge)[0]
            # Собираем гиперрёбра звезды
            star_edges = [edge]
            for j, other_edge in enumerate(hypergraph):
                # Если центр звезды находится в другом гиперрёбре
                if center in other_edge and j != i:
                    # Добавляем гиперрёбро в звезду и помечаем его как использованное
                    star_edges.append(other_edge)
                    used_edges.add(j)

            # Добавляем звезду в словарь
            stars[len(stars) + 1] = (star_edges, center)

    # Выводим результат
    for star_id, (star_edges, center) in stars.items():
        print(f"Звезда №{star_id} - {star_edges}: центр = {center}")


# Пример использования
hypergraph = [
    {1, 3, 9},
    {1, 5, 10},
    {1, 6, 11},
    {2, 4, 12},
    {2, 7, 13},
    {2, 8, 14},
    {1, 4, 9},
    {2, 6, 13}
]

hypergraph_star_covering(hypergraph)
