'''Player Class'''
import pygame

class Player:
    name = ""
    '''current position of the player'''
    position = [0, 0]
    velocity = 5
    _n, _s, _e, _w = False, False, False, False

    def __init__(self, name,  pos):
        '''Initialize the Player with the Give *args'''
        self.name = name
        self.position = pos

    def handle_input(self):
        '''grabs active keys that are pressed and compares to see if they are expected keys for movement'''
        keys = pygame.key.get_pressed()
        # if they are. then go ahead and move based on the position i give You.
        ## and the players velocity
        if keys[pygame.K_w]:
            ## up
            self.position[1] -= self.velocity
        if keys[pygame.K_a]:
            ## left
            self.position[0] -= self.velocity
        if keys[pygame.K_s]:
            ## down
            self.position[1] += self.velocity
        if keys[pygame.K_d]:
            ## right
            self.position[0] += self.velocity

    def set_position(self, pos):
        ''' Update the Players Position POS (x, y'''
        self.position = pos

    def update(self):
        '''Call our own handle input function here'''
        self.handle_input()
