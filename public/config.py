
WINDOW_W, WINDOW_H = 1280, 820

FIELD_W, FIELD_H = 1280, 600
FIELD_OFFSET_X = (WINDOW_W - FIELD_W) // 2  # Center the field horizontally
FIELD_OFFSET_Y = (WINDOW_H - FIELD_H) // 2  # Center the field vertically
FIELD_OFFSET_Y = 0 # Overwrite the field centering



AGENT_SIZE = 20
AGENT_MAX_VELOCITY = 10
AGENT_MAX_SPEED = 4
AGENT_MIN_SPEED = 3
PERCEPTION_RADIUS = 80

# BEHAVIOR WEIGHTS
SEPARATION_WEIGHT = 3.4
ALIGNMENT_WEIGHT = 1.7
COHESION_WEIGHT = 1.7


# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (190, 190, 190)