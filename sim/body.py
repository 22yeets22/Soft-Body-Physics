from math import cos, radians, sin

import pygame

from sim.constants import GRAVITY, HEIGHT, SOFT_BODY_PRESSURE, SPRING_DAMPING, SPRING_FORCE, WIDTH
from sim.node import Node
from sim.spring import Spring


class SoftBody:
    def __init__(self, nodes, edges, draggable_points=False):
        # Pass in nodes and edges as lists
        # Edges in format (node1, node2, spring_force, desired_length, spring_force, spring_damping)
        self.nodes = nodes
        self.springs = []
        self.draggable_points = draggable_points
        for edge in edges:
            self.springs.append(Spring(self.nodes[edge[0]], self.nodes[edge[1]], edge[2], edge[3], edge[4]))

    def _update_springs(self, dt):
        for spring in self.springs:
            spring.update(dt)

    def _update_nodes(self, dt, mouse_pos, mouse_pressed):
        for node in self.nodes:
            if self.draggable_points:
                node.mouse_integration(mouse_pos, mouse_pressed, dt)
            node.update(dt)

    def update(self, dt, mouse_pos, mouse_pressed):
        self._update_springs(dt)
        self._update_nodes(dt, mouse_pos, mouse_pressed)

    def draw(self, display):
        for spring in self.springs:
            spring.draw(display)

        for node in self.nodes:
            node.draw(display)


class PressurizedSoftBody(SoftBody):
    def __init__(
        self,
        sides,
        initial_size,
        pressure_force=SOFT_BODY_PRESSURE,
        spring_force=SPRING_FORCE,
        desired_length=100,
        spring_damping=SPRING_DAMPING,
        gravity=GRAVITY,
        draggable_points=False,
    ):
        nodes = [
            Node(
                (
                    WIDTH / 2 + cos(radians(i / sides * 360)) * initial_size,
                    HEIGHT / 2 + sin(radians(i / sides * 360)) * initial_size,
                ),
                gravity=gravity,
            )
            for i in range(sides)
        ]
        edges = [(i, (i + 1) % sides, spring_force, desired_length, spring_damping) for i in range(sides)]
        super().__init__(nodes, edges, draggable_points)
        self.pressure = pressure_force
        self.area = self._calculate_area()

    def _calculate_area(self):
        # Calculate area using the shoelace formula
        area = 0
        for i in range(len(self.nodes)):
            p1 = self.nodes[i].pos
            p2 = self.nodes[(i + 1) % len(self.nodes)].pos
            area += p1[0] * p2[1] - p2[0] * p1[1]
        self.area = abs(area) / 2

    def _update_pressure(self, dt):
        if self.area == 0:
            return

        pressure_per_node = self.pressure / self.area
        print(pressure_per_node)

        # Apply pressure to each node based on the ideal gas law
        # PV = nRT, assuming n, R, and T are constants, P is proportional to 1/V
        # For simplicity, we assume a 2D volume     (area) for the soft body
        for i in range(len(self.nodes)):
            p1 = self.nodes[i].pos
            p2 = self.nodes[(i + 1) % len(self.nodes)].pos
            normal = ((p2[1] - p1[1]), -(p2[0] - p1[0]))
            normal_length = (normal[0] ** 2 + normal[1] ** 2) ** 0.5
            if normal_length != 0:
                normal = (normal[0] / normal_length, normal[1] / normal_length)
                force = pygame.Vector2(normal[0] * pressure_per_node, normal[1] * pressure_per_node)
                self.nodes[i].apply_force(force, dt)

    def update(self, dt, mouse_pos, mouse_pressed):
        self._update_nodes(dt, mouse_pos, mouse_pressed)
        self._update_springs(dt)
        self._calculate_area()
        self._update_pressure(dt)
