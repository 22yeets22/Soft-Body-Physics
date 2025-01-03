from math import cos, radians, sin

import pygame

from sim.constants import FPS, HEIGHT, SUBSTEPS, WIDTH
from sim.node import Node
from sim.spring import Spring

pygame.display.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Demo")

wheel_width_apart = 110
wheel_sides = 12
wheel_size = 50

nodes = [
    Node((WIDTH // 2 - wheel_width_apart // 2, HEIGHT // 2 + 200), mass=5),
    Node((WIDTH // 2 + wheel_width_apart // 2, HEIGHT // 2 + 200), mass=5),
]
springs = []

# Create wheels
for wheel_num in range(2):
    center_node_index = wheel_num  # Center node for the current wheel
    base_index = len(nodes)  # Track where this wheel's nodes start
    for wheel_side in range(wheel_sides):
        angle = radians(wheel_side / wheel_sides * 360)
        x = nodes[center_node_index].pos[0] + cos(angle) * wheel_size
        y = nodes[center_node_index].pos[1] + sin(angle) * wheel_size
        nodes.append(Node((x, y), mass=1))
        # Connect the center node to the outside nodes
        springs.append(Spring(nodes[center_node_index], nodes[-1], desired_length=wheel_size, force=0.8, damping=5))

    # Connect the outside nodes to adjacent ones
    for wheel_side in range(wheel_sides):
        springs.append(
            Spring(
                nodes[base_index + wheel_side],
                nodes[base_index + (wheel_side + 1) % wheel_sides],
                desired_length=((2 * wheel_size) * sin(radians(180 / wheel_sides))),
                force=0.9,
                damping=10,
            )
        )

# Connect the two wheels together
springs.append(Spring(nodes[0], nodes[1], desired_length=wheel_width_apart, force=1, damping=30))


# # Add a triangle in the bottom left corner
# triangle_nodes = [
#     Node((50, HEIGHT - 50), mass=5),
#     Node((100, HEIGHT - 50), mass=5),
#     Node((75, HEIGHT - 100), mass=5),
# ]

# triangle_springs = [
#     Spring(triangle_nodes[0], triangle_nodes[1], desired_length=50, force=1, damping=5),
#     Spring(triangle_nodes[1], triangle_nodes[2], desired_length=50, force=1, damping=5),
#     Spring(triangle_nodes[2], triangle_nodes[0], desired_length=50, force=1, damping=5),
# ]

# nodes.extend(triangle_nodes)
# springs.extend(triangle_springs)


clock = pygame.time.Clock()
dt = 1

previous_ticks = pygame.time.get_ticks()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display.fill((255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    for _ in range(SUBSTEPS):
        for spring in springs:
            spring.update(dt / SUBSTEPS)

        for node in nodes:
            node.update(dt / SUBSTEPS)
            node.mouse_integration(mouse_pos, mouse_pressed, dt / SUBSTEPS)

    for spring in springs:
        spring.draw(display)
    for node in nodes:
        node.draw(display)

    pygame.display.flip()

    dt = min(clock.tick(FPS) * FPS / 1000, 1)  # Normalize the time step (usually near 1)

pygame.quit()
