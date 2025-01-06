# spring.py
from math import exp

import pygame

from sim.constants import SPRING_COLOR, SPRING_DAMPING, SPRING_FORCE, SPRING_MAX_FORCE, SPRING_WIDTH


class Spring:
    """
    A class to represent a spring connecting two points in a 2D space.
    Attributes:
    -----------
    point1 : Point
        The first point connected by the spring.
    point2 : Point
        The second point connected by the spring.
    force : float
        The spring force constant.
    desired_length : float
        The desired length of the spring.
    damping : float
        The damping factor for the spring.
    color : tuple
        The color of the spring when drawn.
    width : int
        The width of the spring when drawn.
    last_direction : pygame.Vector2
        The last direction vector of the spring.
    Methods:
    --------
    _calculate_force(dt):
        Calculates the force exerted by the spring based on the positions and velocities of the points.
    update(dt):
        Updates the forces applied to the points connected by the spring.
    draw(display):
        Draws the spring as a line between the two points on the given display.
    """

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

    def _calculate_force(self, dt):
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

        # Calculate the relative velocity between the two points
        relative_velocity = (self.point2.vel - self.point1.vel).dot(direction)
        damping_factor = exp(-self.damping * dt)
        new_relative_velocity = relative_velocity * damping_factor
        relative_velocity_delta = new_relative_velocity - relative_velocity

        # Calculate the damping forces to be applied to the points
        damping_force = direction * relative_velocity_delta / 2

        if self.point1.static or self.point2.static:
            damping_force *= 2

        total_force = damping_force + force
        return total_force

    def update(self, dt):
        if self.point1.static and self.point2.static:
            return

        # Uses the calculate force function to actually get the forces
        total_force = self._calculate_force(dt)
        self.point1.apply_force(-total_force, dt)
        self.point2.apply_force(total_force, dt)

    def draw(self, display):
        # Draw the spring as a line between the two points
        pygame.draw.line(display, self.color, self.point1.pos, self.point2.pos, self.width)


class DestroyableSpring(Spring):
    """
    A class representing a spring that can break if the force exceeds a maximum threshold.
    Attributes:
        point1 (Point): The first point connected by the spring.
        point2 (Point): The second point connected by the spring.
        desired_length (float): The desired length of the spring.
        max_force (float): The maximum force the spring can withstand before breaking.
        force (float): The force constant of the spring.
        damping (float): The damping constant of the spring.
        broken (bool): A flag indicating whether the spring is broken.
    Methods:
        update(dt):
            Updates the state of the spring, applying forces to the connected points and checking if the spring breaks.
        draw(display):
            Draws the spring on the given display if it is not broken.
    """

    def __init__(
        self,
        point1,
        point2,
        desired_length,
        max_force=SPRING_MAX_FORCE,
        force=SPRING_FORCE,
        damping=SPRING_DAMPING,
        **kwargs,
    ):
        super().__init__(point1, point2, desired_length, force, damping, **kwargs)
        self.max_force = max_force
        self.broken = False

    def update(self, dt):
        if self.broken or self.point1.static and self.point2.static:
            return

        total_force = self._calculate_force(dt)
        if total_force.magnitude() >= self.max_force:
            self.broken = True
            return

        self.point1.apply_force(-total_force, dt)
        self.point2.apply_force(total_force, dt)

    def draw(self, display):
        if not self.broken:
            super().draw(display)
