import random
import tkinter as tk
from agentFactory import *

class Window:

    WINDOW_W = 1200
    WINDOW_H = 800

    FIELD_W = 700
    FIELD_H = 500

    def __init__(self, root):
        """
        Initializes the application window.

        :param root: The root window of the tkinter application.
        """
        self.root = root
        self.root.title("My Application")
        self.root.geometry(str(self.WINDOW_W) + "x" + str(self.WINDOW_H))  # Width x Height

        # Add a label
        self.label = tk.Label(root, text="Welcome to My Application!", font=("Arial", 14))
        self.label.pack(pady=20)

        # Add a drawing canvas
        self.canvas = tk.Canvas(root, width=self.FIELD_W, height=self.FIELD_H, bg="white")
        self.canvas.pack(pady=20)

        # Add a button
        self.button = tk.Button(root, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

        self.factory = AgentFactory()
        self.render_2D()

    def on_button_click(self):
        """
        Handles the button click event.
        Creates an agent
        """
        x = random.randint(10, self.FIELD_W - 10) # Within the field boundaries
        y = random.randint(10, self.FIELD_H - 10)
        self.factory.create_agent([x, y])
        self.label.config(text="Button Clicked!")

    def render_agents_2D(self):
        size = 10    # Initial size of agent
        color = "red"  # Color of the agents
        for agent in self.factory.get_agent_positions_2D():
            x = agent[0]    # X-coordinate
            y = agent[1]    # Y-coordinate
            self.canvas.create_oval(
                x,
                y,
                x + size,
                y + size,
                fill=color
            )
        print("Rendering agents...")

    def render_2D(self):
        """
        The main rendering loop, called approximately 60 times per second.
        """
        self.factory.move_agents_2D()
        self.render_agents_2D()
        self.root.after(16, self.render_2D)  # Schedule next frame (~60 FPS)
