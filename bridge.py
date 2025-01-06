import pygame

from sim.constants import FPS, HEIGHT, SUBSTEPS, WIDTH
from sim.node import Node
from sim.sim import Simulation
from sim.spring import DestroyableSpring

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wobbly Rope Bridge Demo")

bridge_height = 60
bridge_length = 14
spring_force = 10
bridge_strength = 500
bridge_damping = 50_000
bridge_mass = 2

separation = WIDTH / (bridge_length + 1)


def build():
    nodes = []
    springs = []
    for i in range(bridge_length):
        node = Node((separation * (i + 1), HEIGHT / 2 + bridge_height / 2), mass=bridge_mass)
        nodes.append(node)
        if i > 0:
            spring = DestroyableSpring(
                nodes[i - 1], nodes[i], separation, bridge_strength, spring_force, bridge_damping
            )
            springs.append(spring)
    nodes[0].static = True
    nodes[-1].static = True

    nodes2 = []
    springs2 = []

    for i in range(bridge_length - 1):
        node = Node((separation * (i + 1) + separation / 2, HEIGHT / 2 - bridge_height / 2), mass=bridge_mass)
        nodes2.append(node)
        if i > 0:
            spring = DestroyableSpring(
                nodes2[i - 1], nodes2[i], separation, bridge_strength, spring_force, bridge_damping
            )
            springs2.append(spring)
    nodes2[0].static = True
    nodes2[-1].static = True

    nodes.extend(nodes2)
    springs.extend(springs2)

    diagonal_length = ((separation / 2) ** 2 + bridge_height**2) ** 0.5
    for i in range(bridge_length - 1):
        springs.append(
            DestroyableSpring(nodes[i], nodes2[i], diagonal_length, bridge_strength, spring_force, bridge_damping)
        )
        springs.append(
            DestroyableSpring(nodes[i + 1], nodes2[i], diagonal_length, bridge_strength, spring_force, bridge_damping)
        )

    return nodes, springs


nodes, springs = build()
sim = Simulation(
    display, nodes, springs, None, substeps=SUBSTEPS, fps=FPS, width=WIDTH, height=HEIGHT, reset_func=build, debug=True
)
sim.simulate()

# clock = pygame.time.Clock()
# dt = 1

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     display.fill((255, 255, 255))

#     mouse_pos = pygame.mouse.get_pos()
#     mouse_pressed = pygame.mouse.get_pressed()

#     for _ in range(SUBSTEPS):
#         for spring in springs:
#             spring.update(dt / SUBSTEPS)

#         for node in nodes:
#             node.mouse_integration(dt / SUBSTEPS, mouse_pos, mouse_pressed)
#             node.update(dt / SUBSTEPS)

#     for spring in springs:
#         spring.draw(display)
#     for node in nodes:
#         node.draw(display)

#     pygame.display.flip()

#     dt = min(clock.tick(FPS) * FPS / 1000, 1)  # Normalize the time step (usually near 1)

# pygame.quit()
