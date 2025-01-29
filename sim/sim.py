from dataclasses import dataclass
from time import perf_counter
from typing import List, Optional, Tuple

import pygame


@dataclass
class SimulationConfig:
    """Configuration settings for the physics simulation."""

    width: int = 800
    height: int = 600
    fps: int = 60
    substeps: int = 8
    background_color: Tuple[int, int, int] = (255, 255, 255)
    debug_font_size: int = 18
    reset_key: int = pygame.K_SPACE
    low_fps_threshold: int = 30
    low_fps_color: Tuple[int, int, int] = (255, 0, 0)
    normal_fps_color: Tuple[int, int, int] = (0, 0, 0)


class Simulation:
    """
    Physics simulation system with performance monitoring and debug capabilities.
    """

    def __init__(
        self,
        display,
        config: Optional[SimulationConfig] = None,
        nodes: Optional[List] = None,
        springs: Optional[List] = None,
        bodies: Optional[List] = None,
        reset_key=pygame.K_SPACE,
        reset_func=None,
        debug=False,
    ):
        self.display = display
        self.config = config or SimulationConfig()

        # CHANGE: Directly pass in components
        self.nodes = nodes or []
        self.springs = springs or []
        self.bodies = bodies or []

        # Performance tracking
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.running = True
        self.debug = debug

        # Reset functionality
        self.reset_key = reset_key
        self.reset_func = reset_func or (lambda: None)

        # Debug metrics
        self.draw_time = 0
        self.avg_draw_time = 0
        self.simulate_time = 0
        self.avg_simulate_time = 0
        self.ticks = 0

        # Prepare debug font if needed
        self.font = pygame.font.Font(None, self.config.debug_font_size) if debug else None

    def update(self, dt, mouse_pos, mouse_pressed):
        """Update simulation state"""
        if self.debug:
            start_time = perf_counter()

        substep_dt = dt / self.config.substeps
        for _ in range(self.config.substeps):
            for body in self.bodies:
                body.update(substep_dt, mouse_pos, mouse_pressed)
            for spring in self.springs:
                spring.update(substep_dt)
            for node in self.nodes:
                node.mouse_integration(substep_dt, mouse_pos, mouse_pressed)
                node.update(substep_dt)

        if self.debug:
            end_time = perf_counter()
            self.simulate_time = (end_time - start_time) * 1000

    def draw(self, display=None):
        """Draw simulation state"""
        if self.debug:
            start = perf_counter()

        useable_display = display if display else self.display
        for body in self.bodies:
            body.draw(useable_display)
        for spring in self.springs:
            spring.draw(useable_display)
        for node in self.nodes:
            node.draw(useable_display)

        if self.debug:
            end = perf_counter()
            self.draw_time = (end - start) * 1000
            self._debug_draw(useable_display)

    def _debug_draw(self, display):
        """Draw debug information"""
        fps = self.clock.get_fps()
        fps_color = (255, 0, 0) if fps < 30 else (0, 0, 0)
        fps_text = self.font.render(f"FPS: {fps:.1f}", False, fps_color)
        simulation_text = self.font.render(f"TPS: {self.config.substeps * fps / self.dt:.1f}", False, (0, 0, 0))
        simulate_time_text = self.font.render(f"Sim time: {self.simulate_time:.2f} ms", True, (0, 0, 0))
        draw_time_text = self.font.render(f"Draw time: {self.draw_time:.2f} ms", True, (0, 0, 0))

        display.blit(fps_text, (0, 0))
        display.blit(simulation_text, (0, 15))
        display.blit(simulate_time_text, (0, 30))
        display.blit(draw_time_text, (0, 45))

        self.avg_simulate_time = (self.avg_simulate_time * self.ticks + self.simulate_time) / (self.ticks + 1)
        self.avg_draw_time = (self.avg_draw_time * self.ticks + self.draw_time) / (self.ticks + 1)

    def reset(self):
        """Reset the simulation state"""
        values = self.reset_func()

        if values is None:
            print(
                "No reset function provided, or incorrect return: reset function must return a list of nodes, springs and bodies"
            )
            return

        self.nodes.clear()
        if len(values) > 0 and values[0] is not None:
            self.nodes.extend(values[0])

        self.springs.clear()
        if len(values) > 1 and values[1] is not None:
            self.springs.extend(values[1])

        self.bodies.clear()
        if len(values) > 2 and values[2] is not None:
            self.bodies.extend(values[2])

    def simulate(self, callback=lambda x: None):
        """Run the main simulation loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if self.reset_key and event.key == self.reset_key:
                        self.reset()

            self.display.fill(self.config.background_color)

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            callback(self)
            self.update(self.dt, mouse_pos, mouse_pressed)
            self.draw()

            pygame.display.flip()

            self.dt = min(self.clock.tick(self.config.fps) * self.config.fps / 1000, 1)

            self.ticks += 1

        pygame.quit()

        if self.debug:
            print(f"Ticks: {self.ticks}")
            print(f"Average simulation time: {self.avg_simulate_time:.2f} ms")
            print(f"Average draw time: {self.avg_draw_time:.2f} ms")

    def stop(self):
        """Stop the simulation"""
        self.running = False
