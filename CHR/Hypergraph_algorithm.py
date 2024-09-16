import tkinter as tk
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def cover_with_stars(hypergraph):
    """
    Implements the hypergraph covering with stars problem.
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
    # Get hypergraph input from text box
    hypergraph = {}
    for i in range(len(vertex_entries)):
        vertex = vertex_entries[i].get()
        edges_str = edge_entries[i].get("1.0", tk.END).strip()
        edges = set(edges_str.split()) if edges_str else set()
        hypergraph[vertex] = edges

    # Run the algorithm
    stars = cover_with_stars(hypergraph)

    # Display the results
    result_label.config(text="Звезды, покрывающие гиперграф:")
    result_listbox.delete(0, tk.END)
    for i, star in enumerate(stars):
        result_listbox.insert(tk.END, f"Star {i + 1}: {star}")

    # Draw the hypergraph
    draw_hypergraph(hypergraph, stars)


def draw_hypergraph(hypergraph, stars):
    """
    Draws the hypergraph and its star cover using networkx,
    with different colors for each star cover.

    Args:
        hypergraph (dict): A dictionary representing the hypergraph, where keys are vertices and values are lists of edges incident to the vertex.
        stars (list): A list of star covers, each star cover is a list of edges.

    Returns:
        None
    """

    # Create a graph object
    graph = nx.Graph()

    # Add vertices
    graph.add_nodes_from(hypergraph.keys())

    # Add edges
    for vertex, edges in hypergraph.items():
        for edge in edges:
            graph.add_edge(vertex, edge)

    # Define colors for each star cover
    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']  # Add more colors as needed
    color_index = 0

    # Highlight edges in star covers with different colors
    for i, star in enumerate(stars):
        for edge in star:
            for vertex in hypergraph.keys():
                if edge in hypergraph[vertex]:
                    graph[edge][vertex]['color'] = colors[color_index]

        color_index = (color_index + 1) % len(colors)  # Cycle through colors

    # Draw the graph
    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(graph, with_labels=True, font_weight='bold', ax=ax, node_color='lightblue',
            edge_color=[graph[u][v].get('color', 'black') for u, v in graph.edges()])

    # Create Tkinter canvas and pack it
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def add_vertex():
    """
    Adds a new vertex input field to the interface.
    """
    global vertex_entries, edge_entries

    # Create a new frame for the vertex input
    vertex_frame = tk.Frame(input_frame)
    vertex_frame.pack(fill=tk.X)

    # Add vertex label and entry
    vertex_label = tk.Label(vertex_frame, text=f"Вершины {len(vertex_entries) + 1}:")
    vertex_label.pack(side=tk.LEFT)
    vertex_entry = tk.Entry(vertex_frame)
    vertex_entry.pack(side=tk.LEFT)
    vertex_entries.append(vertex_entry)

    # Add edge label and text box
    edge_label = tk.Label(vertex_frame, text="Грани:")
    edge_label.pack(side=tk.LEFT)
    edge_entry = tk.Text(vertex_frame, height=1, width=20)
    edge_entry.pack(side=tk.LEFT)
    edge_entries.append(edge_entry)


# Create the main window
window = tk.Tk()
window.title("Покрытие гиперграфа звездами")

# Input frame
input_frame = tk.Frame(window)
input_frame.pack()

# Initialize vertex and edge entry lists
vertex_entries = []
edge_entries = []

# Add initial vertex input field
add_vertex()

# Add vertex button
add_vertex_button = tk.Button(input_frame, text="Добавить вершину", command=add_vertex)
add_vertex_button.pack()

# Run button
run_button = tk.Button(window, text="Запуск алгоритма", command=run_algorithm)
run_button.pack()

# Result label and listbox
result_label = tk.Label(window, text="")
result_label.pack()
result_listbox = tk.Listbox(window, height=5)
result_listbox.pack()

# Frame for displaying the hypergraph
graph_frame = tk.Frame(window)
graph_frame.pack()

# Global variable for the canvas
canvas = None

window.mainloop()

# Example usage
# hypergraph = {'A': {'A1', 'A2', 'A3'},
# 'B': {'A1', 'B2', 'B3'},
# 'C': {'B2', 'C3', 'C4'},
# 'D': {'C3', 'D4', 'D5'}, }

# Stars covering the hypergraph:
# Star 1: {'A1', 'A3', 'A2'}
# Star 2: {'D5', 'C3', 'D4'}
# Star 3: {'B3', 'A1', 'B2'}
# Star 4: {'B2', 'C4', 'C3'}
