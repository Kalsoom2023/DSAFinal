import pygame
import sys
from linearHashFunctions import HashTable
from hashAnimation import AnimationSteps
from doubleHashing import DoubleHashTable
from quadraticHashing import QuadraticHashTable

# colors
WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, event):
        if self.rect.collidepoint(event.pos):
            return True
        return False

# Linear HashTableVisualizer Class
class HashTableVisualizer:
    def __init__(self, size=10, screen_width=1200, screen_height=670):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Linear Probing Hash Table Visualization")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.hash_table = HashTable(size)
        self.animation_steps = AnimationSteps()
        self.input_text = ""
        self.input_active = False
        self.back_button = Button(500, 500, 200, 50, BLUE, "Back to Main")

    def insert(self, key):
        original_index, final_index, step_count = self.hash_table.insert(key)
        while self.hash_table.table[final_index] is None:
            self.animation_steps.add_probe_step(original_index, final_index, step_count)
        self.animation_steps.add_insertion_step(original_index, final_index, key, step_count)

    def draw_input_box(self):
        input_box_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 390, 200, 40)
        pygame.draw.rect(self.screen, (0, 0, 0), input_box_rect, 2)
        text_surface = self.font.render(self.input_text, True, BLACK)
        text_rect = text_surface.get_rect(center=input_box_rect.center)
        text = self.font.render("Enter Number", True, BLACK)
        text_r = text.get_rect(center=(self.screen_width // 2 - 200, 300))
        self.screen.blit(text, text_r)
        self.screen.blit(text_surface, text_rect)

    def draw_hash_table(self):        
        cell_width = self.screen_width // (self.hash_table.size + 2)
        cell_height = 50
        start_x = cell_width
        start_y = 100
        
        
        header = self.font.render("Linear Probing Hash Table", True, BLACK)
        header_rect = header.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(header, header_rect)
        
        # Draw each cell
        for i in range(self.hash_table.size):
           
            x = start_x + i * cell_width
            y = start_y
            
         
            rect = pygame.Rect(x, y, cell_width - 5, cell_height)
            
           
            color = WHITE
            if self.animation_steps.current_insertion_step:
               
                if (self.animation_steps.current_insertion_step['action'] == 'insert' and 
                    self.animation_steps.current_insertion_step['original_index'] == i):
                    color = BLUE
               
                elif (self.animation_steps.current_insertion_step['action'] == 'probe' and 
                      self.animation_steps.current_insertion_step['current_index'] == i):
                    color = RED
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
            index_text = self.small_font.render(str(i), True, BLACK)
            index_rect = index_text.get_rect(center=(x + cell_width // 2, y + cell_height + 15))
            self.screen.blit(index_text, index_rect)
            
          
            if self.hash_table.table[i] is not None:
                value_text = self.small_font.render(str(self.hash_table.table[i]), True, BLACK)
                value_rect = value_text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                self.screen.blit(value_text, value_rect)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked(event):
                        return "main"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.input_text:
                        try:
                            key = int(self.input_text)
                            self.insert(key)
                            self.input_text = ""
                        except ValueError:
                            self.input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.unicode.isdigit():
                        self.input_text += event.unicode
            self.screen.fill((173, 216, 230))
            self.draw_hash_table()
            self.draw_input_box()
            draw_complexities(self.screen, self.font, "linear")
            self.back_button.draw(self.screen, self.font)
            pygame.display.flip()
            clock.tick(30)
HASHING_COMPLEXITIES = {
    "linear": {
        "insertion": "Best: O(1), Worst: O(n)",
        "search": "Best: O(1), Worst: O(n)",
        "space": "O(n)"
    },
    "quadratic": {
        "insertion": "Best: O(1), Worst: O(n)",
        "search": "Best: O(1), Worst: O(n)",
        "space": "O(n)"
    },
    "double": {
        "insertion": "Best: O(1), Worst: O(n)",
        "search": "Best: O(1), Worst: O(n)",
        "space": "O(n)"
    },
}
def draw_complexities(screen, font, method):
    complexities = HASHING_COMPLEXITIES[method]
    insertion_text = font.render(f"Insertion: {complexities['insertion']}", True, BLACK)
    search_text = font.render(f"Search: {complexities['search']}", True, BLACK)
    space_text = font.render(f"Space: {complexities['space']}", True, BLACK)

    screen.blit(insertion_text, (20, 400))
    screen.blit(search_text, (20, 440))
    screen.blit(space_text, (20, 480))
            
            
class DoubleHashTableVisualizer:
    def __init__(self, size=10, screen_width=1200, screen_height=670):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Double Hash Table Visualization")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.doubleHash = DoubleHashTable(size)
        self.animation_steps = AnimationSteps()
        self.input_text = ""
        self.input_active = False
        self.back_button = Button(500, 500, 200, 50, BLUE, "Back to Main")

    def insert(self, key):
        original_index, final_index, step_count = self.doubleHash.insert(key)
        while self.doubleHash.table[final_index] is None:
            self.animation_steps.add_probe_step(original_index, final_index, step_count)
        self.animation_steps.add_insertion_step(original_index, final_index, key, step_count)

    def draw_input_box(self):
        input_box_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 390, 200, 40)
        pygame.draw.rect(self.screen, (0, 0, 0), input_box_rect, 2)
        text_surface = self.font.render(self.input_text, True, BLACK)
        text_rect = text_surface.get_rect(center=input_box_rect.center)
        text = self.font.render("Enter Number", True, BLACK)
        text_r = text.get_rect(center=(self.screen_width // 2 - 200, 300))
        self.screen.blit(text, text_r)
        self.screen.blit(text_surface, text_rect)

    def draw_hash_table(self):
      
        cell_width = self.screen_width // (self.doubleHash.size + 2)
        cell_height = 50
        start_x = cell_width
        start_y = 100
        
       
        header = self.font.render("Double Hash Table Visualization", True, BLACK)
        header_rect = header.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(header, header_rect)
        
        for i in range(self.doubleHash.size):
         
            x = start_x + i * cell_width
            y = start_y
            
            rect = pygame.Rect(x, y, cell_width - 5, cell_height)
            
            color = WHITE
            if self.animation_steps.current_insertion_step:
                
                if (self.animation_steps.current_insertion_step['action'] == 'insert' and 
                    self.animation_steps.current_insertion_step['original_index'] == i):
                    color = BLUE
               
                elif (self.animation_steps.current_insertion_step['action'] == 'probe' and 
                      self.animation_steps.current_insertion_step['current_index'] == i):
                    color = RED
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
          
            index_text = self.small_font.render(str(i), True, BLACK)
            index_rect = index_text.get_rect(center=(x + cell_width // 2, y + cell_height + 15))
            self.screen.blit(index_text, index_rect)
            
          
            if self.doubleHash.table[i] is not None:
                value_text = self.small_font.render(str(self.doubleHash.table[i]), True, BLACK)
                value_rect = value_text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                self.screen.blit(value_text, value_rect)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked(event):
                        return "main"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.input_text:
                        try:
                            key = int(self.input_text)
                            self.insert(key)
                            self.input_text = ""
                        except ValueError:
                            self.input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.unicode.isdigit():
                        self.input_text += event.unicode
            self.screen.fill((173, 216, 230))
            self.draw_hash_table()
            self.draw_input_box()
            draw_complexities(self.screen, self.font, "double")
            self.back_button.draw(self.screen, self.font)
            pygame.display.flip()
            clock.tick(30)

class QuadraticHashTableVisualizer:
    def __init__(self, size=10, screen_width=1200, screen_height=670):
        pygame.init()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Quadratic Hash Table Visualization")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.quadraticHash = QuadraticHashTable(size)
        self.animation_steps = AnimationSteps()
        self.input_text = ""
        self.input_active = False
        self.back_button = Button(500, 500, 200, 50, BLUE, "Back to Main")

    def insert(self, key):
        original_index, final_index, step_count = self.quadraticHash.insert(key)
        while self.quadraticHash.table[final_index] is None:
            self.animation_steps.add_probe_step(original_index, final_index, step_count)
        self.animation_steps.add_insertion_step(original_index, final_index, key, step_count)

    def draw_input_box(self):
        input_box_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height - 390, 200, 40)
        pygame.draw.rect(self.screen, (0, 0, 0), input_box_rect, 2)
        text_surface = self.font.render(self.input_text, True, BLACK)
        text_rect = text_surface.get_rect(center=input_box_rect.center)
        text = self.font.render("Enter Number", True, BLACK)
        text_r = text.get_rect(center=(self.screen_width // 2 - 200, 300))
        self.screen.blit(text, text_r)
        self.screen.blit(text_surface, text_rect)

    def draw_hash_table(self):
        # Calculate grid parameters
        cell_width = self.screen_width // (self.quadraticHash.size + 2)
        cell_height = 50
        start_x = cell_width
        start_y = 100
        
        # Draw table header
        header = self.font.render("Quadratic Hash Table Visualization", True, BLACK)
        header_rect = header.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(header, header_rect)
        
        # Draw each cell
        for i in range(self.quadraticHash.size):
            # Calculate position
            x = start_x + i * cell_width
            y = start_y
            
            # Draw cell rectangle
            rect = pygame.Rect(x, y, cell_width - 5, cell_height)
            
            # Color based on state
            color = WHITE
            if self.animation_steps.current_insertion_step:
             
                if (self.animation_steps.current_insertion_step['action'] == 'insert' and 
                    self.animation_steps.current_insertion_step['original_index'] == i):
                    color = BLUE
                
                elif (self.animation_steps.current_insertion_step['action'] == 'probe' and 
                      self.animation_steps.current_insertion_step['current_index'] == i):
                    color = RED
            
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            
            # Draw index
            index_text = self.small_font.render(str(i), True, BLACK)
            index_rect = index_text.get_rect(center=(x + cell_width // 2, y + cell_height + 15))
            self.screen.blit(index_text, index_rect)
            
           
            if self.quadraticHash.table[i] is not None:
                value_text = self.small_font.render(str(self.quadraticHash.table[i]), True, BLACK)
                value_rect = value_text.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
                self.screen.blit(value_text, value_rect)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked(event):
                        return "main"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.input_text:
                        try:
                            key = int(self.input_text)
                            self.insert(key)
                            self.input_text = ""
                        except ValueError:
                            self.input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.unicode.isdigit():
                        self.input_text += event.unicode
            self.screen.fill((173, 216, 230))
            self.draw_hash_table()
            self.draw_input_box()
            draw_complexities(self.screen, self.font, "quadratic")
            self.back_button.draw(self.screen, self.font)
            pygame.display.flip()
            clock.tick(30)

def main_page(screen, font):
    screen.fill((173, 216, 230))
    title_font = pygame.font.Font(None,80)
    title_text = title_font.render("Hashing Visualization", True, BLACK)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2 + 20, 100+20))
    screen.blit(title_text, title_rect)

    button1 = Button(400, 200, 300, 50, BLUE, "Linear Hashing")
    button2 = Button(400, 300, 300, 50, BLUE, "Quadratic Hashing")
    button3 = Button(400, 400, 300, 50, BLUE, "Double Hashing")
    button1.draw(screen, font)
    button2.draw(screen, font)
    button3.draw(screen, font)
    pygame.display.update()
    return button1, button2, button3

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 650))
    pygame.display.set_caption("Hashing")
    font = pygame.font.Font(None, 40)
    running = True
    page = "main"
    button1, button2, button3 = None, None, None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if page == "main":
                    if button1.is_clicked(event):
                        page = HashTableVisualizer().run()
                    elif button2.is_clicked(event):
                        page = QuadraticHashTableVisualizer().run()
                    elif button3.is_clicked(event):
                        page = DoubleHashTableVisualizer().run()
        if page == "main":
            button1, button2, button3 = main_page(screen, font)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
