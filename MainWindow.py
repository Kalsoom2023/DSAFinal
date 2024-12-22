import pygame
import os
import subprocess
import pygetwindow as gw 


pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 670

# Number of images and grid settings
NUM_IMAGES = 14 
GRID_ROWS = 3  
GRID_COLS = 5  
MARGIN = 30

# Increased image size (increase the width and height)
IMAGE_WIDTH = (SCREEN_WIDTH - (GRID_COLS + 1) * MARGIN) // GRID_COLS - 10  
IMAGE_HEIGHT = IMAGE_WIDTH * 3 // 4  

# Path to the images
image_dir = "videos\\" 

# Load your images
image_paths = [
    os.path.join(image_dir, f"img_{i+2}.jpg") for i in range(NUM_IMAGES)
]

images = []
for path in image_paths:
    if os.path.exists(path): 
        try:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (IMAGE_WIDTH, IMAGE_HEIGHT))
            images.append(img)
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            images.append(None)
    else:
        print(f"Image file {path} not found.")
        images.append(None)


font = pygame.font.Font(None, 32)
title_font = pygame.font.Font(None,56)


image_labels = {
    0: "Sorting",             
    1: "Array",                   
    2: "Stack",                 
    3: "QUEUE",        
    4: "Deque",           
    5: "LinkedList",                    
    6: "Hashing",                    
    7: "BST",                 
    8: "AVL",             
    9: "Red Black",                   
    10: "Graph Traversal",                 
    11: "MST",              
    12: "Shortest Path",                    
    13: "Conversions"                    
    
}

# Function to run the scripts and bring the window to the front
def run_script(script_name):
    script_paths = {
        "Conversions": "conversions\\conversions.py",
        "Stack": "datastruct\\stack\\stack_main.py",
        "Sorting": "sorting\\main.py",
        "Graph Traversal": "Graphs\\bfs_dfs.py",
        "Shortest Path": "Graphs\\Path.py",
        "MST": "Graphs\\MST.py",
        "BST": "Trees\\bstnew.py", 
        "Hashing": "hash\\HashMain.py",  
        "LinkedList": "datastruct\\linkedlist\\ll_main.py",
        "Array": "datastruct\\arrayvisualizer.py",
        "Deque": "datastruct\\deque\\deque_main.py",
        "Red Black": "Trees\\rb_tree.py",
        "AVL": "Trees\\AVL.py",
        "QUEUE" : "datastruct\\queue\\queue_main.py"
    }

    script_path = script_paths.get(script_name)
    if script_path and os.path.exists(script_path):
        try:
            print(f"Running script: {script_path}")
            # Start the script as a new subprocess
            process = subprocess.Popen(["python", script_path])  
            process.wait()  

           
            window_title = os.path.basename(script_path).split('.')[0]  # Use script name for title
            try:
                window = gw.getWindowsWithTitle(window_title)[0]
                window.activate()  # Bring the window to the front
            except IndexError:
                print(f"Window with title {window_title} not found.")
            
        except Exception as e:
            print(f"Error running script {script_name}: {e}")
    else:
        print(f"Script for {script_name} not found.")

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Image Grid with Names")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos 
            print(f"Mouse click at: {mouse_x}, {mouse_y}")  

            for row in range(GRID_ROWS):
                for col in range(GRID_COLS):
                    index = row * GRID_COLS + col
                    if index < NUM_IMAGES and images[index]:
                        x = MARGIN + col * (IMAGE_WIDTH + MARGIN)
                        y = 120 + row * (IMAGE_HEIGHT + 60)  

                        
                        print(f"Image {image_labels.get(index)} position: x={x}, y={y}, width={IMAGE_WIDTH}, height={IMAGE_HEIGHT}")

                        if x <= mouse_x <= x + IMAGE_WIDTH and y <= mouse_y <= y + IMAGE_HEIGHT:
                            label = image_labels.get(index, "")
                            print(f"Clicked on label: {label}")  

                           
                            if label:
                                print(f"{label} image clicked! Running script...")
                                run_script(label)

  
    screen.fill((70, 130, 180))

   
    title_text = "Data Structures and Algorithms Visualizer"
    title_surface = title_font.render(title_text, True, (255,255,255))

   
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 25)) 
    screen.blit(title_surface, title_rect)

    
    space_after_title = 40 
    start_y = title_rect.bottom + space_after_title  

    vertical_gap = 60  

    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            index = row * GRID_COLS + col
            if index < NUM_IMAGES and images[index]:
                x = MARGIN + col * (IMAGE_WIDTH + MARGIN)
                y = start_y + row * (IMAGE_HEIGHT + vertical_gap)  
                screen.blit(images[index], (x, y))

            
                label = image_labels.get(index, f"image_{index+2}")  

                text_surface = font.render(label, True, (255,255,255))

                text_rect = text_surface.get_rect(center=(x + IMAGE_WIDTH // 2, y + IMAGE_HEIGHT + 15))
                screen.blit(text_surface, text_rect)

    pygame.display.update()


pygame.quit()
