import pygame
import sys
import random
from linklist_class import LinkedList
from ll_visualizer import LinkedListVisualizer


pygame.init()


screen_width, screen_height = 1200, 670
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Linked List Visualization")


font = pygame.font.Font(None, 36)


linked_list = LinkedList()
linked_list_visualizer = LinkedListVisualizer(screen, screen_width, screen_height, font)


button_width, button_height = 200, 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_button(screen, x, y, text, color, font):
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)

def display_message(screen, message, font, screen_width):
    pygame.draw.rect(screen, WHITE, (0, 0, screen_width, 100))  
    message_surface = font.render(message, True, BLACK)
    message_rect = message_surface.get_rect(center=(screen_width // 2, 50))
    screen.blit(message_surface, message_rect)

def draw_input_box(screen, x, y, width, height, font, text):
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)  
    input_text_surface = font.render(text, True, BLACK)
    screen.blit(input_text_surface, (x + 5, y + 5)) 
def draw_time_complexity(screen, font):
    """Draw time complexity information on the screen."""
    time_text1 = font.render("Insert Front: O(1)", True, (0, 0, 255))
    time_text2 = font.render("Insert End: O(n)", True, (0, 0, 255))
    time_text3 = font.render("Delete Front: O(1)", True, (0, 0, 255))
    time_text4 = font.render("Delete End: O(n)", True, (0, 0, 255))
    time_text5 = font.render("Search: O(n)", True, (0, 0, 255))
    time_text6 = font.render("Reverse: O(n)", True, (0, 0, 255))

    screen.blit(time_text1, (50, 100))
    screen.blit(time_text2, (50, 150))
    screen.blit(time_text3, (50, 200))
    screen.blit(time_text4, (300, 100))
    screen.blit(time_text5, (300, 150))
    screen.blit(time_text6, (300, 200))
def main():
    current_message = "Enter a number in the box and press a button to perform operations on the Linked List."
    input_text = "" 

    while True:
        screen.fill((255, 255, 255))  # White background

        # Display buttons
        draw_button(screen, 100, 550, "Insert Front", (0, 255, 0), font)
        draw_button(screen, 350, 550, "Insert End", (255, 0, 0), font)
        draw_button(screen, 600, 550, "Delete Front", (255, 105, 180), font)
        draw_button(screen, 850, 550, "Delete End", (128, 0, 128), font)
        draw_button(screen, 100, 610, "Search", (255, 255, 0), font)
        draw_button(screen, 350, 610, "Reverse", (0, 255, 255), font)
        draw_button(screen, 600, 610, "Delete", (128, 0, 128), font)
        draw_button(screen, 850, 610, "Quit", (200, 200, 200), font)
        draw_time_complexity(screen, font)

        # Display message
        display_message(screen, current_message, font, screen_width)

        # Draw the input box for the search
        draw_input_box(screen, 100, 460, 200, 40, font, input_text)

        # Visualize the linked list
        linked_list_visualizer.visualize_linkedlist(linked_list)
                                                    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 300 and 550 <= y <= 600:  # Insert Front button
                    if input_text.isdigit():  # Check if the input is a number
                        value = int(input_text)
                        linked_list.insert_front(value)
                        current_message = f"Inserted {value} at the front. Linked List size: {linked_list.size()}"
                    else:
                        current_message = "Please enter a valid number to insert."

                elif 350 <= x <= 550 and 550 <= y <= 600:  # Insert End button
                    if input_text.isdigit():
                        value = int(input_text)
                        linked_list.insert_end(value)
                        current_message = f"Inserted {value} at the end. Linked List size: {linked_list.size()}"
                    else:
                        current_message = "Please enter a valid number to insert."

                elif 600 <= x <= 800 and 550 <= y <= 600:  # Delete Front button
                    linked_list.delete_front()  # Just delete the front node
                    current_message = f"Deleted from the front. Linked List size: {linked_list.size()}"

                elif 850 <= x <= 1050 and 550 <= y <= 600:  # Delete End button
                    linked_list.delete_end()  # Just delete the end node
                    current_message = f"Deleted from the end. Linked List size: {linked_list.size()}"

                elif 100 <= x <= 300 and 610 <= y <= 660:  # Search button
                    if input_text.isdigit():
                        value = int(input_text)
                        search_position = linked_list_visualizer.search_with_animation(linked_list, value, linked_list_visualizer, screen)
                        if search_position != -1:
                            current_message = f"Found {value} at position {search_position}."
                        else:
                            current_message = f"{value} not found in the list."
                    else:
                        current_message = "Please enter a valid number to search."

                elif 350 <= x <= 550 and 610 <= y <= 660:  # Reverse button
                    linked_list.reverse()
                    current_message = "Reversed the Linked List."

                elif 600 <= x <= 800 and 610 <= y <= 660:  # Delete button based on input
                    if input_text.isdigit():
                        value = int(input_text)
                        search_position = linked_list_visualizer.search_with_animation(linked_list, value, linked_list_visualizer, screen)
                        removed_data = linked_list.delete(value)  # Delete based on the input value
                        if removed_data is not None:
                            current_message = f"Deleted {removed_data} from the list."
                        else:
                            current_message = f"{value} not found in the list."
                    else:
                        current_message = "Please enter a valid number to delete."

                elif 850 <= x <= 1050 and 610 <= y <= 660:  # Quit button
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN: 
                    if input_text.isdigit():
                        value = int(input_text)
                        current_message = f"Entered {value} for the action."
                    else:
                        current_message = "Please enter a valid number."
                else: 
                    if len(input_text) < 10: 
                        input_text += event.unicode

        pygame.display.flip()

if __name__ == "__main__":
    main()
