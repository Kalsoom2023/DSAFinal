import pygame
from sorting import bubble_sort,quick_sort,bucket_sort,insertion_sort,selection_sort,merge_sort,radix_sort,counting_sort
from animations import SortingVisualizer
import random
import sys
import copy

pygame.init()
screen = pygame.display.set_mode((1200, 670))  
pygame.display.set_caption("Sorting Algorithm Visualizer")

    # Colors and Fonts
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (176, 224, 230) 
TEXT_COLOR = (0, 0, 0) 
INPUT_BOX_COLOR = (220, 220, 255)  
FONT = pygame.font.Font(None, 36)
SLIDER_COLOR = (0, 0, 0) 
KNOB_COLOR = (0, 0, 0) 
BUTTON_COLOR = (0, 191, 255)
SMALL_FONT = pygame.font.Font(None, 24)
HEADERFONT = pygame.font.Font(pygame.font.match_font('arialblack'), 40)
SMALLFONT = pygame.font.Font(pygame.font.match_font('arialblack'), 20)
sorting_complete = False
speed_factor = 1.0
TIME_COMPLEXITIES = {
    "insertion": "Best: O(n), Avg: O(n^2), Worst: O(n^2)",
    "selection": "Best: O(n^2), Avg: O(n^2), Worst: O(n^2)",
    "bubble": "Best: O(n), Avg: O(n^2), Worst: O(n^2)",
    "merge": "Best: O(n log n), Avg: O(n log n), Worst: O(n log n)",
    "quick": "Best: O(n log n), Avg: O(n log n), Worst: O(n^2)",
    "counting": "Best: O(n + k), Avg: O(n + k), Worst: O(n + k)",
    "radix": "Best: O(nk), Avg: O(nk), Worst: O(nk)",
    "bucket": "Best: O(n + k), Avg: O(n + k), Worst: O(n^2)",
}

SPACE_COMPLEXITIES = {
    "insertion": "O(1)",
    "selection": "O(1)",
    "bubble": "O(1)",
    "merge": "O(n)",
    "quick": "O(log n)",
    "counting": "O(k)",
    "radix": "O(n + k)",
    "bucket": "O(n + k)",
}

def create_button(text, x, y, width, height, screen, color=BUTTON_COLOR):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = FONT.render(text, True, TEXT_COLOR)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)
    return pygame.Rect(x, y, width, height)

