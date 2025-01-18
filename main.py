import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    sim_over = False

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                player.kill()
                [shot.kill() for shot in shots]
                [asteroid.kill() for asteroid in asteroids]
                asteroid_field.kill()
                sim_over = True

            for shot in shots:
                if shot.collides_with(asteroid):
                    shot.kill()
                    asteroid.split()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        if sim_over:
            font = pygame.font.Font(None, 200)
            text_surface = font.render("SIM OVER", True, 'white')
            text_rect = text_surface.get_rect()
            text_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            bg_rect = text_rect.copy()
            bg_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, 'white', bg_rect, 2)  # White outline
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
