import pygame
import sys
import time

# Node class for BST
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

# BST class
class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = BSTNode(key)
        else:
            self._insert(self.root, key)

    def _insert(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key)
            else:
                self._insert(node.left, key)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key)
            else:
                self._insert(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            successor = self._min_value_node(node.right)
            node.key = successor.key
            node.right = self._delete(node.right, successor.key)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def preorder(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node is not None:
            result.append(node.key)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.key)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None or node.key == key:
            return node
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

# Function to draw the BST
def draw_bst(node, x, y, spacing, screen, font, highlight=None):
    if node is not None:
        color = (255, 0, 0) if highlight == node.key else (0, 0, 255)
        pygame.draw.circle(screen, color, (x, y), 20)
        text = font.render(str(node.key), True, (255, 255, 255))
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

        # Draw left child
        if node.left is not None:
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x - spacing, y + 60), 2)
            draw_bst(node.left, x - spacing, y + 60, spacing // 2, screen, font, highlight)

        # Draw right child
        if node.right is not None:
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x + spacing, y + 60), 2)
            draw_bst(node.right, x + spacing, y + 60, spacing // 2, screen, font, highlight)

def draw_button(screen, text, x, y, width, height, font):
    button_rect = pygame.Rect(x, y, width, height)
    
    color_start = (255, 255, 255)  
    color_end = (255, 255, 255)  
    border_color = (70, 130, 180) 
    border_width = 4  

   
    for i in range(height):
        color = (
            int(color_start[0] + (color_end[0] - color_start[0]) * i / height),
            int(color_start[1] + (color_end[1] - color_start[1]) * i / height),
            int(color_start[2] + (color_end[2] - color_start[2]) * i / height)
        )
        pygame.draw.line(screen, color, (x, y + i), (x + width, y + i))

    
    pygame.draw.rect(screen, (255, 255, 255), button_rect, border_radius=15)
    
    
    pygame.draw.rect(screen, border_color, button_rect, width=border_width, border_radius=15)
    
    
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, (255, 255, 255, 100), button_rect, border_radius=15, width=2)  # White border on hover




def handle_text_input(event, current_text):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            current_text = current_text[:-1]
        elif event.key == pygame.K_RETURN:
            return current_text, True
        else:
            current_text += event.unicode
    return current_text, False


def draw_input_box(screen, font, text, x, y):
    
    border_color = (70, 130, 180) 
    background_color = (255, 255, 255)  
    text_color = (0, 0, 0) 
    placeholder_color = (150, 150, 150) 

    input_box_rect = pygame.Rect(x, y, 200, 30)
    pygame.draw.rect(screen, background_color, input_box_rect)
    
    # Draw the border around the input box
    pygame.draw.rect(screen, border_color, input_box_rect, 2)  

   
    if not text:
        placeholder_text = font.render("Enter value...", True, placeholder_color)
        screen.blit(placeholder_text, (x + 5, y + 5)) 
    else:
        # Render the actual user input text
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, (x + 5, y + 5)) 



def visualize_traversal(tree, traversal, screen, font):
    for key in traversal:
       
        screen.fill((255, 255, 255))  
        draw_title(screen, font)  
        draw_bst(tree.root, 400, 90, 200, screen, font, highlight=key)  
        pygame.display.flip() 
        time.sleep(0.5)  


# Function to draw a message on the screen
def draw_message(screen, message, font):
    text = font.render(message, True, (0, 0, 0))
    screen.blit(text, (20, 550))
    pygame.display.flip()
    time.sleep(1)  

# Insert feedback function
def insert_feedback(tree, key, screen, font):
    tree.insert(key)

# Delete feedback function
def delete_feedback(tree, key, screen, font):
    tree.delete(key)

# Search feedback function
def search_feedback(tree, key, screen, font):
    result = tree.search(key)
    if result:
       
        screen.fill((255, 255, 255))
        pygame.display.flip()
        
        search_traversal(tree.root, key, screen, font)
        
        draw_bst(tree.root, 400, 50, 200, screen, font, highlight=result.key)
    

