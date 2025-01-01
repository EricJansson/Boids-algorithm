import pygame
from agentFactory import AgentFactory

class Game:
    
    def __init__(self): 
        self.agent_factory = AgentFactory()

    def update(self):
        """
        Update all game entities.
        """
        self.agent_factory.update()

    def render(self, screen):
        """
        Render all game entities.
        """
        self.agent_factory.render(screen)

    def create_agent(self, pos):
        """
        Creates a new agent with the specified position (pos).
        """
        self.agent_factory.create_agent(pos)
