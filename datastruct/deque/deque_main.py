import pygame
import sys
import random
from dequeClass import DequeClass
from deque_visualizer import DequeVisualizer



pygame.init()
button_width, button_height = 200, 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen_width, screen_height = 1200, 670
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Deque Visualization")


font = pygame.font.Font(None, 36)


deque = DequeClass()
deque_visualizer = DequeVisualizer(screen, screen_width, screen_height, font)
def draw_button(screen, x, y, text, color, font):
    """Draw a button on the screen."""
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)

def display_message(screen, message, font, screen_width):
    """Display the message at the top of the screen."""
    pygame.draw.rect(screen, WHITE, (0, 0, screen_width, 100))  # Clear the top area
    message_surface = font.render(message, True, BLACK)
    message_rect = message_surface.get_rect(center=(screen_width // 2, 50))
    screen.blit(message_surface, message_rect)
def draw_time_complexity(screen, font):
    """Draw time complexity information on the screen."""
    time_text = font.render("Insert (Enqueue/Dequeue): O(1)", True, (0, 0, 255))
    search_text = font.render("Search: O(n)", True, (0, 0, 255))

    screen.blit(time_text, (50, 100))
    screen.blit(search_text, (50, 150))    
def main():
    current_message = "Press buttons to perform deque operations."

    while True:
        screen.fill((255, 255, 255))  # White background

        # Display buttons
        draw_button(screen, 100, 550, "Enqueue Front", (0, 255, 0), font)
        draw_button(screen, 350, 550, "Enqueue Rear", (255, 0, 0), font)
        draw_button(screen, 600, 550, "Dequeue Front", (255, 105, 180), font)
        draw_button(screen, 850, 550, "Dequeue Rear", (128, 0, 128), font)
        draw_button(screen, 500, 610, "Quit", (200, 200, 200), font)
        draw_time_complexity(screen, font)

        # Display message
        display_message(screen, current_message, font, screen_width)

        # Visualize the deque
        deque_visualizer.visualize_deque(deque)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 300 and 550 <= y <= 600:  # Enqueue Front button
                    value = random.randint(1, 100)  # Random number for enqueue
                    deque.enqueue_front(value)
                    current_message = f"Enqueued {value} to the front. Deque size: {deque.size()}"

                elif 350 <= x <= 550 and 550 <= y <= 600:  # Enqueue Rear button
                    value = random.randint(1, 100)  # Random number for enqueue
                    deque.enqueue_rear(value)
                    current_message = f"Enqueued {value} to the rear. Deque size: {deque.size()}"

                elif 600 <= x <= 800 and 550 <= y <= 600:  # Dequeue Front button
                    if not deque.is_empty():
                        dequeued_value = deque.dequeue_front()
                        current_message = f"Dequeued {dequeued_value} from the front. Deque size: {deque.size()}"
                    else:
                        current_message = "Deque is empty!"

                elif 850 <= x <= 1050 and 550 <= y <= 600:  # Dequeue Rear button
                    if not deque.is_empty():
                        dequeued_value = deque.dequeue_rear()
                        current_message = f"Dequeued {dequeued_value} from the rear. Deque size: {deque.size()}"
                    else:
                        current_message = "Deque is empty!"

                elif 500 <= x <= 700 and 610 <= y <= 660:  # Quit button
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main()
