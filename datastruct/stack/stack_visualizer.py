import pygame

class StackVisualizer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 36)
        
        # Predefined color palette for each stack item
        self.colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (255, 165, 0),  # Orange
            (0, 255, 255),  # Cyan
            (255, 192, 203),  # Pink
            (128, 0, 128),  # Purple
            
           
            (192, 192, 192),  # Silver
            (255, 140, 0),  # Dark Orange
        ]

    def visualize_stack(self, stack, highlight_index=None):
        """
        Visualize the stack with each item in a unique color.
        Each stack element will be drawn in its own colored box.
        """
        num_elements = stack.size()  # Get the current stack size
        if num_elements == 0:
            return  # Do nothing if the stack is empty

        # Define the starting position to stack items vertically
        start_x = self.width // 2  # Center horizontally
        start_y = self.height // 6  # Start higher on the screen

          

        # Draw each element in the stack with unique color for each
        for i in range(num_elements):
            value = stack.items[i]  # Get the value at this index in the stack
            # Calculate vertical position (go downwards for stack items)
            y_position = start_y + (num_elements - i - 1) * 40  # Stack items vertically, from top to bottom

            # Use a color from the color palette for each stack item
            box_color = self.colors[i % len(self.colors)]  # Cycle through the color palette if needed
            text_color = (0, 0, 0)  # Black text for readability

            # Draw a rectangle (colored box) behind the text
            box_width = 120  # Smaller width for the box
            box_height = 40  # Smaller height for the box
            box_x = start_x - box_width // 2  # Center the box horizontally
            box_y = y_position - box_height // 2  # Center the box vertically around the text

            pygame.draw.rect(self.screen, box_color, (box_x, box_y, box_width, box_height))  # Draw the box

            # Render the value as text
            value_text = self.font.render(str(value), True, text_color)
            text_rect = value_text.get_rect(center=(start_x, y_position))  # Center the text in the box
            self.screen.blit(value_text, text_rect)  # Draw the text

        # Update the display to reflect changes
        pygame.display.flip()