def search_traversal(node, key, screen, font):
    if node is not None:
        draw_bst(node, 400, 50, 200, screen, font, highlight=node.key)
        pygame.display.flip()
        time.sleep(0.5)  

  
        if key < node.key:
            search_traversal(node.left, key, screen, font)
        elif key > node.key:
            search_traversal(node.right, key, screen, font)
        else:
            draw_bst(node, 400, 50, 200, screen, font, highlight=node.key)
            pygame.display.flip()
            time.sleep(0.5)

            message = font.render("Node found!", True, (0, 0, 0))
            screen.blit(message, (400 - message.get_width() // 2, 450))
            pygame.display.flip()
            time.sleep(1)  
            return  

    else:
        pygame.display.flip()
        time.sleep(0.5)

def draw_title(screen, font):
    title_text = font.render("Binary Search Tree Visualizer", True, (70, 130, 180))
    screen.blit(title_text, (300, 20))
def search_feedback(tree, key, screen, font):
    screen.fill((255, 255, 255))
    pygame.display.flip()

    search_traversal(tree.root, key, screen, font)
    
   
def draw_complexity_info(screen, font):
    # Define the text and position
    complexity_info = [
        "BST Tree Complexities:",
        "",  # Blank line for spacing
        "Insert: O(log n)",
        "Delete: O(log n)",
        "Search: O(log n)",
        "Inorder Traversal: O(n)",
        "Preorder Traversal: O(n)",
        "Postorder Traversal: O(n)",
        "Space Complexity: O(n)"
    ]

    x_start = 850  # Position on the right side
    y_start = 100
    line_spacing = 30

    for i, line in enumerate(complexity_info):
        color = (70, 130, 180)  # Black color for text
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (x_start, y_start + i * line_spacing))
def visualize_bst_pygame(tree):
    pygame.init()
    screen = pygame.display.set_mode((1200, 670))
    pygame.display.set_caption("Binary Search Tree Visualization")
    font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()
    running = True

    input_text = ''
    while running:
        screen.fill((255, 255, 255))
        draw_title(screen, title_font)

        draw_bst(tree.root, 400, 90, 200, screen, font)

        # Draw buttons and input box
        draw_button(screen, "Insert", 20, 500, 120, 50, font)
        draw_button(screen, "Delete", 160, 500, 120, 50, font)
        draw_button(screen, "Search", 300, 500, 120, 50, font)
        draw_button(screen, "Inorder", 440, 500, 120, 50, font)
        draw_button(screen, "Preorder", 580, 500, 120, 50, font)
        draw_button(screen, "Postorder", 720, 500, 120, 50, font)
        draw_input_box(screen, font, input_text, 324, 440)
        draw_complexity_info(screen, font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= event.pos[0] <= 140 and 500 <= event.pos[1] <= 550:
                 
                    if input_text:
                        insert_feedback(tree, int(input_text), screen, font)
                        input_text = '' 
                elif 160 <= event.pos[0] <= 280 and 500 <= event.pos[1] <= 550:
                 
                    if input_text:
                        delete_feedback(tree, int(input_text), screen, font)
                        input_text = ''  
                elif 300 <= event.pos[0] <= 420 and 500 <= event.pos[1] <= 550:
                    # Search button clicked
                    if input_text:
                        search_feedback(tree, int(input_text), screen, font)
                        input_text = ''  
                elif 440 <= event.pos[0] <= 560 and 500 <= event.pos[1] <= 550:
                    # Inorder button clicked
                    inorder_traversal = tree.inorder()
                    visualize_traversal(tree, inorder_traversal, screen, font)
                elif 580 <= event.pos[0] <= 700 and 500 <= event.pos[1] <= 550:
                    # Preorder button clicked
                    preorder_traversal = tree.preorder()
                    visualize_traversal(tree, preorder_traversal, screen, font)
                elif 720 <= event.pos[0] <= 840 and 500 <= event.pos[1] <= 550:
                    # Postorder button clicked
                    postorder_traversal = tree.postorder()
                    visualize_traversal(tree, postorder_traversal, screen, font)


            # Handle text input
            input_text, is_enter_pressed = handle_text_input(event, input_text)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# Example usage
tree = BST()
visualize_bst_pygame(tree)
