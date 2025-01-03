from agent import Agent
from config import *

class AgentFactory:
    def __init__(self):
        self.agent_iterator = 0
        self.agents = []

    def update(self, settings):
        bounds = (FIELD_W, FIELD_H)
        for agent in self.agents:
            agent.apply_behaviors(self.agents, settings)  # Apply separation, alignment, cohesion
            agent.update()                      # Update position and velocity
            agent.edges(bounds, phase_through=settings["phase_through"])                 # Don't cross field boundaries

    def render(self, screen):
        for agent in self.agents:
            agent.render(screen)

    def create_agent(self, pos):
        """
        param : pos - [x, y] 
        """
        self.agent_iterator += 1
        temp_agent = Agent(self.agent_iterator, pos)
        self.agents.append(temp_agent)

    def get_agents(self):
        return self.agents
    
    