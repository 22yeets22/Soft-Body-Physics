import pygame

from sim.constants import FPS, HEIGHT, SUBSTEPS, WIDTH
from sim.node import Node
from sim.spring import Spring

pygame.display.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bridge Demo")


# Creating a truss bridge
nodes = []
springs = []

bridge_height = 60
bridge_length = 14
spring_force = 8

separation = WIDTH / (bridge_length + 1)
for i in range(bridge_length):
    node = Node((separation * (i + 1), HEIGHT / 2 + bridge_height / 2))
    nodes.append(node)
    if i > 0:
        spring = Spring(nodes[i - 1], nodes[i], separation, spring_force, 10000)
        springs.append(spring)
nodes[0].static = True
nodes[-1].static = True

nodes2 = []
springs2 = []

for i in range(bridge_length - 1):
    node = Node((separation * (i + 1) + separation / 2, HEIGHT / 2 - bridge_height / 2))
    nodes2.append(node)
    if i > 0:
        spring = Spring(nodes2[i - 1], nodes2[i], separation, spring_force, 10000)
        springs2.append(spring)
nodes2[0].static = True
nodes2[-1].static = True

nodes.extend(nodes2)
springs.extend(springs2)

diagonal_length = ((separation / 2) ** 2 + bridge_height**2) ** 0.5
for i in range(bridge_length - 1):
    springs.append(Spring(nodes[i], nodes2[i], diagonal_length, spring_force, 10000))
    springs.append(Spring(nodes[i + 1], nodes2[i], diagonal_length, spring_force, 10000))

# End truss bridge

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
