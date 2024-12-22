import pygame

class DequeVisualizer:
    def __init__(self, screen, width, height, font):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        
        # Predefined color palette for each deque item
        self.colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (255, 165, 0),  # Orange
            (0, 255, 255),  # Cyan
            (255, 192, 203),  # Pink
            (128, 0, 128),  # Purple
            (0, 0, 0),  # Black
            (255, 255, 255),  # White
            (192, 192, 192),  # Silver
            (255, 140, 0),  # Dark Orange
        ]

    def visualize_deque(self, deque):
      
        num_elements = deque.size() 
        if num_elements == 0:
            return  

        start_x = 150  
        start_y = self.height // 2  

       
        for i in range(num_elements):
            value = deque.items[i]  
            
            x_position = start_x + (i * 130) 

           
            box_color = self.colors[i % len(self.colors)]  
            text_color = (0, 0, 0)  

           
            box_width = 120  
            box_height = 40  
            box_x = x_position - box_width // 2 
            box_y = start_y - box_height // 2  

            pygame.draw.rect(self.screen, box_color, (box_x, box_y, box_width, box_height)) 

            # Render the value as text
            value_text = self.font.render(str(value), True, text_color)
            text_rect = value_text.get_rect(center=(x_position, start_y))  
            self.screen.blit(value_text, text_rect)  

       
        pygame.display.flip()
