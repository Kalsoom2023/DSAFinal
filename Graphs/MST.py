import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200,670
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kruskal and Prim Algorithm Visualizer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0) 
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (150, 150, 255) 

pygame.font.init()
font = pygame.font.SysFont("times new roman", 24)

# Graph variables
nodes = []
edges = []
mst_edges = []
is_running = True
font = pygame.font.Font(None, 28)
def draw_algorithm_complexity(screen):
   
    


    # Rendering the time and space complexities for Kruskal's Algorithm
    time_text = font.render(f"Time Complexity of Kruskal: O(E log E)", True, (0,0,0))
    space_text = font.render(f"Space Complexity of Kruskal: O(E + V)", True, (0,0,0))

    # Rendering the time and space complexities for Prim's Algorithm
    time_text2 = font.render(f"Time Complexity of Prim: O(E log V)", True, (0,0,0))
    space_text2 = font.render(f"Space Complexity of Prim: O(V)", True, (0,0,0))

    # Displaying the texts on the screen at specified positions
    screen.blit(time_text, (800,20))
    screen.blit(space_text, (800,40))
    screen.blit(time_text2, (800,60))
    screen.blit(space_text2, (800,80))
 
# Kruskal's Algorithm Helper Functions
def kruskal():
    parent = {}
    
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        if root1 != root2:
            parent[root2] = root1

    for node in nodes:
        parent[node] = node

    sorted_edges = sorted(edges, key=lambda x: x[2])
    mst = []

    for edge in sorted_edges:
        node1, node2, weight = edge
        if find(node1) != find(node2):
            union(node1, node2)
            mst.append(edge)

    return mst

# Prim's Algorithm Helper Functions
def prim():
    visited = set()
    mst = []
    
    current_node = random.choice(nodes)
    visited.add(current_node)

    edges_to_consider = [edge for edge in edges if current_node in edge[:2]]
    source_node = current_node 

    draw_graph(source_node=source_node)

    while len(visited) < len(nodes):
        edges_to_consider = [e for e in edges_to_consider if e[0] in visited or e[1] in visited]
        edges_to_consider = sorted(edges_to_consider, key=lambda x: x[2])

        for edge in edges_to_consider:
            node1, node2, weight = edge
            if node1 not in visited or node2 not in visited:
                mst.append(edge)
                visited.update([node1, node2])
                edges_to_consider.extend([e for e in edges if node1 in e[:2] or node2 in e[:2]])
                break

    return mst, source_node

def draw_graph(source_node=None):
    screen.fill(WHITE)  
    title_text = font.render("MST Visualizer", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    for edge in edges:
        node1, node2, weight = edge
        x1, y1 = node1
        x2, y2 = node2
        pygame.draw.line(screen, GRAY, (x1, y1), (x2, y2), 2)
        weight_text = font.render(str(weight), True, BLACK)
        screen.blit(weight_text, ((x1 + x2) // 2, (y1 + y2) // 2))

    for x, y in nodes:
        pygame.draw.circle(screen, BLUE, (x, y), 10)

    if source_node:
        sx, sy = source_node
        source_text = font.render(f"Source", True, RED)
        screen.blit(source_text, (sx + 12, sy - 12))  

    draw_buttons()

    pygame.display.flip()

def draw_mst(mst, source_node=None):
    for edge in edges:
        node1, node2, weight = edge
        x1, y1 = node1
        x2, y2 = node2
        pygame.draw.line(screen, GRAY, (x1, y1), (x2, y2), 2)
        weight_text = font.render(str(weight), True, BLACK)
        screen.blit(weight_text, ((x1 + x2) // 2, (y1 + y2) // 2))

    for i, edge in enumerate(mst):
        node1, node2, weight = edge
        x1, y1 = node1
        x2, y2 = node2
        pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 4)

        pygame.display.flip()

        pygame.time.delay(500) 

    for x, y in nodes:
        pygame.draw.circle(screen, BLUE, (x, y), 10)

    # Display source node label
    if source_node:
        sx, sy = source_node
        source_text = font.render(f"Source", True, RED)
        screen.blit(source_text, (sx + 12, sy - 12))  

    draw_buttons()

    pygame.display.flip()

def draw_buttons():
    kruskal_button = pygame.Rect(50, HEIGHT - 50, 200, 40)
    prim_button = pygame.Rect(300, HEIGHT - 50, 200, 40)
    reset_button = pygame.Rect(550, HEIGHT - 50, 200, 40)

    pygame.draw.rect(screen, BUTTON_COLOR, kruskal_button)
    pygame.draw.rect(screen, BUTTON_COLOR, prim_button)
    pygame.draw.rect(screen, BUTTON_COLOR, reset_button)

    kruskal_text = font.render("Kruskal's Algorithm", True, WHITE)
    prim_text = font.render("Prim's Algorithm", True, WHITE)
    reset_text = font.render("Reset Graph", True, WHITE)

    screen.blit(kruskal_text, (kruskal_button.x + 10, kruskal_button.y + 10))
    screen.blit(prim_text, (prim_button.x + 10, prim_button.y + 10))
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 10))

    return kruskal_button, prim_button, reset_button

def reset_graph():
    global nodes, edges, mst_edges
    nodes = []
    edges = []
    mst_edges = []

    for _ in range(6):
        nodes.append((random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            weight = random.randint(1, 20)
            edges.append((nodes[i], nodes[j], weight))

    draw_graph()

# Main Loop
def main():
    global is_running, mst_edges

    reset_graph()
    draw_algorithm_complexity(screen) 
    

    while is_running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                   
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k: 
                  
                    mst_edges = kruskal()
                    draw_mst(mst_edges)
                elif event.key == pygame.K_p:  
                   
                    mst_edges, source_node = prim()
                    draw_mst(mst_edges, source_node)  
                elif event.key == pygame.K_r: 
                    reset_graph()
                    draw_algorithm_complexity(screen) 

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                kruskal_button, prim_button, reset_button = draw_buttons()

                if kruskal_button.collidepoint(mouse_pos):
                    mst_edges = kruskal()
                    draw_mst(mst_edges)
                elif prim_button.collidepoint(mouse_pos):
                    mst_edges, source_node = prim()
                    draw_mst(mst_edges, source_node)
                elif reset_button.collidepoint(mouse_pos):
                    reset_graph()
                    draw_algorithm_complexity(screen) 

        pygame.display.update()

    pygame.quit()
    sys.exit()

main()
