import pygame


pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 670
BOX_WIDTH = 72
BOX_HEIGHT = 52
ARRAY_SIZE = 11
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Linear Search Visualizer")
font = pygame.font.Font(None, 36)
def draw_time_complexity():
    """Draw time complexity information on the screen."""
    time_text1 = font.render("Insert: O(1)", True, (0, 0, 0))  # Insert operation time complexity
    time_text2 = font.render("Delete: O(1)", True, (0, 0, 0))  # Delete operation time complexity
    time_text3 = font.render("Linear Search: O(n)", True, (0, 0, 0))  # Linear Search time complexity

    # Positioning text on the screen
    screen.blit(time_text1, (700, 100))  # Insert time complexity at position (50, 100)
    screen.blit(time_text2, (700, 150))  # Delete time complexity at position (50, 150)
    screen.blit(time_text3, (700, 200))  # Linear Search time complexity at position (50, 200)

# Functions
def draw_array(array, highlight=None, found_index=None):
    """Draws the array on the screen."""
    screen.fill(WHITE)
    
    start_x = (SCREEN_WIDTH - (ARRAY_SIZE * BOX_WIDTH)) // 2
    y = SCREEN_HEIGHT // 2 - BOX_HEIGHT // 2

    for i, value in enumerate(array):
        x = start_x + i * BOX_WIDTH
        if found_index == i:
            color = GREEN
        elif highlight == i:
            color = YELLOW
        else:
            color = CYAN
        
        pygame.draw.rect(screen, BLACK, (x, y, BOX_WIDTH, BOX_HEIGHT), 2)
        pygame.draw.rect(screen, color, (x + 2, y + 2, BOX_WIDTH - 4, BOX_HEIGHT - 4))

        font = pygame.font.SysFont(None, 36)
        text = font.render(str(value) if value is not None else "", True, RED)
        screen.blit(text, (x + BOX_WIDTH // 2 - text.get_width() // 2, y + BOX_HEIGHT // 2 - text.get_height() // 2))

        index_font = pygame.font.SysFont(None, 24)
        index_text = index_font.render(str(i), True, BLACK)
        screen.blit(index_text, (x + BOX_WIDTH // 2 - index_text.get_width() // 2, y + BOX_HEIGHT + 10))

def draw_label(x, y, text, font_size=24, color=BLACK):
    """Draws a label above or near UI elements."""
    font = pygame.font.SysFont(None, font_size)
    label = font.render(text, True, color)
    screen.blit(label, (x + 5, y - font_size - 5))

def draw_title(screen, font):
    """Draws the title at the top of the screen."""
    title_text = font.render("Array Visualizer", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 20))

def draw_text_box(x, y, width, height, text, active):
    """Draws a text input box."""
    color = GREEN if active else BLACK
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    
    font = pygame.font.SysFont(None, 32)
    input_text = font.render(text, True, BLACK)
    screen.blit(input_text, (x + 5, y + height // 2 - input_text.get_height() // 2))

def draw_button(x, y, width, height, text):
    """Draws a button."""
    pygame.draw.rect(screen, CYAN, (x, y, width, height))
    font = pygame.font.SysFont(None, 32)
    button_text = font.render(text, True, BLACK)
    screen.blit(button_text, (x + width // 2 - button_text.get_width() // 2, y + height // 2 - button_text.get_height() // 2))

def linear_search(array, target):
    """Performs a linear search with visualization."""
    for i, value in enumerate(array):
        yield i
        if value == target:
            yield i 
            return
    yield -1  

def main():
    # Variables
    array = [None] * ARRAY_SIZE
    input_value = ""
    input_index = ""
    active_field = None
    search_active = False
    search_index = None
    target_value = None
    found_index = None

    clock = pygame.time.Clock()
    running = True

    # UI Element Positions
    input_value_rect = pygame.Rect(50, 100, 150, 40)
    input_index_rect = pygame.Rect(50, 200, 150, 40)
    insert_button_rect = pygame.Rect(250, 100, 120, 40)
    delete_button_rect = pygame.Rect(250, 200, 120, 40)
    search_button_rect = pygame.Rect(450, 150, 160, 40)
    title_font = pygame.font.SysFont(None, 36)
     
    


    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_value_rect.collidepoint(event.pos):
                    active_field = "value"
                elif input_index_rect.collidepoint(event.pos):
                    active_field = "index"
                else:
                    active_field = None

                if insert_button_rect.collidepoint(event.pos):
                    if input_value.isdigit() and input_index.isdigit():
                        index = int(input_index)
                        value = int(input_value)
                        if 0 <= index < ARRAY_SIZE:
                            array[index] = value

                if delete_button_rect.collidepoint(event.pos):
                    if input_index.isdigit():
                        index = int(input_index)
                        if 0 <= index < ARRAY_SIZE:
                            array[index] = None

                if search_button_rect.collidepoint(event.pos):
                    if input_value.isdigit():
                        target_value = int(input_value)
                        search_active = True
                        search_index = linear_search(array, target_value)
                        found_index = None

            elif event.type == pygame.KEYDOWN:
                if active_field == "value":
                    if event.key == pygame.K_BACKSPACE:
                        input_value = input_value[:-1]
                    elif event.unicode.isdigit():
                        input_value += event.unicode
                elif active_field == "index":
                    if event.key == pygame.K_BACKSPACE:
                        input_index = input_index[:-1]
                    elif event.unicode.isdigit():
                        input_index += event.unicode

        # Linear search logic
        if search_active and search_index:
            try:
                current_index = next(search_index)
                if current_index == -1:
                    search_active = False
                elif array[current_index] == target_value:
                    found_index = current_index
                    search_active = False
                   
                    draw_array(array, highlight=current_index, found_index=current_index)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    found_index = None 
            except StopIteration:
                search_active = False

        # Drawing
        draw_array(array, highlight=current_index if search_active else None, found_index=found_index)

        # Draw UI
        draw_title(screen, title_font)

        # Draw Labels for Input Fields
        draw_label(input_value_rect.x, input_value_rect.y, "Value")
        draw_label(input_index_rect.x, input_index_rect.y, "Index")

        # Draw Text Boxes
        draw_text_box(input_value_rect.x, input_value_rect.y, input_value_rect.width, input_value_rect.height, input_value, active_field == "value")
        draw_text_box(input_index_rect.x, input_index_rect.y, input_index_rect.width, input_index_rect.height, input_index, active_field == "index")

        # Draw Buttons
        draw_button(insert_button_rect.x, insert_button_rect.y, insert_button_rect.width, insert_button_rect.height, "Insert")
        draw_button(delete_button_rect.x, delete_button_rect.y, delete_button_rect.width, delete_button_rect.height, "Delete")
        draw_button(search_button_rect.x, search_button_rect.y, search_button_rect.width, search_button_rect.height, "Linear Search")
        draw_time_complexity() 
        pygame.display.flip()
        clock.tick(3)

    pygame.quit()

if __name__ == "__main__":
    main()