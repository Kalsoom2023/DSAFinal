import pygame
import sys
import time

# Node class for AVL Tree
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

# AVL Tree class
class AVL:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def right_rotate(self, y):
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))

        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node  

        
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

        
        balance = self.get_balance(node)

       
        if balance > 1 and key < node.left.key:
            return self.right_rotate(node)

       
        if balance < -1 and key > node.right.key:
            return self.left_rotate(node)

      
        if balance > 1 and key > node.left.key:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

       
        if balance < -1 and key < node.right.key:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        # Update height
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    
        balance = self.get_balance(node)

     
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.right_rotate(node)

      
        if balance > 1 and self.get_balance(node.left) < 0:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.left_rotate(node)

     
        if balance < -1 and self.get_balance(node.right) > 0:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

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
def visualize_traversal(tree, traversal, screen, font):
    for key in traversal:

        screen.fill((255, 255, 255))  
        draw_title(screen, font)  
        draw_avl(tree.root, 400, 90, 200, screen, font, highlight=key) 
        pygame.display.flip()  
        time.sleep(0.5)  
def draw_title(screen, font):
    title_text = font.render("AVL Tree Visualizer", True, (70, 130, 180))
    screen.blit(title_text, (320, 20))

def handle_text_input(event, current_text):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            current_text = current_text[:-1]
        elif event.key == pygame.K_RETURN:
            return current_text, True
        else:
            current_text += event.unicode
    return current_text, False
def draw_button(screen, text, x, y, width, height, font):
 
    button_rect = pygame.Rect(x, y, width, height)
    
    # Colors for the button
    color_start = (255, 255, 255)  
    color_end = (255, 255, 255)  
    border_color = (70, 130, 180) 
    border_width = 4 

    # Draw gradient background
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


# Visualization and interaction code (same structure as BST)
def draw_avl(node, x, y, spacing, screen, font, highlight=None):
    if node is not None:
        color = (255, 0, 0) if highlight == node.key else (0, 0, 255)
        pygame.draw.circle(screen, color, (x, y), 20)
        text = font.render(str(node.key), True, (255, 255, 255))
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

        if node.left is not None:
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x - spacing, y + 60), 2)
            draw_avl(node.left, x - spacing, y + 60, spacing // 2, screen, font, highlight)

        if node.right is not None:
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x + spacing, y + 60), 2)
            draw_avl(node.right, x + spacing, y + 60, spacing // 2, screen, font, highlight)
def draw_input_box(screen, font, text, x, y):
    # Colors for the input box
    border_color = (70, 130, 180) 
    background_color = (255, 255, 255)  
    text_color = (0, 0, 0)  
    placeholder_color = (150, 150, 150) 

    # Draw the background of the input box
    input_box_rect = pygame.Rect(x, y, 200, 30)
    pygame.draw.rect(screen, background_color, input_box_rect)
    
    # Draw the border around the input box
    pygame.draw.rect(screen, border_color, input_box_rect, 2)  

    # If text is empty, draw placeholder text
    if not text:
        placeholder_text = font.render("Enter value...", True, placeholder_color)
        screen.blit(placeholder_text, (x + 5, y + 5))  
    else:
       
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, (x + 5, y + 5))  
# Modify the main loop to use AVL

def draw_complexity_info(screen, font):
    # Define the text and position
    complexity_info = [
        "AVL Tree Complexities:",
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
def visualize_avl_pygame(tree):
    pygame.init()
    screen = pygame.display.set_mode((1200,670))
    pygame.display.set_caption("AVL Tree Visualization")
    font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()
    running = True
    input_text = ''

    while running:
        screen.fill((255, 255, 255))
        draw_title(screen, title_font)
        draw_avl(tree.root, 400, 90, 200, screen, font)

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
                        tree.insert(int(input_text))
                        input_text = ''
                elif 160 <= event.pos[0] <= 280 and 500 <= event.pos[1] <= 550:
                    if input_text:
                        tree.delete(int(input_text))
                        input_text = ''
                elif 300 <= event.pos[0] <= 420 and 500 <= event.pos[1] <= 550:
                    if input_text:
                        result = tree.search(int(input_text))
                        input_text = ''
                elif 440 <= event.pos[0] <= 560 and 500 <= event.pos[1] <= 550:
                    visualize_traversal(tree, tree.inorder(), screen, font)
                elif 580 <= event.pos[0] <= 700 and 500 <= event.pos[1] <= 550:
                    visualize_traversal(tree, tree.preorder(), screen, font)
                elif 720 <= event.pos[0] <= 840 and 500 <= event.pos[1] <= 550:
                    visualize_traversal(tree, tree.postorder(), screen, font)

            input_text, is_enter_pressed = handle_text_input(event, input_text)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

# Example usage
tree = AVL()
visualize_avl_pygame(tree)
