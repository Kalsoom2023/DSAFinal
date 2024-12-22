
import pygame
import random
HEIGHT = 600
BACKGROUND_COLOR = (240, 240, 255)

class SortingVisualizer:
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data
        self.width = screen.get_width()
        self.height = screen.get_height()
        
    def update_bars(self, arr, highlight_indices=[]):
        num_bars = len(arr)
        max_gap = 8  
        min_bar_width = 3 

        available_width = self.width - (num_bars - 1) * max_gap
        bar_width = max(min_bar_width, available_width // (num_bars * 2)) 
        gap = (self.width - (num_bars * bar_width)) // (num_bars - 1) if num_bars > 1 else 0

        max_value = max(arr, default=1)
        total_bars_width = num_bars * bar_width + (num_bars - 1) * gap
        padding = (self.width - total_bars_width) // 2
        max_bar_height = (self.height // 2) - 60  

        font = pygame.font.Font(None, 24)

        for i, value in enumerate(arr):
                x = padding + i * (bar_width + gap)
                bar_height = int((value / max_value) * max_bar_height)
                color = (255, 0, 0) if i in highlight_indices else (0, 150, 255)

                pygame.draw.rect(
                        self.screen,
                        color,
                        (x, self.height - bar_height - 250, bar_width, bar_height),
                )

                value_text = font.render(str(value), True, (0, 0, 128))
                value_text_x = x + (bar_width - value_text.get_width()) // 2
                value_text_y = self.height - bar_height - 260
                self.screen.blit(value_text, (value_text_x, value_text_y))

                index_text = font.render(str(i), True, (128, 0, 0))
                index_text_x = x + (bar_width - index_text.get_width()) // 2
                index_text_y = self.height - 200
                self.screen.blit(index_text, (index_text_x, index_text_y))

        pygame.display.flip()

    def draw_bars(self, highlight_indices=None):
        
        num_bars = len(self.data)
        gap=8

        available_width = self.width -  (num_bars - 1) * gap
        bar_width = max(3, available_width // (num_bars *2))  
        max_value = max(self.data, default=1)
        
        total_bars_width = num_bars * bar_width + (num_bars - 1) * gap
        padding = (self.width - total_bars_width) // 2

        max_bar_height = (self.height // 2) - 60 
        middle_y = self.height // 2 

        for i, value in enumerate(self.data):
            x = padding + i * (bar_width + gap)
            bar_height = int((value / max_value) * max_bar_height)
            color = (0, 150, 255)  
            if highlight_indices and i in highlight_indices:
                color = (255, 0, 0)  

            y = middle_y - bar_height
            pygame.draw.rect(self.screen, color, (x, y+70, bar_width, bar_height))

    def display_data(self):
        font = pygame.font.Font(None, 24)
        num_bars = len(self.data)
        gap = 8 

        available_width = self.width - (num_bars - 1) * gap
        bar_width = max(3, available_width // (num_bars * 2))
        
        total_bars_width = num_bars * bar_width + (num_bars - 1) * gap

        padding = (self.width - total_bars_width) // 2
        max_value = max(self.data, default=1)
        max_bar_height = (self.height // 2) - 90  
        middle_y = self.height // 2

        for i, value in enumerate(self.data):
            x = padding + i * (bar_width + gap)

            value_text = font.render(str(value), True, (0, 0, 128))
            value_text_width = value_text.get_width()
            value_text_x = x + (bar_width - value_text_width) // 2            
            bar_height = int((value / max_value) * max_bar_height)
            y = middle_y - bar_height  

            value_text_y = (y + 50) - value_text.get_height() - 20
            self.screen.blit(value_text, (value_text_x, value_text_y))

            index_text = font.render(str(i), True, (128, 0, 0))
            index_text_width = index_text.get_width()
            index_text_x = x + (bar_width - index_text_width) // 2

            index_text_y = (y + 50 + bar_height) + 25
            self.screen.blit(index_text, (index_text_x, index_text_y))

    @staticmethod
    def generate_random_data(datalength, min_value=10, max_value=100):
        return [random.randint(min_value, max_value) for _ in range(datalength)] 
    
    
    def visualize_radix_sort_bars(self, arr, highlight_index=None):

        num_bars = len(arr)
        gap = 8  

        available_width = self.width - (num_bars - 1) * gap
        bar_width = max(3, available_width // (num_bars * 2)) 
        max_value = max(arr, default=1)

        total_bars_width = num_bars * bar_width + (num_bars - 1) * gap
        padding = (self.width - total_bars_width) // 2
        max_bar_height = (self.height // 2) - 60 
        baseline_y = self.height // 2 + 50 

        font = pygame.font.Font(None, 24)

        for i, value in enumerate(arr):
            x = padding + i * (bar_width + gap)
            bar_height = int((value / max_value) * max_bar_height)
            y = baseline_y - bar_height  

            if i == highlight_index:
                color = (255, 0, 0)  
            else:
                color = (0, 150, 255)  

            pygame.draw.rect(self.screen, color, (x, y, bar_width, bar_height))

            value_text = font.render(str(value), True, (0, 0, 128))
            value_text_x = x + (bar_width - value_text.get_width()) // 2
            value_text_y = y - 25
            self.screen.blit(value_text, (value_text_x, value_text_y))

        pygame.display.flip()


   