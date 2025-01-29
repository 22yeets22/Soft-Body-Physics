from random import uniform

import pygame

from sim.constants import BG_COLOR, DEBUG_FONT, FPS, HEIGHT, SUBSTEPS, WIDTH
from sim.node import Node
from sim.sim import Simulation, SimulationConfig
from sim.spring import ColorizedDestroyableSpring


def earthquake(sim):
    leftmost_pos = sim.nodes[0].pos.x
    rightmost_pos = leftmost_pos + (building_width - 1) * node_spacing_x
    shake = (
        uniform(
            -min(earthquake_strength, abs(leftmost_pos)),
            min(earthquake_strength, abs(WIDTH - rightmost_pos)),
        )
        * sim.dt
    )
    for node in sim.nodes:
        if node.static:
            node.pos.x += shake


# Building parameters
building_x = WIDTH / 2  # Where the building starts

building_width = 4  # How many nodes wide the building is
building_height = 9  # How many nodes tall the building is

node_spacing_x = 60  # How far apart the nodes are in the x direction
node_spacing_y = 60  # How far apart the nodes are in the y direction
diagonal_node_spacing = (node_spacing_x**2 + node_spacing_y**2) ** 0.5

building_strength = 500  # Max force of the topmost floor (level)
level_difference = 65  # How much stronger each level below another should be
node_mass = 50  # How heavy each node is
building_stiffness = 75  # How stiff the springs are
building_damping = 1_000_000  # How much the springs dampen the movement

# Environment parameters
earthquake_strength = 5  # Adjusts the max force of the earthquake

# Create nodes
x1 = building_x - node_spacing_x / 2
x2 = building_x + node_spacing_x / 2


def build():
    nodes = []
    springs = []

    for i in range(building_height):
        static = i == 0
        for j in range(building_width):
            x = building_x - (building_width / 2 - j) * node_spacing_x
            node = Node((x, HEIGHT - i * node_spacing_y), mass=node_mass, static=static, draggable=not static)
            nodes.append(node)

            if j > 0:
                springs.append(
                    ColorizedDestroyableSpring(
                        nodes[-2],
                        node,
                        node_spacing_x,
                        building_strength + level_difference * (building_height - i - 1),
                        building_stiffness,
                        building_damping,
                    )
                )

            if i > 0:
                springs.append(
                    ColorizedDestroyableSpring(
                        node,
                        nodes[-building_width - 1],
                        node_spacing_y,
                        building_strength + level_difference * (building_height - i - 1),
                        building_stiffness,
                        building_damping,
                    )
                )
                if j > 0:
                    springs.append(
                        ColorizedDestroyableSpring(
                            node,
                            nodes[-building_width - 2],
                            diagonal_node_spacing,
                            building_strength + level_difference * (building_height - i - 1),
                            building_stiffness,
                            building_damping,
                        )
                    )
                if j < building_width - 1:
                    springs.append(
                        ColorizedDestroyableSpring(
                            node,
                            nodes[-building_width],
                            diagonal_node_spacing,
                            building_strength + level_difference * (building_height - i - 1),
                            building_stiffness,
                            building_damping,
                        )
                    )

    return [nodes, springs]


config = SimulationConfig(
    width=WIDTH, height=HEIGHT, fps=FPS, substeps=SUBSTEPS, background_color=BG_COLOR, debug_font_size=DEBUG_FONT
)
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earthquake Simulation Demo")

nodes, springs = build()
sim = Simulation(
    display,
    config=config,
    nodes=nodes,
    springs=springs,
    debug=True,
)
sim.simulate(earthquake)  # never stops until the user closes the window or sim.stop is called
