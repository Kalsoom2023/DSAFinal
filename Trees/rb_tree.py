import pygame
import sys
import time

# Node class for Red-Black Tree
class RBTreeNode:
    def __init__(self, key, color="Red"):
        self.key = key
        self.color = color  
        self.left = None
        self.right = None
        self.parent = None


# Red-Black Tree class
class RBTree:
    def __init__(self):
        self.TNULL = RBTreeNode(None, "Black")  # Sentinel node for NULL
        self.root = self.TNULL

    # Rotate left
    def _rotate_left(self, node):
        y = node.right
        node.right = y.left
        if y.left != self.TNULL:
            y.left.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    # Rotate right
    def _rotate_right(self, node):
        y = node.left
        node.left = y.right
        if y.right != self.TNULL:
            y.right.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

    # Fix the tree after insertion
    def _fix_insert(self, k):
        while k.parent.color == "Red":
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == "Red":  # Case 1: Uncle is red
                    u.color = "Black"
                    k.parent.color = "Black"
                    k.parent.parent.color = "Red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:  # Case 2: k is a right child
                        k = k.parent
                        self._rotate_left(k)
                    # Case 3: k is a left child
                    k.parent.color = "Black"
                    k.parent.parent.color = "Red"
                    self._rotate_right(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == "Red":  # Case 1: Uncle is red
                    u.color = "Black"
                    k.parent.color = "Black"
                    k.parent.parent.color = "Red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:  # Case 2: k is a left child
                        k = k.parent
                        self._rotate_right(k)
                    # Case 3: k is a right child
                    k.parent.color = "Black"
                    k.parent.parent.color = "Red"
                    self._rotate_left(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "Black"

    # Insert a node
    def insert(self, key):
        node = RBTreeNode(key)
        node.parent = None
        node.key = key
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "Red"

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = "Black"
            return

        if node.parent.parent is None:
            return

        self._fix_insert(node)

    # Fix the tree after deletion
    def _fix_delete(self, x):
        while x != self.root and x.color == "Black":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "Red":  
                    s.color = "Black"
                    x.parent.color = "Red"
                    self._rotate_left(x.parent)
                    s = x.parent.right
                if s.left.color == "Black" and s.right.color == "Black":  # Case 2: Both children are black
                    s.color = "Red"
                    x = x.parent
                else:
                    if s.right.color == "Black":  # Case 3: Right child is black
                        s.left.color = "Black"
                        s.color = "Red"
                        self._rotate_right(s)
                        s = x.parent.right
                    s.color = x.parent.color  # Case 4: Recolor and rotate
                    x.parent.color = "Black"
                    s.right.color = "Black"
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "Red":  # Case 1: Sibling is red
                    s.color = "Black"
                    x.parent.color = "Red"
                    self._rotate_right(x.parent)
                    s = x.parent.left
                if s.right.color == "Black" and s.left.color == "Black":  # Case 2: Both children are black
                    s.color = "Red"
                    x = x.parent
                else:
                    if s.left.color == "Black":  # Case 3: Left child is black
                        s.right.color = "Black"
                        s.color = "Red"
                        self._rotate_left(s)
                        s = x.parent.left
                    s.color = x.parent.color  # Case 4: Recolor and rotate
                    x.parent.color = "Black"
                    s.left.color = "Black"
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = "Black"

    # Delete a node
    def delete(self, key):
       
        node = self.search(key)
        if node == self.TNULL:
            print(f"Key {key} not found in the tree.")
            return

        y = node 
        y_original_color = y.color
        if node.left == self.TNULL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.TNULL:
            x = node.left
            self._transplant(node, node.left)
        else:
           
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y

            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color

        if y_original_color == "Black":
            self._fix_delete(x)

    def _transplant(self, u, v):
        """Replaces the subtree rooted at u with the subtree rooted at v."""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        """Finds the node with the minimum key in the subtree rooted at `node`."""
        while node.left != self.TNULL:
            node = node.left
        return node


    # Traversals (Inorder, Preorder, Postorder)
    def inorder(self):
        result = []
        self._inorder_helper(self.root, result)
        return result

    def _inorder_helper(self, node, result):
        if node != self.TNULL:
            self._inorder_helper(node.left, result)
            result.append(node.key)
            self._inorder_helper(node.right, result)

    def preorder(self):
        result = []
        self._preorder_helper(self.root, result)
        return result

    def _preorder_helper(self, node, result):
        if node != self.TNULL:
            result.append(node.key)
            self._preorder_helper(node.left, result)
            self._preorder_helper(node.right, result)

    def postorder(self):
        result = []
        self._postorder_helper(self.root, result)
        return result

    def _postorder_helper(self, node, result):
        if node != self.TNULL:
            self._postorder_helper(node.left, result)
            self._postorder_helper(node.right, result)
            result.append(node.key)

    def search(self, key):
        return self._search_helper(self.root, key)

    def _search_helper(self, node, key):
        if node == self.TNULL or key == node.key:
            return node
        if key < node.key:
            return self._search_helper(node.left, key)
        return self._search_helper(node.right, key)

def draw_rb(node, x, y, spacing, screen, font, highlight=None):
    if node and node.key is not None:  
    
        color = (255, 0, 0) if node.color == "Red" else (0, 0, 0)  
        highlight_color = (255, 255, 0) if highlight == node.key else color 
        
        # Draw the node
        pygame.draw.circle(screen, highlight_color, (x, y), 20)
        text = font.render(str(node.key), True, (255, 255, 255))  # White text
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

        # Draw left child
        if node.left and node.left.key is not None:
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x - spacing, y + 60), 2)
            draw_rb(node.left, x - spacing, y + 60, spacing // 2, screen, font, highlight)

        # Draw right child
        if node.right and node.right.key is not None:
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x + spacing, y + 60), 2)
            draw_rb(node.right, x + spacing, y + 60, spacing // 2, screen, font, highlight)


def draw_button(screen, text, x, y, width, height, font):
    # Create a rounded rectangle with a gradient effect
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
    # Colors for the input box
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
        draw_rb(tree.root, 400, 90, 200, screen, font, highlight=key) 
        pygame.display.flip()       
        time.sleep(0.5)              




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
        
       
        draw_rb(tree.root, 400, 50, 200, screen, font, highlight=result.key)
    

def search_traversal(node, key, screen, font):
    if node is not None:
       
        draw_rb(node, 400, 50, 200, screen, font, highlight=node.key)
        pygame.display.flip()
        time.sleep(0.5)  

       
        if key < node.key:
            search_traversal(node.left, key, screen, font)
        elif key > node.key:
            search_traversal(node.right, key, screen, font)
        else:
          
            draw_rb(node, 400, 50, 200, screen, font, highlight=node.key)
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
    title_text = font.render("Red Black Tree Visualizer", True, (70, 130, 180))
    screen.blit(title_text, (300, 20))

def search_feedback(tree, key, screen, font):
    screen.fill((255, 255, 255))
    pygame.display.flip()

 
    search_traversal(tree.root, key, screen, font)
    
 
   
def draw_complexity_info(screen, font):
    # Define the text and position
    complexity_info = [
        "RB Tree Complexities:",
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
    pygame.display.set_caption("Red-Black Tree Visualization")
    font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 36)

    clock = pygame.time.Clock()
    running = True

    input_text = ''
    while running:
        screen.fill((255, 255, 255)) 
        draw_title(screen, title_font)  
        draw_rb(tree.root, 400, 90, 200, screen, font) 

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
                    if input_text.isdigit():
                        tree.insert(int(input_text))
                        input_text = ''
                elif 160 <= event.pos[0] <= 280 and 500 <= event.pos[1] <= 550:
                    if input_text.isdigit():
                        tree.delete(int(input_text))
                        input_text = ''
                elif 300 <= event.pos[0] <= 420 and 500 <= event.pos[1] <= 550:
                    if input_text.isdigit():
                        search_feedback(tree, int(input_text), screen, font)
                        input_text = ''
                elif 440 <= event.pos[0] <= 560 and 500 <= event.pos[1] <= 550:
                    visualize_traversal(tree, tree.inorder(), screen, font)
                elif 580 <= event.pos[0] <= 700 and 500 <= event.pos[1] <= 550:
                    visualize_traversal(tree, tree.preorder(), screen, font)
                elif 720 <= event.pos[0] <= 840 and 500 <= event.pos[1] <= 550:
                    visualize_traversal(tree, tree.postorder(), screen, font)
            input_text, _ = handle_text_input(event, input_text)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


# Example usage
tree = RBTree()
visualize_bst_pygame(tree)

