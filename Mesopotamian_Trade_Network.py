import networkx as nx
import matplotlib.pyplot as plt
import heapq

mesoCities = ["Eridu", "Ur", "Uruk", "Nippur", "Mari", "Assur", "Nineveh", "Ebla", "Kültepe"]
G = nx.Graph()
G.add_nodes_from(mesoCities)

routes = [
    ("Eridu", "Ur", 1),("Eridu", "Uruk", 1),("Eridu", "Nippur", 2),("Eridu", "Mari", 2),
    ("Eridu", "Assur", 3), ("Kültepe", "Assur", 1),("Kültepe", "Nineveh", 1), ("Kültepe", "Ebla", 2),
    ("Kültepe", "Mari", 3), ("Ur", "Uruk", 1),("Uruk", "Nippur", 1),("Nippur", "Mari", 2),
    ("Mari", "Assur", 2), ("Assur", "Nineveh", 2),("Nineveh", "Ebla", 1),("Ebla", "Ur", 3),
    ("Uruk", "Nineveh", 3),("Nippur", "Assur", 2),
]

G.add_weighted_edges_from(routes)

def dijkstra(graph, start_node):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    pq = [(0, start_node)]

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue
        for neighbor in graph.neighbors(curr_node):
            weight = graph[curr_node][neighbor]['weight']
            distance = curr_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances

erIdu = dijkstra(G, "Eridu")
kuLtep = dijkstra(G, "Kültepe")

betweenness = nx.betweenness_centrality(G, weight="weight", normalized=True)

closeness = nx.closeness_centrality(G, distance='weight')

listMeso = sorted(betweenness.items(), key=lambda x: -x[1])

print("\nMesopotamian Trade Network Stats")
print("="*40)

print(" Trade Hubs:")
for i, (city, score) in enumerate(listMeso):
    print(f"{i+1}. {city} — Influence Score: {score:.3f}")

print("\nShortest Routes:")
demo = [
    ("Eridu", "Nineveh"),
    ("Ur", "Ebla"),
    ("Mari", "Kültepe"),
    ("Uruk", "Assur"),
    ("Nippur", "Kültepe")
]

for source, target in demo:
    path = nx.shortest_path(G, source, target, weight="weight")
    length = nx.shortest_path_length(G, source, target, weight="weight")
    print(f"{source} → {target}: {' → '.join(path)} (Distance: {length})")

centralmesoCities = [city for city, _ in listMeso[:2]]

highlight_color = "#328E6E"
cityStates = "#9EC6F3"

pos = nx.spring_layout(G, k=0.8, weight='weight', seed=42)
plt.figure(figsize=(12, 8))

nx.draw_networkx_edges(G, pos, edge_color="gray", width=[3 if G[u][v]['weight']==1 else 1.5 for u,v in G.edges()], alpha=0.7)
nx.draw_networkx_nodes(
    G, pos,
    node_size=[4000 if node in centralmesoCities else 2000 for node in G.nodes()],
    node_color=[highlight_color if node in centralmesoCities else cityStates for node in G.nodes()],
    edgecolors="none",
    linewidths=2
)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"), font_size=8)

plt.title("Mesopotamian Trade Network", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
