import pygame
from player import Player

pygame.init()


def main():
    player = Player("Player1", [100, 100])
    pygame.display.set_caption("Hello World!")

    window = pygame.display.set_mode((1200, 800))
    clock = pygame.time.Clock()

    # player_x, player_y = 100, 100
    vel = 5
    run = True

    while run:
        # watch for events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        

        window.fill((22, 22, 22))
        # draw player
        pygame.draw.circle(window, (255, 0, 0),
                           (player.position[0], player.position[1]), 20)
        pygame.display.update()

        clock.tick(60)

    pygame.quit()


main()
