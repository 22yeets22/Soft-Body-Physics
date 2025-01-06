import pygame

from sim.constants import FPS, HEIGHT, SUBSTEPS, WIDTH
from sim.node import Node
from sim.sim import Simulation
from sim.spring import DestroyableSpring, Spring  # noqa: F401

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tearable Cloth Demo")

# Cloth parameters (feel free to change)!!
rows = 15
cols = 20
node_distance_x = 30
node_distance_y = 25
start_x = WIDTH // 2
start_y = 20
cloth_strength = 90  # Adjusts the max force of each spring
cloth_stiffness = 1  # Adjusts the stiffness of each spring
cloth_damping = 100  # Adjusts the damping of each spring


def build():
    nodes = []
    springs = []

    # Create nodes
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * node_distance_x - cols * node_distance_x // 2
            y = start_y + row * node_distance_y
            static = row == 0
            nodes.append(Node((x, y), static=static, mass=(node_distance_x + node_distance_y) / 150))

    # Create springs
    for row in range(rows):
        for col in range(cols):
            if col < cols - 1:
                springs.append(
                    DestroyableSpring(
                        nodes[row * cols + col],
                        nodes[row * cols + col + 1],
                        node_distance_x,
                        cloth_strength,
                        force=cloth_stiffness,
                        damping=cloth_damping,
                    )
                )
            if row < rows - 1:
                springs.append(
                    DestroyableSpring(
                        nodes[row * cols + col],
                        nodes[(row + 1) * cols + col],
                        node_distance_y,
                        cloth_strength,
                        force=cloth_stiffness,
                        damping=cloth_damping,
                    )
                )

    return nodes, springs


nodes, springs = build()
sim = Simulation(
    display,
    nodes=nodes,
    springs=springs,
    substeps=SUBSTEPS,
    fps=FPS,
    width=WIDTH,
    height=HEIGHT,
    reset_func=build,
    debug=True,
)
sim.simulate()  # never stops until the user closes the window or sim.stop is called

# Alternative code below for those who want more control
# # don't call simulate() if you want to control the simulation loop yourself
# clock = pygame.time.Clock()
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     display.fill((255, 255, 255))

#     mouse_pos = pygame.mouse.get_pos()
#     mouse_pressed = pygame.mouse.get_pressed()

#     sim.update(dt, mouse_pos, mouse_pressed)
#     sim.draw()

#     pygame.display.flip()

#     dt = min(clock.tick(FPS) * FPS / 1000, 1)  # Normalize the time step (usually near 1)

# pygame.quit()