def draw_speed_slider(screen, speed_factor):
    slider_x = 350 + int((speed_factor - 0.25) / (2-0.25) * (400))
    pygame.draw.line(screen, TEXT_COLOR, (350, 550), (750, 550), 3)
    pygame.draw.circle(screen, TEXT_COLOR, (slider_x, 550), 10) 
    speed_label = SMALL_FONT.render(f"Speed: {speed_factor:.2f}x", True, TEXT_COLOR)
    screen.blit(speed_label, (WIDTH // 2 - speed_label.get_width() // 2 + 100, 500))

def main_menu(screen):
    running = True
    selected_algorithm = None
    array_size = 10
    user_data = []
    speed=50
    
    while running:
        screen.fill(BACKGROUND_COLOR)
        
    # Title
        title = HEADERFONT.render("Sorting Visualizer", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # Algorithm selection buttons
        bubble_button = create_button("Bubble Sort", 200, 150, 150, 50, screen)
        quick_button = create_button("Quick Sort", 400, 150, 150, 50, screen)
        bucket_button = create_button("Bucket Sort", 600, 150, 150, 50, screen)
        insertion_button = create_button("Insertion Sort", 800, 150, 170, 50, screen)
        selection_button = create_button("Selection Sort", 200, 250, 170, 50, screen)
        merge_button = create_button("Merge Sort", 400, 250, 150, 50, screen)
        radix_button = create_button("Radix Sort", 600, 250, 150, 50, screen)
        counting_button = create_button("Counting Sort", 800, 250, 170, 50, screen)

        # Slider for array size
        array_size_label = SMALL_FONT.render(f"Array Size: {array_size}", True, TEXT_COLOR)
        screen.blit(array_size_label, (WIDTH // 2 +150, 330))
        pygame.draw.line(screen, TEXT_COLOR, (450, 380), (750, 380), 3)
        slider_x = 450 + (array_size - 5) * (750-450)/ (15-5)  
        pygame.draw.circle(screen, TEXT_COLOR, (slider_x, 380), 10)
        
        input_label = SMALL_FONT.render("Press 'I' to Input Array or 'R' for Random", True, TEXT_COLOR)
        screen.blit(input_label, (WIDTH // 2 - input_label.get_width() // 2 + 200, 420))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Slider logic
            elif event.type == pygame.MOUSEBUTTONDOWN and 450 <= event.pos[0] <= 750 and 370 <= event.pos[1] <= 390:
                array_size = 5 + int((event.pos[0] - 450)* (15-5)// (750-450))
            elif event.type == pygame.MOUSEBUTTONDOWN and 450 <= event.pos[0] <= 750 and 740 <= event.pos[1] <= 760:
                speed = 10 + (event.pos[0] - 450) * 2
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bubble_button.collidepoint(event.pos):
                    selected_algorithm = "bubble"
                elif quick_button.collidepoint(event.pos):
                    selected_algorithm = "quick"
                elif bucket_button.collidepoint(event.pos):
                    selected_algorithm = "bucket"
                elif insertion_button.collidepoint(event.pos):
                    selected_algorithm = "insertion"
                elif selection_button.collidepoint(event.pos):
                    selected_algorithm = "selection"
                elif merge_button.collidepoint(event.pos):
                    selected_algorithm = "merge"
                elif radix_button.collidepoint(event.pos):
                    selected_algorithm = "radix"
                elif counting_button.collidepoint(event.pos):
                    selected_algorithm = "counting"
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    user_data = user_input(screen, array_size)
                    if len(user_data) == array_size:  # Ensure valid input size
                        running = False
                elif event.key == pygame.K_r:
                    user_data = [random.randint(10, 100) for _ in range(array_size)]
                    running = False
        pygame.display.flip()
    return selected_algorithm, user_data, array_size

def user_input(screen,array_size):
    input_data = []
    input_string = ""
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)

        # Instructions
        instructions = FONT.render("Enter Number and Press space", True, TEXT_COLOR)
        screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2 + 200, 200))
        
        input_field_x = WIDTH // 2 + 55  
        input_field_y = 290
        input_field_width = 300
        input_field_height = 50
        pygame.draw.rect(screen, (50, 50, 50), (input_field_x, input_field_y, input_field_width, input_field_height))  # Dark gray
        pygame.draw.rect(screen, (200, 200, 200), (input_field_x, input_field_y, input_field_width, input_field_height), 2)  # Border


        input_label = FONT.render(input_string, True, BACKGROUND_COLOR)
        screen.blit(input_label, (WIDTH // 2 - input_label.get_width() // 2 +200, 300))
        
        remaining_label = FONT.render(
            f"Remaining numbers: {array_size - len(input_data)}", True, TEXT_COLOR
        )
        screen.blit(remaining_label, (50, 300))
        
        if len(input_data) == array_size:
            start_button = create_button("Start Sorting", 500, 400, 200, 50, screen)
            
        back = create_button("Back", 1000, 580, 100, 40, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(input_data) == array_size:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    if input_string:
                        input_string = input_string[:-1]
                elif event.unicode.isdigit() or event.unicode == ' ':
                    input_string += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if len(input_data) == array_size and start_button.collidepoint(event.pos):
                    running = False
                elif back.collidepoint(event.pos):
                    print("Back button clicked!")
                    return "main_menu"
                    
        if " " in input_string:
            try:
                num = int(input_string.strip())
                if len(input_data) < array_size:
                    input_data.append(num)
                input_string = ""
            except ValueError:
                input_string = ""

        pygame.display.flip()

    return input_data


def main():
    global sorting_complete, speed_factor
    sorting_complete = False
    is_paused = False
    
    while True:
        selected_algorithm, user_data, array_size = main_menu(screen)

        if not user_data:
            user_data = [random.randint(10, 100) for _ in range(array_size)]

        visualizer = SortingVisualizer(screen, user_data)

        if selected_algorithm == "bubble":
            sorting_gen = bubble_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
        elif selected_algorithm == "quick":
            sorting_gen = quick_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
        elif selected_algorithm == "bucket":
            sorting_gen = bucket_sort(user_data, visualizer,delay=lambda: 500 / speed_factor) 
        elif selected_algorithm == "insertion":
            sorting_gen = insertion_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
        elif selected_algorithm == "selection":
            sorting_gen = selection_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
        elif selected_algorithm == "merge":
            sorting_gen = merge_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
        elif selected_algorithm == "radix":
            sorting_gen = radix_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
        elif selected_algorithm == "counting":
            sorting_gen = counting_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
            

        original_data = copy.deepcopy(user_data) 
        sorting_complete = False
        is_paused = False
        running = True
        while running:
            screen.fill(BACKGROUND_COLOR)

            play_button = create_button("Play", 350, 580, 100, 40, screen)
            pause_button = create_button("Pause", 500, 580, 100, 40, screen)
            restart_button = create_button("Restart", 650, 580, 100, 40, screen)
            back_button = create_button("Back", 1000, 580, 100, 40, screen)
            draw_speed_slider(screen, speed_factor)
            
            algorithm_title = HEADERFONT.render(f"{selected_algorithm.capitalize()} Sort", True, TEXT_COLOR)
            time_complexity_text = SMALLFONT.render(f"Time Complexity: {TIME_COMPLEXITIES[selected_algorithm]}", True, TEXT_COLOR)
            space_complexity_text = SMALLFONT.render(f"Space Complexity: {SPACE_COMPLEXITIES[selected_algorithm]}", True, TEXT_COLOR)

            # Display the algorithm title
            screen.blit(algorithm_title, (WIDTH // 3 - algorithm_title.get_width() // 2, 20))

            # Display time complexity below the title
            screen.blit(time_complexity_text, (WIDTH // 1 - time_complexity_text.get_width() // 2, 30))

            # Display space complexity below the time complexity
            screen.blit(space_complexity_text, (WIDTH // 1 - space_complexity_text.get_width() // 2, 70))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        is_paused = False
                    elif pause_button.collidepoint(event.pos):
                        is_paused = True
                    elif back_button.collidepoint(event.pos):
                            running = False 
                    elif restart_button.collidepoint(event.pos):
                        sorting_complete = False  
                        user_data = [random.randint(10, 100) for _ in range(array_size)]
                        visualizer = SortingVisualizer(screen, user_data)
                        if selected_algorithm == "bubble":
                            sorting_gen = bubble_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
                        elif selected_algorithm == "quick":
                            sorting_gen = quick_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
                        elif selected_algorithm == "bucket":
                            sorting_gen = bucket_sort(user_data, visualizer,delay=lambda: 500 / speed_factor) 
                        elif selected_algorithm == "insertion":
                            sorting_gen = insertion_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
                        elif selected_algorithm == "selection":
                            sorting_gen = selection_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
                        elif selected_algorithm == "merge":
                            sorting_gen = merge_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
                        elif selected_algorithm == "radix":
                            sorting_gen = radix_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)
                        elif selected_algorithm == "counting":
                            sorting_gen = counting_sort(user_data, visualizer,delay=lambda: 500 / speed_factor)               
                        is_paused = False
                    elif 350 <= event.pos[0] <= 750 and 540 <= event.pos[1] <= 560:
                            speed_factor = 0.25 + ((event.pos[0] - 350) / 400) * 1.75

            if sorting_complete:
                visualizer.draw_bars()
                visualizer.display_data()
              
            else:
                if not is_paused:
                    try:
                        next(sorting_gen)
                    except StopIteration:
                        sorting_complete = True
                        visualizer.draw_bars()
                        visualizer.display_data()
                else:
                    visualizer.draw_bars()
                    visualizer.display_data()

            pygame.display.flip()



if __name__ == "__main__":
    main()