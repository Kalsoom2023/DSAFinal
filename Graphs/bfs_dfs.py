import pygame
import sys
import math
from collections import deque

# Colors
WHITE, BLACK, BLUE, RED, GREEN, ORANGE, GREY, YELLOW = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 165, 0), (200, 200, 200), (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 670))
pygame.display.set_caption("Graph Traversal Visualization")
font = pygame.font.Font(None, 32)

# Speed Control Variable
speed = 0.5 

# Graph Representation
class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_id, position):
        self.nodes[node_id] = position
        self.edges[node_id] = []

    def add_edge(self, node1, node2):
        self.edges[node1].append(node2)  

def draw_nodes(screen, graph, visited_order, visiting_node, start_node):
    for node, (x, y) in graph.nodes.items():
        if node == start_node:
            color = BLUE
            label = "source"
        elif node == visiting_node:
            color = GREEN  # Yellow: currently visiting
            label = "visiting"
        elif node in visited_order:
            color = RED  # Green: visited
            label = str(visited_order[node])  
        else:
            color = ORANGE  # Orange: not visited
            label = ""

        pygame.draw.circle(screen, color, (x, y), 25)
        text = font.render(str(node), True, BLACK)
        screen.blit(text, text.get_rect(center=(x, y)))

        if label:
            label_text = font.render(label, True, BLACK)
            screen.blit(label_text, (x + 30, y - 15))

def draw_edges(screen, graph, highlighted_edges, visited_edges):
    for node1, neighbors in graph.edges.items():
        for node2 in neighbors:
            x1, y1 = graph.nodes[node1]
            x2, y2 = graph.nodes[node2]

            if (node1, node2) in highlighted_edges:
                color = RED  # Red: edge currently being traversed
            elif (node1, node2) in visited_edges:
                color = GREY  # Grey: already traversed edge
            else:
                color = BLACK  # Black: not traversed yet
            draw_arrow(screen, x1, y1, x2, y2, color)

def draw_arrow(screen, x1, y1, x2, y2, color):
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_length = 15
    arrow_angle = math.pi / 6

    end_x = x2 - 25 * math.cos(angle)
    end_y = y2 - 25 * math.sin(angle)
    pygame.draw.line(screen, color, (x1, y1), (end_x, end_y), 3)

    left_x = end_x - arrow_length * math.cos(angle - arrow_angle)
    left_y = end_y - arrow_length * math.sin(angle - arrow_angle)
    right_x = end_x - arrow_length * math.cos(angle + arrow_angle)
    right_y = end_y - arrow_length * math.sin(angle + arrow_angle)

    pygame.draw.polygon(screen, color, [(end_x, end_y), (left_x, left_y), (right_x, right_y)])

def draw_speed_bar(screen, speed):

    bar_x, bar_y, bar_width, bar_height = 50, 620, 300, 10
    handle_x = bar_x + int((speed - 0.1) / 1.9 * bar_width)
    
    pygame.draw.rect(screen, GREY, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.circle(screen, RED, (handle_x, bar_y + 5), 8) 
    text = font.render("Slow", True, BLACK)
    screen.blit(text, (370, 610))

def bfs_with_animation(graph, start_node, screen, speed):
    visited = {}
    queue = deque([start_node])
    order = 1
    highlighted_edges = []
    visited_edges = set()
    visiting_node = None  
    clock = pygame.time.Clock()

    while queue:
        node = queue.popleft()
        if node not in visited:
            visited[node] = order
            order += 1
            visiting_node = node 
            print(f"Visited Node {node}, Order: {visited[node]}")  
            for neighbor in graph.edges[node]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    highlighted_edges.append((node, neighbor))
                    visited_edges.add((node, neighbor))

            screen.fill((135, 206, 235))
            draw_edges(screen, graph, highlighted_edges, visited_edges)
            draw_nodes(screen, graph, visited, visiting_node, start_node)
            draw_speed_bar(screen, speed)
            pygame.display.flip()
            clock.tick(1 / speed)

    visiting_node = None
def draw_complexity(screen):
    text1 = font.render(f"Time Complexity: O(V + E)", True, BLACK)
    text2 = font.render(f"Space Complexity: O(V)", True, BLACK)
    screen.blit(text1, (800, 50))
    screen.blit(text2, (800, 90))
def dfs_with_animation(graph, start_node, screen, speed):
    visited = {}
    stack = [start_node]
    order = 1
    highlighted_edges = []
    visited_edges = set()
    visiting_node = None 
    clock = pygame.time.Clock()

    while stack:
        node = stack.pop()
        if node not in visited:
            visited[node] = order
            order += 1
            visiting_node = node
            print(f"Visited Node {node}, Order: {visited[node]}")  # Debugging
            for neighbor in reversed(graph.edges[node]):
                if neighbor not in visited:
                    stack.append(neighbor)
                    highlighted_edges.append((node, neighbor))
                    visited_edges.add((node, neighbor))

            screen.fill((135, 206, 235))
            draw_edges(screen, graph, highlighted_edges, visited_edges)
            draw_nodes(screen, graph, visited, visiting_node, start_node)
            draw_speed_bar(screen, speed)
            pygame.display.flip()
            clock.tick(1 / speed)

    visiting_node = None


def get_clicked_node(graph, mouse_pos):
    for node, (x, y) in graph.nodes.items():
        if math.hypot(mouse_pos[0] - x, mouse_pos[1] - y) <= 25:
            return node
    return None

def main():
    global speed
    graph = Graph()
    positions = [
        (100, 200), (100, 400), (250, 200), (250, 400), (400, 100),
        (400, 200), (400, 500), (550, 200), (550, 400), (700, 100),
        (700, 300), (700, 500), (850, 200), (850, 400), (1000, 400)
    ]
    for i, pos in enumerate(positions):
        graph.add_node(i, pos)
    edges = [
        (0, 1), (0, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8),
        (6, 9), (7, 10), (8, 11), (9, 12), (10, 13), (11, 14),(3,7)
    ]
    for edge in edges:
        graph.add_edge(*edge)

    running, start_node = True, None
    highlighted_edges = []  
    visited_edges = set() 

    while running:
        screen.fill((0, 191, 255))
        draw_edges(screen, graph, highlighted_edges, visited_edges)  
        draw_nodes(screen, graph, {},None, start_node)  
        draw_speed_bar(screen, speed)
        draw_complexity(screen)
        instructions = font.render("Click a Node | Press B for BFS, D for DFS | Adjust Speed Below", True, BLACK)
        screen.blit(instructions, (50, 580))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE):
                      running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 50 <= x <= 350 and 620 - 5 <= y <= 630 + 5:  # Speed bar area
                    speed = 0.1 + (x - 50) / 300 * 1.9
                else:
                    clicked_node = get_clicked_node(graph, (x, y))
                    if clicked_node is not None:
                        start_node = clicked_node
                        print(f"Start Node Selected: {start_node} {clicked_node}") 

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    print(f"Starting BFS from node {start_node}") 
                   
                    bfs_with_animation(graph, start_node, screen, speed)
                elif event.key == pygame.K_d:
                    print(f"Starting DFS from node {start_node}") 

                    dfs_with_animation(graph, start_node, screen, speed)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
