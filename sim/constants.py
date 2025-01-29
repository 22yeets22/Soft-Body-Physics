# WORLD CONSTANTS
# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Frames per second
FPS = 60

# Gravity constant
GRAVITY = 0.981

# Substeps for physics simulation
SUBSTEPS = 5

# NODES
# Elasticity coefficient for node collisions
ELASTICITY = 0.3

# Friction coefficient for nodes and surfaces
FRICTION = 0.4

# Air friction coefficient for nodes
AIR_FRICTION = 0.02

# The strength of the node dragging force from 0 to 1
DRAG_STRENGTH = 1

# Radius of each invidual node (when drawing)
NODE_RADIUS = 6

# SPRINGS
# Default damping factor for motion
SPRING_DAMPING = 2

# Default spring force
SPRING_FORCE = 1

# Default spring width (when drawing)
SPRING_WIDTH = 3

# DESTROYABLE SPRING
# Max force a destroyable spring can handle before breaking
SPRING_MAX_FORCE = 25

# PRESSURIZED SOFT BODY
SOFT_BODY_PRESSURE = 10000  # Depends on the size of the body

# RENDER

# COLORS
# Background color of the simulation
BG_COLOR = (240, 240, 240)

# Color of a node when it is being dragged
NODE_DRAGGING_COLOR = (224, 59, 47)

# Color of a node when it is idle
NODE_IDLE_COLOR = (47, 224, 59)

# Static node color
NODE_STATIC_COLOR = (50, 50, 50)

# Color of the spring connecting nodes
SPRING_COLOR = (47, 127, 224)

# Colors of colorized destroyable spring
COLOR_1 = (34, 191, 45)
COLOR_2 = (235, 64, 52)

# Debug
DEBUG_FONT = 24
