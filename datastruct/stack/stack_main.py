import pygame
import sys
from stack_visualizer import StackVisualizer
import random

pygame.init()
from stack import Stack


screen_width, screen_height = 1200, 670
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Stack Visualization")


button_width, button_height = 200, 50
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PINK = (255, 192, 203),  # Pink

font = pygame.font.Font(None, 36)

def draw_button(x, y, text, color):
    """Draw a button on the screen."""
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)

def display_message(message):
    """Display the message at the top of the screen."""
    
    pygame.draw.rect(screen, WHITE, (0, 0, screen_width, 100)) 

    message_surface = font.render(message, True, BLACK)
    message_rect = message_surface.get_rect(center=(screen_width // 2, 50))
    screen.blit(message_surface, message_rect)
def draw_time_complexity():
    """Draw time complexity information on the screen."""
    time_text1 = font.render("Push: O(1)", True, (0, 0, 255))
    time_text2 = font.render("Pop: O(1)", True, (0, 0, 255))
    time_text3 = font.render("Peek: O(1)", True, (0, 0, 255))

    screen.blit(time_text1, (150, 100))
    screen.blit(time_text2, (150, 150))
    screen.blit(time_text3, (150, 200))
def main():
  
    current_message = "Press the buttons to perform operations."
    stack = Stack()
    visualizer = StackVisualizer(screen, screen_width, screen_height)
    # Main loop
    while True:
        screen.fill(WHITE) 

        # Display buttons
        draw_button(100, 550, "Push", GREEN)
        draw_button(350, 550, "Pop", RED)
        draw_button(600, 550, "Peek", PINK)
        draw_button(850, 550, "Quit", GRAY)
        draw_time_complexity()

       
        display_message(current_message)
        visualizer.visualize_stack(stack)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 300 and 550 <= y <= 600: 
                
                    random_number = random.randint(1, 100)
                    stack.push(random_number)
                    
                    current_message = f"Pushed 10 onto the stack. Stack size: {len(stack.items)}"

                elif 350 <= x <= 550 and 550 <= y <= 600: 
                    if stack.is_empty():
                        current_message = "Cannot pop, stack is empty!"
                    else:
                        popped_value = stack.pop()
                        current_message = f"Popped {popped_value}. Stack size: {len(stack.items)}"

                elif 600 <= x <= 800 and 550 <= y <= 600:  
                    if stack.is_empty():
                        current_message = "Cannot peek, stack is empty!"
                    else:
                        top_value = stack.peek()
                        current_message = f"Top of stack: {top_value}"

                elif 850 <= x <= 1050 and 550 <= y <= 600:  
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()  
if __name__ == "__main__":
    main()