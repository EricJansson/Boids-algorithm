import random
import pygame
from game import Game
from config import *
import numpy as np


class Window:

    def __init__(self):
        """
        Initializes the application window.

        :param root: The root window of the tkinter application.
        """
        pygame.init()


        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pygame.time.Clock()

        self.game = Game()

        # Button callback
        def add_agent():
            self.game.agent_factory.create_agent(np.random.uniform(0, FIELD_H, size=2))

        # Button callback
        def add_many_agents():
            for i in range(10):
                self.game.agent_factory.create_agent(np.random.uniform(0, FIELD_H, size=2))


        add_agent_button = AddAgentButton(
            WINDOW_W // 2 - 300,       # X position
            FIELD_H + 20,                   # Y position
            200,                            # Width
            50,                             # Height
            "Add Boid", add_agent
        )
        
        add_agents_button = AddAgentButton(
            WINDOW_W // 2 + 100,       # X position
            FIELD_H + 20,                   # Y position
            200,                            # Width
            50,                             # Height
            "Add 10 Boids", add_many_agents
        )

        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                add_agent_button.handle_event(event)
                add_agents_button.handle_event(event)

            self.game.update()

            # Render
            self.render()
            add_agent_button.render(self.screen)
            add_agents_button.render(self.screen)
            
            pygame.display.flip()

            # Limit rendering to a reasonable FPS
            self.clock.tick(30)

        pygame.quit()


    def render(self):
        self.screen.fill(WHITE)

        # Draw the game field
        pygame.draw.rect(self.screen, GREEN, (FIELD_OFFSET_X, FIELD_OFFSET_Y, FIELD_W, FIELD_H))

        self.game.render(self.screen)



# Button class
class AddAgentButton:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = GRAY

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

