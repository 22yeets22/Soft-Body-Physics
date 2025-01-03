from random import randint  # noqa: F401

import pygame

from sim.constants import FPS, HEIGHT, SUBSTEPS, WIDTH
from sim.node import Node
from sim.spring import Spring

pygame.display.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cloth Simulation Demo")

nodes = []
springs = []

rows = 12
cols = 16
node_distance = 30
start_x = WIDTH // 2
start_y = 20

# Create nodes
for row in range(rows):
    for col in range(cols):
        x = start_x + col * node_distance - cols * node_distance // 2
        y = start_y + row * node_distance
        static = row == 0
        nodes.append(Node((x, y), static=static, mass=1))

# Create springs
for row in range(rows):
    for col in range(cols):
        if col < cols - 1:
            springs.append(Spring(nodes[row * cols + col], nodes[row * cols + col + 1], node_distance, 1, 10000))
        if row < rows - 1:
            springs.append(Spring(nodes[row * cols + col], nodes[(row + 1) * cols + col], node_distance, 1, 10000))


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
    # pressurized_soft_body.update(dt / 10, mouse_pos, mouse_pressed)
    # pressurized_soft_body.draw(display)

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
