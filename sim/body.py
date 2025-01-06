from math import cos, radians, sin

import pygame

from sim.constants import GRAVITY, SOFT_BODY_PRESSURE, SPRING_DAMPING, SPRING_FORCE
from sim.node import Node
from sim.spring import Spring


class SoftBody:
    """
    A class to represent a soft body composed of nodes and springs.
    Attributes:
    -----------
    nodes : list
        A list of nodes that make up the soft body.
    springs : list
        A list of springs connecting the nodes.
    draggable_points : bool
        A flag indicating whether the nodes are draggable by the mouse.
    Methods:
    --------
    __init__(nodes, edges, draggable_points=False):
        Initializes the soft body with nodes and edges.
    _update_springs(dt):
        Updates the state of all springs over a time step dt.
    _update_nodes(dt, mouse_pos, mouse_pressed):
        Updates the state of all nodes over a time step dt, considering mouse interactions.
    update(dt, mouse_pos, mouse_pressed):
        Updates the state of the soft body over a time step dt, considering mouse interactions.
    draw(display):
        Draws the soft body on the given display.
    copy():
        Creates and returns a copy of the soft body.
    """

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
                node.mouse_integration(dt, mouse_pos, mouse_pressed)
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
    """
    A class representing a pressurized soft body, which is a type of soft body
    that maintains its shape through internal pressure.
    Attributes:
        pressure (float): The internal pressure force of the soft body.
        center_of_mass (pygame.Vector2): The center of mass of the soft body.
    Methods:
        _update_pressure(dt):
            Updates the pressure forces acting on the nodes of the soft body.
        update(dt, mouse_pos, mouse_pressed):
            Updates the state of the soft body, including pressure, springs, and nodes.
    Args:
        pos (tuple): The initial position of the soft body.
        sides (int): The number of sides (nodes) of the soft body.
        initial_radius (float): The initial radius of the soft body.
        pressure_force (float, optional): The internal pressure force. Defaults to SOFT_BODY_PRESSURE.
        spring_force (float, optional): The spring force between nodes. Defaults to SPRING_FORCE.
        desired_length (float, optional): The desired length of the springs. Defaults to 100.
        spring_damping (float, optional): The damping factor for the springs. Defaults to SPRING_DAMPING.
        gravity (pygame.Vector2, optional): The gravity vector affecting the nodes. Defaults to GRAVITY.
        draggable_points (bool, optional): Whether the nodes are draggable. Defaults to False.
    """

    def __init__(
        self,
        pos,
        sides,
        initial_radius,
        pressure_force=SOFT_BODY_PRESSURE,
        spring_force=SPRING_FORCE,
        desired_length=100,
        spring_damping=SPRING_DAMPING,
        gravity=GRAVITY,
        draggable_points=False,
    ):
        pos = pygame.Vector2(pos)
        nodes = [
            Node(
                (
                    pos.x + cos(radians(i / sides * 360)) * initial_radius,
                    pos.y + sin(radians(i / sides * 360)) * initial_radius,
                ),
                gravity=gravity,
            )
            for i in range(sides)
        ]
        edges = [(i, (i + 1) % sides, spring_force, desired_length, spring_damping) for i in range(sides)]
        super().__init__(nodes, edges, draggable_points)
        self.pressure = pressure_force
        self.center_of_mass = pos

    def _update_pressure(self, dt):
        # Calculate area using the shoelace formula
        area = 0
        center_of_mass = pygame.Vector2(0, 0)
        total_distance = 0
        distances = []

        for i in range(len(self.nodes)):
            p1 = self.nodes[i].pos
            p2 = self.nodes[(i + 1) % len(self.nodes)].pos
            area += p1[0] * p2[1] - p2[0] * p1[1]
            center_of_mass += p1
            distance = (p1 - p2).length()
            distances.append(distance)
            total_distance += distance

        area = abs(area) / 2
        center_of_mass /= len(self.nodes)
        self.center_of_mass = center_of_mass

        pressure_per_node = self.pressure / (area + 1e-8)

        # Apply pressure to each node
        for i in range(len(self.nodes)):
            p1 = self.nodes[i].pos
            p2 = self.nodes[(i + 1) % len(self.nodes)].pos

            # Compute normal vector
            normal = pygame.Vector2((p2.y - p1.y), -(p2.x - p1.x))
            if normal.length() == 0:
                continue

            normal.normalize_ip()

            # Force proportional to distance between nodes
            force = normal * pressure_per_node * distances[i] / total_distance

            self.nodes[i].apply_force(force, dt)
            self.nodes[(i + 1) % len(self.nodes)].apply_force(force, dt)

    def update(self, dt, mouse_pos, mouse_pressed):
        self._update_pressure(dt)
        self._update_springs(dt)
        self._update_nodes(dt, mouse_pos, mouse_pressed)
