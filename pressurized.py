# work in progress
import pygame

from sim.body import PressurizedSoftBody
from sim.constants import FPS, HEIGHT, WIDTH

pygame.display.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pressurized Ball Demo")

pressurized_soft_body = PressurizedSoftBody(8, 100, 300000, 100, 0.5, 1, draggable_points=True)

clock = pygame.time.Clock()
dt = 1

previous_ticks = pygame.time.get_ticks()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display.fill((255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    pressurized_soft_body.update(dt, mouse_pos, mouse_pressed)
    pressurized_soft_body.draw(display)

    pygame.display.flip()

    dt = min(clock.tick(FPS) * FPS / 1000, 1)  # Normalize the time step (usually near 1)

pygame.quit()
