import pygame

from sim.body import DestroyablePressurizedSoftBody, PressurizedSoftBody
from sim.constants import BG_COLOR, DEBUG_FONT, FPS, GRAVITY, HEIGHT, SUBSTEPS, WIDTH
from sim.node import Node
from sim.sim import Simulation, SimulationConfig
from sim.spring import Spring


def build():
    poppable_ball = DestroyablePressurizedSoftBody(
        pos=pygame.Vector2(WIDTH / 2 - 300, HEIGHT / 2),
        sides=12,
        initial_radius=50,
        pressure_force=500_000,
        spring_force=20,
        max_force=100,
        desired_length=2,
        spring_damping=50,
        draggable_points=True,
        colorized=True,
    )
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
    return nodes, springs, [poppable_ball, inflated_ball, deflated_ball, balloon]


config = SimulationConfig(
    width=WIDTH, height=HEIGHT, fps=FPS, substeps=SUBSTEPS, background_color=BG_COLOR, debug_font_size=DEBUG_FONT
)
pygame.init()
display = pygame.display.set_mode((config.width, config.height))
pygame.display.set_caption("Pressurized Balls Demo")

nodes, springs, bodies = build()
sim = Simulation(
    display,
    config=config,
    nodes=nodes,
    springs=springs,
    bodies=bodies,
    debug=True,
)
sim.simulate()
