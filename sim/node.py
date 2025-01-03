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
    WIDTH,
)


class Node:
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
        self.dragging = False

    def update(self, dt):
        if self.static:
            return

        self.vel.y += self.gravity * dt
        self.vel *= exp(-AIR_FRICTION * dt)
        self.pos += self.vel * dt

        collisions = self.find_collisions()

        for collision in collisions:
            if collision["depth"] < 0.0:
                continue

            self.pos += collision["normal"] * collision["depth"]

            normal_velocity = collision["normal"] * self.vel.dot(collision["normal"]) * -self.elasticity
            tangential_velocity = (self.vel - normal_velocity) * exp(-self.friction * dt)

            self.vel = normal_velocity + tangential_velocity

    def mouse_integration(self, mouse_pos, mouse_down, dt):
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

    def find_collisions(self):
        collisions = []

        if self.pos.x - self.radius < 0:
            collisions.append({"depth": -(self.pos.x - self.radius), "normal": pygame.Vector2(1, 0)})
        if self.pos.x + self.radius > WIDTH:
            collisions.append({"depth": (self.pos.x + self.radius) - WIDTH, "normal": pygame.Vector2(-1, 0)})
        if self.pos.y - self.radius < 0:
            collisions.append({"depth": -(self.pos.y - self.radius), "normal": pygame.Vector2(0, 1)})
        if self.pos.y + self.radius > HEIGHT:
            collisions.append({"depth": (self.pos.y + self.radius) - HEIGHT, "normal": pygame.Vector2(0, -1)})

        return collisions

    def apply_force(self, force, dt):
        self.vel += force * dt / self.mass

    def draw(self, display):
        if self.dragging:
            pygame.draw.circle(display, self.dragging_color, self.pos, self.radius)
        else:
            pygame.draw.circle(display, self.color, self.pos, self.radius)
