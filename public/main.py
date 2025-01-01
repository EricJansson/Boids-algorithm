import pygame

# Initialize Pygame
from window import *


if __name__ == "__main__":
    pygame.init()
    print("Start")
    root = tk.Tk()
    app = Window(root)
    root.mainloop()
    print("End!")

