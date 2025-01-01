import random
from agent import *

class AgentFactory:
    def __init__(self):
        self.agent_iterator = 0
        self.agents = []

    def create_agent(self, pos):
        self.agent_iterator += 1
        temp_agent = Agent(self.agent_iterator, pos)
        self.agents.append(temp_agent)

    def move_agents_2D(self):
        for agent in self.agents:
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            agent.move_2D([dx, dy])

    def get_agent_positions_2D(self):
        agent_positions = []
        for agent in self.agents:
            agent_positions.append([agent.pos[0], agent.pos[1]])
        return agent_positions
    
    def get_agent_positions_3D(self):
        agent_positions = []
        for agent in self.agents:
            agent_positions.append([agent.pos[0], agent.pos[1], agent.pos[2]])
        return agent_positions

    def get_agents(self):
        return self.agents
    
    