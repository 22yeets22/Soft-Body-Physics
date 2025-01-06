from math import exp

import pygame

from sim.constants import (
    AIR_FRICTION,
    DRAG_STRENGTH,
    ELASTICITY,
    FRICTION,
    GRAVITY,
    HEIGHT,
    NODE_DRAGGING_COLOR,
    NODE_IDLE_COLOR,
    NODE_RADIUS,
    NODE_STATIC_COLOR,
    WIDTH,
)


class Node:
    """
    A class to represent a node in a pressurized soft body ball simulation.
    Attributes
    ----------
    pos : pygame.Vector2
        The position of the node.
    mass : float, optional
        The mass of the node (default is 1).
    vel : pygame.Vector2, optional
        The velocity of the node (default is (0, 0)).
    gravity : float, optional
        The gravitational force acting on the node (default is GRAVITY).
    radius : float, optional
        The radius of the node (default is NODE_RADIUS).
    elasticity : float, optional
        The elasticity of the node (default is ELASTICITY).
    friction : float, optional
        The friction coefficient of the node (default is FRICTION).
    color : tuple, optional
        The color of the node when idle (default is NODE_IDLE_COLOR).
    dragging_color : tuple, optional
        The color of the node when being dragged (default is NODE_DRAGGING_COLOR).
    static_color : tuple, optional
        The color of the node when static (default is NODE_STATIC_COLOR).
    draggable : bool, optional
        Whether the node is draggable (default is True).
    static : bool, optional
        Whether the node is static (default is False).
    Methods
    -------
    update(dt: float) -> None:
        Updates the node's position and velocity based on the elapsed time.
    find_collisions() -> list:
        Finds and returns a list of collisions with the boundaries.
    mouse_integration(dt: float, mouse_pos: tuple, mouse_down: tuple) -> None:
        Integrates mouse interactions with the node.
    apply_force(force: pygame.Vector2, dt: float) -> None:
        Applies a force to the node.
    draw(display) -> None:
        Draws the node on the given display.
    """

    def __init__(
        self,
        pos,
        mass=1,
        vel=(0, 0),
        gravity=GRAVITY,
        radius=NODE_RADIUS,
        elasticity=ELASTICITY,
        friction=FRICTION,
        color=NODE_IDLE_COLOR,
        dragging_color=NODE_DRAGGING_COLOR,
        static_color=NODE_STATIC_COLOR,
        draggable=True,
        static=False,
    ):
        self.pos = pygame.Vector2(pos)
        self.mass = mass
        self.vel = pygame.Vector2(vel)
        self.gravity = gravity
        self.radius = radius
        self.elasticity = elasticity
        self.friction = friction
        self.color = color
        self.dragging_color = dragging_color
        self.draggable = draggable
        self.static = static
        self.static_color = static_color
        self.dragging = False

    def update(self, dt: float) -> None:
        if self.static:
            return

        self.vel.y += self.gravity * dt
        self.vel *= exp(-AIR_FRICTION * dt)
        self.pos += self.vel * dt

        collisions = self.find_collisions()

        for collision in collisions:
            if collision[0] < 0.0:
                continue

            self.pos += collision[1] * collision[0]

            normal_velocity = collision[1] * self.vel.dot(collision[1])
            tangential_velocity = self.vel - normal_velocity

            self.vel = normal_velocity * -self.elasticity + tangential_velocity * exp(-self.friction * dt)

    def find_collisions(self):
        # returns in the form depth, normal (need to look in detail later)
        collisions = []
        if self.pos.x - self.radius < 0:
            collisions.append([-(self.pos.x - self.radius), pygame.Vector2(1, 0)])
        if self.pos.x + self.radius > WIDTH:
            collisions.append([(self.pos.x + self.radius) - WIDTH, pygame.Vector2(-1, 0)])
        if self.pos.y - self.radius < 0:
            collisions.append([-(self.pos.y - self.radius), pygame.Vector2(0, 1)])
        if self.pos.y + self.radius > HEIGHT:
            collisions.append([(self.pos.y + self.radius) - HEIGHT, pygame.Vector2(0, -1)])

        return collisions

    def mouse_integration(self, dt, mouse_pos, mouse_down):
        if not self.draggable:
            return

        if not mouse_down[0] and self.dragging:
            self.dragging = False

        if (
            self.dragging
            or mouse_down[0]
            and (mouse_pos[0] - self.pos[0]) ** 2 + (mouse_pos[1] - self.pos[1]) ** 2 <= self.radius**2
        ):
            if self.static:
                self.pos = pygame.Vector2(mouse_pos)
            else:
                self.vel = pygame.Vector2(0, 0)
                self.apply_force((mouse_pos - self.pos) * DRAG_STRENGTH * self.mass, dt)

            self.dragging = True

    def apply_force(self, force: pygame.Vector2, dt: float) -> None:
        if self.static:
            return
        self.vel += force * dt / self.mass

    def draw(self, display):
        if self.dragging:
            pygame.draw.circle(display, self.dragging_color, self.pos, self.radius)
        elif self.static:
            pygame.draw.circle(display, self.static_color, self.pos, self.radius)
        else:
            pygame.draw.circle(display, self.color, self.pos, self.radius)
