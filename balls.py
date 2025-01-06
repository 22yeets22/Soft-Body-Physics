import pygame

from sim.body import PressurizedSoftBody
from sim.constants import FPS, GRAVITY, HEIGHT, SUBSTEPS, WIDTH
from sim.node import Node
from sim.sim import Simulation
from sim.spring import Spring

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pressurized Balls Demo")


def build():
    inflated_ball = PressurizedSoftBody(
        pos=pygame.Vector2(WIDTH / 2 - 200, HEIGHT / 2),
        sides=12,
        initial_radius=50,
        pressure_force=500_000,
        spring_force=20,
        desired_length=2,
        spring_damping=50,
        draggable_points=True,
    )
    deflated_ball = PressurizedSoftBody(
        pos=pygame.Vector2(WIDTH / 2, HEIGHT / 2),
        sides=12,
        initial_radius=50,
        pressure_force=75_000,
        spring_force=20,
        desired_length=2,
        spring_damping=50,
        draggable_points=True,
    )
    balloon = PressurizedSoftBody(
        pos=pygame.Vector2(WIDTH / 2 + 200, HEIGHT / 2 - 100),
        sides=12,
        initial_radius=50,
        pressure_force=400_000,
        spring_force=20,
        desired_length=2,
        spring_damping=50,
        draggable_points=True,
        gravity=-GRAVITY,
    )
    nodes = [Node(pos=(WIDTH / 2 + 200, HEIGHT / 2)), Node(pos=(WIDTH / 2 + 200, HEIGHT / 2 + 100), static=True)]
    springs = [Spring(nodes[0], balloon.nodes[0], 75, 0.8, 10), Spring(nodes[0], nodes[1], 75, 0.8, 10)]
    return nodes, springs, [inflated_ball, deflated_ball, balloon]


nodes, springs, bodies = build()
sim = Simulation(
    display,
    nodes,
    springs,
    bodies,
    substeps=SUBSTEPS,
    fps=FPS,
    width=WIDTH,
    height=HEIGHT,
    reset_func=build,
    debug=True,
)
sim.simulate()
