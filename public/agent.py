import random
import pygame
from config import *
from utils import clamp
import numpy as np

class Agent:
    """
    The unit that will be moving around the field
    """
    color = LIGHT_GRAY # Blue
    detection_color = color
    draw_perception_radius = False
    x_offset = (WINDOW_W - FIELD_W) // 2

    def __init__(self, id, position, velocity=None, max_speed=AGENT_MAX_SPEED, min_speed=AGENT_MIN_SPEED, max_force=AGENT_MAX_SPEED*0.02):
        """
        Initialize a boid with position and velocity.
        
        :param position: Initial position as a numpy array (e.g., np.array([x, y])).
        :param velocity: Initial velocity as a numpy array (default is random).
        :param max_speed: Maximum speed the boid can achieve.
        :param max_force: Maximum force applied to the boid (for steering).
        """
        self.id = id
        self.size = AGENT_SIZE
        self.position = np.array(position, dtype=float)
        self.velocity = velocity if velocity is not None else np.random.uniform(-100, 100, size=2)
        self.acceleration = np.zeros(2)  # Start with no acceleration
        self.max_speed = max_speed
        self.min_speed = min_speed
        self.max_force = max_force
        if id == 1:
            self.draw_perception_radius = True

    def __repr__(self):
        """
        Returns a string representation of the object.
        """
        posString = "" + str(int(self.pos[0]))
        for i in range(len(self.pos)):
            if i == 0:
                continue
            posString += ", " + str(int(self.pos[i]))
        accString = "" + str(self.velocity[0])
        for i in range(len(self.velocity)):
            if i == 0:
                continue
            accString += ", " + str(self.velocity[i])
        return f"{self.__class__.__name__}(id={self.id}, pos({posString}), velocity({accString}))"

    def render(self, screen):
        """
        Render the boid as a triangle pointing in the direction of its velocity.
        :param screen: The Pygame screen to draw on.
        """

        
        # Normalize the velocity to determine direction
        direction = self.velocity / (np.linalg.norm(self.velocity) + 1e-8)  # Avoid divide by zero
    
        # Scale the direction for the triangle's tip
        tip = self.position + direction * self.size

        # Calculate the perpendicular vector for the base of the triangle
        perp = np.array([-direction[1], direction[0]])  # Rotate 90 degrees
        base_left = self.position - perp * (self.size / 2)
        base_right = self.position + perp * (self.size / 2)

        # Define the triangle's vertices and apply the x-axis offset
        points = [
            (tip[0] + self.x_offset, tip[1]),
            (base_left[0] + self.x_offset, base_left[1]),
            (base_right[0] + self.x_offset, base_right[1])
        ]

        # Convert points to integers for rendering
        points = [tuple(map(int, p)) for p in points]

        # Draw the triangle
        pygame.draw.polygon(screen, self.color, points)
        if (self.draw_perception_radius):
            self.color = RED
            center = (self.position[0] + self.x_offset, self.position[1])  # Apply x_offset to x-coordinate
            pygame.draw.circle(screen, self.detection_color, (int(center[0]), int(center[1])), PERCEPTION_RADIUS, 2)
            self.detection_color = self.color # Reset color


    def update(self):
        """
        Update the boid's position based on velocity, acceleration, and delta_time.
        :param delta_time: Time elapsed since the last update (in seconds).
        """
        self.velocity += self.acceleration
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed
        if speed < self.min_speed:
            self.velocity = (self.velocity / (speed + 1e-8)) * self.min_speed
        self.position += self.velocity
        self.acceleration = np.zeros_like(self.acceleration)

    def apply_force(self, force):
        """
        Apply a force to the boid.
        :param force: A numpy array representing the force.
        """
        self.acceleration += force

    def edges(self, bounds, wall_avoid_distance=50, wall_avoid_force=AGENT_MAX_SPEED*0.08, phase_through=False):
        """
        Avoid walls by steering the boid away from them.
        :param bounds: Tuple representing the (width, height) of the field.
        :param wall_avoid_distance: Distance from the wall within which avoidance is applied.
        :param wall_avoid_force: Magnitude of the force to steer away from the wall.
        :param phase_through: Should walls be ignored and let the agent phase through.
        """
        if phase_through:
            for i in range(len(bounds)):
                if self.position[i] > bounds[i]:
                    self.position[i] = 0
                elif self.position[i] < 0:
                    self.position[i] = bounds[i]
            return

        for i in range(len(bounds)):
            # Check if the boid is near the left wall
            if self.position[i] < wall_avoid_distance:
                force = np.zeros_like(self.position)
                force[i] = wall_avoid_force
                self.apply_force(force)

            # Check if the boid is near the right wall
            elif self.position[i] > bounds[i] - wall_avoid_distance:
                force = np.zeros_like(self.position)
                force[i] = -wall_avoid_force
                self.apply_force(force)
    
    def wander(self, magnitude=0.5):
        """
        Generate a wandering force that slightly changes the boid's direction.
        :param magnitude: Maximum magnitude of the wandering force.
        :return: A wandering force vector.
        """
        wander_angle = np.random.uniform(0, 2 * np.pi)  # Random angle
        wander_vector = np.array([np.cos(wander_angle), np.sin(wander_angle)])
        return wander_vector * magnitude

    def separate(self, agents, perception_radius=PERCEPTION_RADIUS*0.5):
        """
        Steer to avoid crowding neighbors.
        :param agents: List of other agents (boids).
        :param perception_radius: Radius within which other agents affect separation.
        :return: Steering force as a numpy array.
        """
        steer = np.zeros_like(self.position)
        total = 0

        for agent in agents:
            distance = np.linalg.norm(self.position - agent.position)
            if agent != self and distance < perception_radius:
                diff = self.position - agent.position
                diff /= distance  # Normalize and weight by distance
                steer += diff
                total += 1

        if total > 0:
            self.detection_color = RED # Used to draw perception_circle
            steer /= total  # Average the separation vectors
            if np.linalg.norm(steer) > 0:
                steer = (steer / np.linalg.norm(steer)) * self.max_speed - self.velocity
                if np.linalg.norm(steer) > self.max_force:
                    steer = (steer / np.linalg.norm(steer)) * self.max_force
        return steer


    def align(self, agents, perception_radius=PERCEPTION_RADIUS):
        """
        Steer to align with the average velocity of neighbors.
        :param agents: List of other agents (boids).
        :param perception_radius: Radius within which other agents affect alignment.
        :return: Steering force as a numpy array.
        """
        avg_velocity = np.zeros_like(self.velocity)
        total = 0

        for agent in agents:
            distance = np.linalg.norm(self.position - agent.position)
            if agent != self and distance < perception_radius:
                avg_velocity += agent.velocity
                total += 1

        if total > 0:
            self.detection_color = RED # Used to draw perception_circle
            avg_velocity /= total  # Compute the average velocity
            steer = avg_velocity - self.velocity
            if np.linalg.norm(steer) > self.max_force:
                steer = (steer / np.linalg.norm(steer)) * self.max_force
            return steer
        return np.zeros_like(self.velocity)


    def cohere(self, agents, perception_radius=PERCEPTION_RADIUS):
        """
        Steer to move toward the average position of neighbors.
        :param agents: List of other agents (boids).
        :param perception_radius: Radius within which other agents affect cohesion.
        :return: Steering force as a numpy array.
        """
        avg_position = np.zeros_like(self.position)
        total = 0

        for agent in agents:
            distance = np.linalg.norm(self.position - agent.position)
            if agent != self and distance < perception_radius:
                avg_position += agent.position
                total += 1

        if total > 0:
            self.detection_color = RED # Used to draw perception_circle
            avg_position /= total  # Compute the center of mass
            direction = avg_position - self.position
            if np.linalg.norm(direction) > 0:
                direction = (direction / np.linalg.norm(direction)) * self.max_speed - self.velocity
                if np.linalg.norm(direction) > self.max_force:
                    direction = (direction / np.linalg.norm(direction)) * self.max_force
            return direction
        return np.zeros_like(self.position)

    def apply_behaviors(self, agents, settings):
        """
        Apply the three main boid behaviors (separation, alignment, cohesion).
        :param agents: List of other agents (boids).
        """
        separation = self.separate(agents) * SEPARATION_WEIGHT  # Weight for separation
        alignment = self.align(agents) * ALIGNMENT_WEIGHT       # Weight for alignment
        cohesion = self.cohere(agents) * COHESION_WEIGHT        # Weight for cohesion
        wander_force = self.wander(0.1)     # Add wandering behavior


        # Apply the combined forces
        if settings["separation"]:
            self.apply_force(separation)
        if settings["alignment"]:
            self.apply_force(alignment)
        if settings["cohesion"]:
            self.apply_force(cohesion)
        if settings["wander_force"]:
            self.apply_force(wander_force)
