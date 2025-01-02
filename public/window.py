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

        self.settings = {
            "separation": True,
            "alignment": True,
            "cohesion": True,
            "randomness": True,
            "wander_force": True,
            "phase_through": True
        }

        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pygame.time.Clock()

        self.game = Game()

        # Callback Buttons
        def add_agent():
            self.game.agent_factory.create_agent(np.random.uniform(0, FIELD_H, size=2))

        def add_many_agents():
            for i in range(35):
                self.game.agent_factory.create_agent(np.random.uniform(0, FIELD_H, size=2))

        def toggle_separation():
            self.settings["separation"] = not self.settings["separation"]
            return self.settings["separation"]

        def toggle_alignment():
            self.settings["alignment"] = not self.settings["alignment"]
            return self.settings["alignment"]

        def toggle_cohesion():
            self.settings["cohesion"] = not self.settings["cohesion"]
            return self.settings["cohesion"]

        def toggle_randomness():
            self.settings["randomness"] = not self.settings["randomness"]
            return self.settings["randomness"]

        def toggle_wander_force():
            self.settings["wander_force"] = not self.settings["wander_force"]
            return self.settings["wander_force"]
        
        def toggle_phase_through():
            self.settings["phase_through"] = not self.settings["phase_through"]
            return self.settings["phase_through"]
        

        self.all_buttons = []

        add_agent_button = AddAgentButton(
            WINDOW_W // 2 - 220,            # X position
            FIELD_H + 20,                   # Y position
            200,                            # Width
            50,                             # Height
            "Add Boid", add_agent
        )
        
        add_agents_button = AddAgentButton(
            WINDOW_W // 2 + 20,             # X position
            FIELD_H + 20,                   # Y position
            200,                            # Width
            50,                             # Height
            "Add 35 Boids", add_many_agents
        )


        toggle_button_separation = ToggleButton(
            WINDOW_W // 2 - 100, 
            FIELD_H + 85, 
            200,
            50,
            toggle_separation,
            text_on="Separation ON", 
            text_off="Separation OFF"
        )
        
        toggle_button_alignment = ToggleButton(
            WINDOW_W // 2 - 350, 
            FIELD_H + 85, 
            200,
            50,
            toggle_alignment,
            text_on="Alignment ON", 
            text_off="Alignment OFF"
        )

        toggle_button_cohesion = ToggleButton(
            WINDOW_W // 2 + 150, 
            FIELD_H + 85,
            200,
            50,
            toggle_cohesion,
            text_on="Cohesion ON", 
            text_off="Cohesion OFF"
        )

        toggle_button_randomness = ToggleButton(
            WINDOW_W // 2 - 110, 
            FIELD_H + 150, 
            220,
            50,
            toggle_randomness,
            text_on="Randomness ON", 
            text_off="Randomness OFF"
        )

        toggle_button_wander_force = ToggleButton(
            WINDOW_W // 2 - 360, 
            FIELD_H + 150, 
            220,
            50,
            toggle_wander_force,
            text_on="Wander force ON", 
            text_off="Wander force OFF"
        )
        
        toggle_button_phase_through = ToggleButton(
            WINDOW_W // 2 + 140, 
            FIELD_H + 150, 
            220,
            50,
            toggle_phase_through,
            text_on="Avoid walls ON", 
            text_off="Avoid walls OFF"
        )
        
        self.all_buttons.append(add_agent_button)
        self.all_buttons.append(add_agents_button)
        self.all_buttons.append(toggle_button_separation)
        self.all_buttons.append(toggle_button_alignment)
        self.all_buttons.append(toggle_button_cohesion)
        self.all_buttons.append(toggle_button_randomness)
        self.all_buttons.append(toggle_button_wander_force)
        self.all_buttons.append(toggle_button_phase_through)

        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                for btn in self.all_buttons:
                    btn.handle_event(event)

            self.game.update(self.settings)

            # Render
            self.render()

            for btn in self.all_buttons:
                btn.render(self.screen)
            
            pygame.display.flip()

            # Limit rendering to a reasonable FPS
            self.clock.tick(30)

        pygame.quit()


    def render(self):
        self.screen.fill(BLACK)

        # Draw the game field
        pygame.draw.rect(self.screen, DARK_GRAY, (FIELD_OFFSET_X, FIELD_OFFSET_Y, FIELD_W, FIELD_H))

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


class ToggleButton:
    def __init__(self, x, y, width, height, callback, text_on="ON", text_off="OFF"):
        """
        Initialize the toggle button.
        :param x: X position of the button.
        :param y: Y position of the button.
        :param width: Width of the button.
        :param height: Height of the button.
        :param callback: Callback function to handle button functionality.
        :param text_on: Text to display when the state is True.
        :param text_off: Text to display when the state is False.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text_on = text_on
        self.text_off = text_off
        self.callback = callback
        self.state = True
        self.color_on = (0, 200, 0)  # Green when True
        self.color_off = (200, 0, 0)  # Red when False
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        """
        Handle mouse click events to toggle the button state.
        :param event: Pygame event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = self.callback()

    def render(self, screen):
        """
        Render the button on the screen.
        :param screen: The Pygame screen to draw on.
        """
        # Choose color based on state
        color = self.color_on if self.state else self.color_off
        pygame.draw.rect(screen, color, self.rect)

        # Render text
        text = self.text_on if self.state else self.text_off
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
