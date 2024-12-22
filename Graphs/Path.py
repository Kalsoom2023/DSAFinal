import pygame
import sys
import random
import heapq

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200,670
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Visualizer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  
BUTTON_COLOR = (70, 130, 180)  
BUTTON_HOVER_COLOR = (150, 150, 255)  

pygame.font.init()
font = pygame.font.SysFont("times new roman", 24)

# Graph variables
nodes = []
edges = []
distances = {}  # Dictionary to store distances from the source node
previous_nodes = {}  # For reconstructing the shortest path
path_edges = []  # List of edges part of the shortest path
checked_edges = []  # List of edges that have been checked during the algorithm
is_running = True
algorithm_running = False
font = pygame.font.Font(None, 36)
def draw_algorithm_complexity(screen):
        time_text3 = font.render(f"Time Complexity of Dijkstra: O(E log V)", True, (0,0,0))
        space_text3 = font.render(f"Space Complexity of Dijkstra: O(V)", True, (0,0,0))

        screen.blit(time_text3, (700,50))
        screen.blit(space_text3, (700,80))
# Dijkstra's Algorithm with edge checking
def dijkstra(source):
    global distances, previous_nodes, path_edges, checked_edges, algorithm_running
    path_edges = []  
    checked_edges = [] 
    distances = {node: float('inf') for node in nodes}
    previous_nodes = {node: None for node in nodes}
    distances[source] = 0

    pq = [(0, source)] 
    visited = set()

    algorithm_running = True  

    while pq and algorithm_running:
        current_distance, current_node = heapq.heappop(pq)

        if current_node in visited:
            continue

        visited.add(current_node)

        for edge in edges:
            node1, node2, weight = edge
            if current_node == node1:
                neighbor = node2
            elif current_node == node2:
                neighbor = node1
            else:
                continue

            if neighbor in visited:
                continue

            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                checked_edges.append((node1, node2)) 
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

                draw_graph()
                pygame.display.flip()  
                pygame.time.wait(500)  

    for node in nodes:
        current_node = node
        path = []
        while previous_nodes[current_node] is not None:
            path.append((previous_nodes[current_node], current_node))
            current_node = previous_nodes[current_node]
        path.reverse()
        path_edges.extend(path)
    
    algorithm_running = False 

def draw_graph():
    screen.fill(WHITE)
    title_text = font.render("Dijkstra Visualizer", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    for edge in edges:
        node1, node2, weight = edge
        x1, y1 = node1
        x2, y2 = node2

        if (node1, node2) in checked_edges or (node2, node1) in checked_edges:
            pygame.draw.line(screen, YELLOW, (x1, y1), (x2, y2), 2)
        elif (node1, node2) not in path_edges and (node2, node1) not in path_edges:
            pygame.draw.line(screen, GRAY, (x1, y1), (x2, y2), 2)

        weight_text = font.render(str(weight), True, BLACK)
        screen.blit(weight_text, ((x1 + x2) // 2, (y1 + y2) // 2))

    for edge in path_edges:
        node1, node2 = edge
        x1, y1 = node1
        x2, y2 = node2
        pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 4)

    for x, y in nodes:
        pygame.draw.circle(screen, BLUE, (x, y), 10)

    pygame.display.flip()

def reset_graph():
    global nodes, edges, distances, previous_nodes, path_edges, checked_edges
    nodes = []
    edges = []
    distances = {}
    previous_nodes = {}
    path_edges = []
    checked_edges = []

    for _ in range(6):
        nodes.append((random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            weight = random.randint(1, 20)
            edges.append((nodes[i], nodes[j], weight))

    draw_graph()

def draw_buttons():
    dijkstra_button = pygame.Rect(50, HEIGHT - 50, 200, 40)
    reset_button = pygame.Rect(300, HEIGHT - 50, 200, 40)

    pygame.draw.rect(screen, BUTTON_COLOR, dijkstra_button)
    pygame.draw.rect(screen, BUTTON_COLOR, reset_button)

    dijkstra_text = font.render("Dijkstra's Algorithm", True, WHITE)
    reset_text = font.render("Reset Graph", True, WHITE)

    screen.blit(dijkstra_text, (dijkstra_button.x + 10, dijkstra_button.y + 10))
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 10))

    return dijkstra_button, reset_button

def main():
    global is_running, previous_nodes, algorithm_running
    reset_graph()
    draw_algorithm_complexity(screen)

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and not algorithm_running:  
                    source_node = random.choice(nodes)
                    previous_nodes = dijkstra(source_node)
                    draw_graph()
                elif event.key == pygame.K_r:  
                    reset_graph()
                    draw_algorithm_complexity(screen)
                    draw_graph()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                dijkstra_button, reset_button = draw_buttons()

                if dijkstra_button.collidepoint(mouse_x, mouse_y) and not algorithm_running:
                    source_node = random.choice(nodes)
                    previous_nodes = dijkstra(source_node)
                    draw_graph()

                if reset_button.collidepoint(mouse_x, mouse_y):
                    reset_graph()
                    draw_algorithm_complexity(screen)
                    draw_graph()

        draw_buttons()

        pygame.display.update()

    pygame.quit()
    sys.exit()

main()
