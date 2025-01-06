from time import perf_counter

import pygame

from .constants import FPS, HEIGHT, SUBSTEPS, WIDTH


class Simulation:
    """
    A class to represent a physics simulation.
    Attributes:
    display : pygame.Surface
        The display surface where the simulation is drawn.
    nodes : list, optional
        A list of nodes in the simulation (default is None).
    springs : list, optional
        A list of springs in the simulation (default is None).
    bodies : list, optional
        A list of bodies in the simulation (default is None).
    substeps : int, optional
        The number of substeps for the simulation (default is SUBSTEPS).
    fps : int, optional
        The target frames per second (default is FPS).
    width : int, optional
        The width of the simulation display (default is WIDTH).
    height : int, optional
        The height of the simulation display (default is HEIGHT).
    reset_key : int, optional
        The key used to reset the simulation (default is pygame.K_SPACE).
    reset_func : function, optional
        The function used to reset the simulation (default is lambda: None).
    debug : bool, optional
        Flag to enable or disable debug mode (default is False).
    Methods:
    update(dt, mouse_pos, mouse_pressed):
        Updates the simulation state.
    draw(display=None):
        Draws the simulation state.
    debug_draw(display):
        Draws debug information.
    reset():
        Resets the simulation state.
    simulate(callback=lambda x: None):
        Runs the main simulation loop.
    stop():
        Stops the simulation.
    """

    def __init__(
        self,
        display,
        nodes=None,
        springs=None,
        bodies=None,
        substeps=SUBSTEPS,
        fps=FPS,
        width=WIDTH,
        height=HEIGHT,
        reset_key=pygame.K_SPACE,
        reset_func=lambda: None,
        debug=False,
    ):
        # Initialize the simulation with given parameters
        self.display = display
        self.nodes = nodes if nodes else []
        self.springs = springs if springs else []
        self.bodies = bodies if bodies else []
        self.substeps = substeps
        self.target_fps = fps
        self.width = width
        self.height = height

        self.clock = pygame.time.Clock()
        self.dt = 1
        self.running = True

        self.debug = debug

        self.reset_key = reset_key
        self.reset_func = reset_func

        self.draw_time = 0
        self.avg_draw_time = 0
        self.simulate_time = 0
        self.avg_simulate_time = 0
        self.ticks = 0

    def update(self, dt, mouse_pos, mouse_pressed):
        # Update the simulation state
        if self.debug:
            start_time = perf_counter()

        substep_dt = dt / self.substeps
        for _ in range(self.substeps):
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
        # Draw the simulation state
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
            self.debug_draw(useable_display)

    def debug_draw(self, display):
        # Draw debug information
        fps = self.clock.get_fps()
        fps_color = (255, 0, 0) if fps < 30 else (0, 0, 0)
        fps_text = self.font.render(f"FPS: {fps:.1f}", False, fps_color)  # Render the FPS (for drawing)
        simulation_text = self.font.render(
            f"TPS: {self.substeps * fps / self.dt:.1f}", False, (0, 0, 0)
        )  # For all of the nerds in the code, TPS is the amount of times the physics loop runs every second

        simulate_time_text = self.font.render(f"Sim time: {self.simulate_time:.2f} ms", True, (0, 0, 0))
        draw_time_text = self.font.render(f"Draw time: {self.draw_time:.2f} ms", True, (0, 0, 0))

        display.blit(fps_text, (0, 0))
        display.blit(simulation_text, (0, 15))
        display.blit(simulate_time_text, (0, 30))
        display.blit(draw_time_text, (0, 45))

        self.avg_simulate_time = (self.avg_simulate_time * self.ticks + self.simulate_time) / (self.ticks + 1)
        self.avg_draw_time = (self.avg_draw_time * self.ticks + self.draw_time) / (self.ticks + 1)

    def reset(self):
        # Reset the simulation state using the reset function provided by the user (if any)
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
        # Main simulation loop
        self.font = pygame.font.Font(None, 18)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if self.reset_key and event.key == self.reset_key:
                        self.reset()

            self.display.fill((255, 255, 255))

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            callback(self)
            self.update(self.dt, mouse_pos, mouse_pressed)
            self.draw()

            pygame.display.flip()

            self.dt = min(
                self.clock.tick(self.target_fps) * self.target_fps / 1000, 1
            )  # Normalize the time step (usually near 1)

            self.ticks += 1

        pygame.quit()

        if self.debug:
            print(f"Ticks: {self.ticks}")
            print(f"Average simulation time: {self.avg_simulate_time:.2f} ms")
            print(f"Average draw time: {self.avg_draw_time:.2f} ms")

    def stop(self):
        # Stop the simulation
        self.running = False
