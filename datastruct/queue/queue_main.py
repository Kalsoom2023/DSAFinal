import pygame
import sys
import random
from queue_visualizer import QueueVisualizer
from queue_class import QueueClass

pygame.init()


screen_width, screen_height = 1200, 670
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Queue Visualization")


button_width, button_height = 200, 50
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PINK =   (255, 192, 203),  
PURPLE = (128, 0, 128),  


font = pygame.font.Font(None, 36)




queue = QueueClass()
queue_visualizer = QueueVisualizer(screen, screen_width, screen_height)
def draw_time_complexity():
    """Draw time complexity information on the screen."""
    time_text1 = font.render("Enqueue: O(1)", True, (0, 0, 255))
    time_text2 = font.render("Dequeue: O(1)", True, (0, 0, 255))
    time_text3 = font.render("Front: O(1)", True, (0, 0, 255))
    time_text4 = font.render("Rear: O(1)", True, (0, 0, 255))

    screen.blit(time_text1, (50, 100))
    screen.blit(time_text2, (50, 150))
    screen.blit(time_text3, (50, 200))
    screen.blit(time_text4, (50, 250))
# Main loop
def main():
    current_message = "Press buttons to perform queue operations."

    while True:
        screen.fill(WHITE)

        # Display buttons
        draw_button(100, 550, "Enqueue", GREEN)
        draw_button(350, 550, "Dequeue", RED)
        draw_button(600, 550, "Front", PINK)
        draw_button(850, 550, "Rear", PURPLE)
        draw_button(500, 610, "Quit", GRAY)
        draw_time_complexity()
        
        display_message(current_message)
        queue_visualizer.visualize_queue(queue) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 300 and 550 <= y <= 600: 
                    value = random.randint(1, 100)  
                    queue.enqueue(value)
                    current_message = f"Enqueued {value}. Queue size: {queue.size()}"

                elif 350 <= x <= 550 and 550 <= y <= 600:  
                    if not queue.is_empty():
                        dequeued_value = queue.dequeue()
                        current_message = f"Dequeued {dequeued_value}. Queue size: {queue.size()}"
                    else:
                        current_message = "Queue is empty!"

                elif 600 <= x <= 800 and 550 <= y <= 600: 
                    front_value = queue.front()
                    if front_value is not None:
                        current_message = f"Front of queue: {front_value}"
                    else:
                        current_message = "Queue is empty!"

                elif 850 <= x <= 1050 and 550 <= y <= 600: 
                    rear_value = queue.rear()
                    if rear_value is not None:
                        current_message = f"Rear of queue: {rear_value}"
                    else:
                        current_message = "Queue is empty!"

                elif 500 <= x <= 700 and 610 <= y <= 660: 
                    pygame.quit()
                    sys.exit()

        
        pygame.display.flip()



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

if __name__ == "__main__":
    main()
