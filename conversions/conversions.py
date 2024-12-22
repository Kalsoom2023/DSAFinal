import pygame
import sys
import time

# Helper functions for conversion
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = []
    result = []
    steps = [] 

    for char in expression:
        if char.isalnum():  
            result.append(char)
        elif char == '(':  
            stack.append(char)
        elif char == ')':  
            while stack and stack[-1] != '(':
                result.append(stack.pop())
            stack.pop()  # Pop '('
        else:  # Operator
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence.get(char, 0):
                result.append(stack.pop())
            stack.append(char)
        
       
        steps.append((list(stack), list(result)))

    while stack:
        result.append(stack.pop())
        steps.append((list(stack), list(result)))

    return ''.join(result), steps

def infix_to_prefix(expression):
   
    reversed_expr = expression[::-1]
   
    reversed_expr = ''.join(['(' if c == ')' else ')' if c == '(' else c for c in reversed_expr])

   
    postfix, steps = infix_to_postfix(reversed_expr)
    prefix = postfix[::-1]

   
    reversed_steps = [(stack[::-1], result[::-1]) for stack, result in steps]
    return prefix, reversed_steps

# Pygame UI Functions
def draw_button(screen, text, x, y, width, height, font, color):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect, border_radius=10)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)
    return button_rect

def draw_text(screen, text, x, y, font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_stack(screen, stack, x, y, width, height, font):
    total_height = 4 * (height + 10)
    start_y = y + 50  

   
    pygame.draw.line(screen, (0, 0, 0), (x, start_y), (x, start_y - total_height), 3)  
    pygame.draw.line(screen, (0, 0, 0), (x + width, start_y), (x + width, start_y - total_height), 3) 
    
    for i, item in enumerate(stack):
        item_rect = pygame.Rect(x, y - i * (height + 10), width, height)
        pygame.draw.rect(screen, (0, 128, 255), item_rect, border_radius=10)
        text_surf = font.render(item, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=item_rect.center)
        screen.blit(text_surf, text_rect)

def visualize_steps(screen, font, steps, step_delay,user_text):
    stack_x, stack_y = 400, 300 
    stack_width, stack_height = 120, 50 

    for stack, result in steps:
        screen.fill((173, 216, 230)) 
        draw_text(screen, f"Expression:{user_text}" , stack_x - 50, stack_y - 280, font)
       
        draw_text(screen, "Stack:", stack_x - 50, stack_y - 250, font)
        draw_stack(screen, stack, stack_x, stack_y, stack_width, stack_height, font)

        # Draw result
        draw_text(screen, "Result: " + ''.join(result), 100, 400, font, (0, 128, 0))

        pygame.display.flip()
        time.sleep(step_delay)

# Main Function
def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 670))
    pygame.display.set_caption("Infix to Postfix/Prefix Visualizer")
    font = pygame.font.SysFont(None, 40)  
    input_font = pygame.font.SysFont(None, 48)  

    input_box = pygame.Rect(100, 50, 600, 50) 
    user_text = ''
    running = True
    step_delay = 1 

    while running:
        screen.fill((173, 216, 230)) 

        # Instructions
        draw_text(screen, "Enter Infix Expression:", 100, 20, font)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
        text_surface = input_font.render(user_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # Buttons
        postfix_button = draw_button(screen, "Convert to Postfix", 150, 150, 250, 60, font, (0, 128, 255))
        prefix_button = draw_button(screen, "Convert to Prefix", 450, 150, 250, 60, font, (128, 0, 255))
        clear_button = draw_button(screen, "Clear", 800, 150, 120, 60, font, (255, 0, 0))

        # Speed Controls (slower/faster visualization)
        slow_button = draw_button(screen, "Slow", 150, 250, 150, 60, font, (0, 255, 0))
        fast_button = draw_button(screen, "Fast", 450, 250, 150, 60, font, (255, 255, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    pass  # Placeholder for submit
                else:
                    user_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if postfix_button.collidepoint(event.pos):
                    postfix, steps = infix_to_postfix(user_text)
                    visualize_steps(screen, font, steps, step_delay,user_text)
                    draw_text(screen, f"Postfix: {postfix}", 100, 500, font, (128, 0, 128))
                    pygame.display.flip()
                    time.sleep(2)
                elif prefix_button.collidepoint(event.pos):
                    prefix, steps = infix_to_prefix(user_text)
                    visualize_steps(screen, font, steps, step_delay,user_text)
                    draw_text(screen, f"Prefix: {prefix}", 100, 500, font, (128, 0, 128))
                    pygame.display.flip()
                    time.sleep(2)
                elif clear_button.collidepoint(event.pos):
                    user_text = ''  # Clear input box
                elif slow_button.collidepoint(event.pos):
                    step_delay = 2  # Slow down visualization
                elif fast_button.collidepoint(event.pos):
                    step_delay = 0.5  # Speed up visualization

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
