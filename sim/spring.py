from math import exp

import pygame

from sim.constants import SPRING_COLOR, SPRING_DAMPING, SPRING_FORCE, SPRING_WIDTH


class Spring:
    def __init__(
        self,
        point1,
        point2,
        desired_length,
        force=SPRING_FORCE,
        damping=SPRING_DAMPING,
        color=SPRING_COLOR,
        width=SPRING_WIDTH,
    ):
        # Initialize the spring with two points, force, desired length, damping, color, and width
        self.point1 = point1
        self.point2 = point2
        self.force = force
        self.desired_length = desired_length
        self.damping = damping
        self.color = color
        self.width = width

        self.last_direction = pygame.Vector2(0, 0)

    def update(self, dt):
        # Calculate the difference in position between the two points
        delta = self.point2.pos - self.point1.pos
        distance = delta.length()
        if distance != 0:
            direction = delta / distance
            self.last_direction = direction
        else:
            direction = self.last_direction

        # Calculate the required change in position to achieve the desired length
        required_delta = direction * self.desired_length
        force = self.force * (required_delta - delta)

        # Initialize forces to be applied later
        force1 = pygame.Vector2(0, 0)
        force2 = pygame.Vector2(0, 0)

        # Calculate the forces to be applied to the points
        force1 -= force
        force2 += force

        # Calculate the relative velocity between the two points
        relative_velocity = (self.point2.vel - self.point1.vel).dot(direction)
        damping_factor = exp(-self.damping * dt)
        new_relative_velocity = relative_velocity * damping_factor
        relative_velocity_delta = new_relative_velocity - relative_velocity

        # Calculate the damping forces to be applied to the points
        damping_force = direction * relative_velocity_delta

        if self.point1.static and not self.point2.static:
            force2 += damping_force
        elif self.point2.static and not self.point1.static:
            force1 -= damping_force
        else:
            force1 -= damping_force / 2.0
            force2 += damping_force / 2.0

        # Apply the calculated forces to the points
        if not self.point1.static:
            self.point1.apply_force(force1, dt)
        if not self.point2.static:
            self.point2.apply_force(force2, dt)

    def draw(self, display):
        # Draw the spring as a line between the two points
        pygame.draw.line(display, self.color, self.point1.pos, self.point2.pos, self.width)


# Test:
# from spring import Spring; from node import Node; a, b = Node((0,0)), Node((10,0)); c = Spring(a, b, 1, 15); c.update(1); print(a.vel, b.vel)
