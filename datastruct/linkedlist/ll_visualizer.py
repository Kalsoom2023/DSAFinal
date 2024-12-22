import pygame

class LinkedListVisualizer:
    def __init__(self, screen, width, height, font):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font

    def visualize_linkedlist(self, linked_list, highlight_node=None):
       
        current_node = linked_list.head
        num_elements = linked_list.size()

        if num_elements == 0:
            return

        start_x = 150
        start_y = self.height // 2

        
        node_index = 1
        while current_node:
            value = current_node.data

           
            box_color = (0, 255, 0)  
            if highlight_node == node_index:
                box_color = (255, 255, 0)  

            text_color = (0, 0, 0)  
            box_width, box_height = 120, 40
            box_x, box_y = start_x - box_width // 2, start_y - box_height // 2

            pygame.draw.rect(self.screen, box_color, (box_x, box_y, box_width, box_height))
            value_text = self.font.render(str(value), True, text_color)
            text_rect = value_text.get_rect(center=(start_x, start_y))
            self.screen.blit(value_text, text_rect)

            # Draw arrows
            if current_node.next:
                arrow_start = (start_x + box_width // 2, start_y)
                arrow_end = (start_x + 160, start_y)
                pygame.draw.line(self.screen, (0, 0, 0), arrow_start, arrow_end, 5)
                pygame.draw.polygon(self.screen, (0, 0, 0), [
                    (arrow_end[0], arrow_end[1]),
                    (arrow_end[0] - 10, arrow_end[1] - 10),
                    (arrow_end[0] - 10, arrow_end[1] + 10)
                ])

            start_x += 160  # Move to next node
            current_node = current_node.next
            node_index += 1

        pygame.display.flip()
    
    def search_with_animation(self,linked_list, value, visualizer, screen):
        """
        Search for a value in the linked list with animation.
        """
        current_node = linked_list.head
        node_index = 1

        while current_node:
          
            visualizer.visualize_linkedlist(linked_list, highlight_node=node_index)

            pygame.time.delay(500)  

            if current_node.data == value:
               
                visualizer.visualize_linkedlist(linked_list, highlight_node=node_index)
                pygame.time.delay(500)
                return node_index 

          
            current_node = current_node.next
            node_index += 1

       
        visualizer.visualize_linkedlist(linked_list)
        return -1
