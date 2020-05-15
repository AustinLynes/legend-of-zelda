import pygame as pg
from settings import *
from player import Player
import sys
from os import path
from overworld import *

vec2 = pg.math.Vector2

"""
    - SCREENS
        [ TITLE => GAME ]

"""


class Game:
    running = True

    def __init__(self, width=1024, height=768):
        #  initalize pygame
        pg.init()
        # get the first plugged in Joystick PS4 or X_BONE controller
        if pg.joystick.get_count() > 0:
            self.joystick = pg.joystick.Joystick(0)
            self.joystick.init()
        # screen setup
        self.dimensions = vec2()
        self.dimensions[:] = width, height
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((width, height))
        # create internal clock
        self.clock = pg.time.Clock()

        self.player = Player(7, 5)
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.player)

        self.overworld = OverWorld()
        self.current_chunk = self.overworld.current_chunk
        self.player.walls = self.overworld.current_chunk.wall_list
        self.player.doors = self.overworld.current_chunk.door_list

        self.current_screen = "title"

    def main_loop(self):
        pg.mixer.music.load(MAIN_THEME)
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.02)

        while self.running:
            if(self.current_screen == "game"):
                self.handle_events()
                self.draw()
                self.all_sprites.update()
                self.change_room()
            elif(self.current_screen == "title"):
                self.handle_title_events()
                self.draw_title()

            self.clock.tick(60)
            pg.display.set_caption(
                f"{TITLE}  --  FPS:  {self.clock.get_fps():.1f}")
        pg.quit()

    def change_room(self):
        # right side of screen ->| will
        # transition to the east
        width, height = self.dimensions
        if self.player.rect.x > width:
            # update the current position to the new chunk
            # change the current chunk to the new chunk
            _id = self.current_chunk.exit_e.get_id()
            self.current_chunk = self.overworld.generate_chunk(_id)
            # self.current_chunk = self.current_chunk.exit_e
            self.player.walls = self.current_chunk.wall_list
            self.player.doors = self.current_chunk.door_list
            self.player.rect.x = 0

        elif self.player.rect.x < 0:
            _id = self.current_chunk.exit_w.get_id()
            self.current_chunk = self.overworld.generate_chunk(_id)
            # self.current_chunk = self.current_chunk.exit_w
            self.player.walls = self.current_chunk.wall_list
            self.player.doors = self.current_chunk.door_list
            self.player.rect.x = 16 * TILESIZE

        elif self.player.rect.y > height:
            _id = self.current_chunk.exit_s.get_id()
            self.current_chunk = self.overworld.generate_chunk(_id)
            # self.current_chunk = self.current_chunk.exit_s
            self.player.walls = self.current_chunk.wall_list
            self.player.doors = self.current_chunk.door_list
            self.player.rect.y = 0 * TILESIZE

        elif self.player.rect.y < 0:
            _id = self.current_chunk.exit_n.get_id()
            self.current_chunk = self.overworld.generate_chunk(_id)
            self.player.walls = self.current_chunk.wall_list
            self.player.doors = self.current_chunk.door_list
            self.player.rect.y = height - 64

    def draw(self):
        # add check for dungeon here
        if self.current_chunk.is_dungeon:
            self.screen.fill((20, 20, 20))
        else:
            self.screen.fill(CLEAR_COLOR)
        self.current_chunk.wall_list.draw(self.screen)
        self.current_chunk.door_list.draw(self.screen)
        self.current_chunk.pickup_list.draw(self.screen)

        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def draw_title(self):
        # give the screen a background_color
        self.screen.fill((80, 80, 80))
        logo = pg.image.load(path.join(UI_PATH, "title.png"))
        credit = pg.image.load(path.join(UI_PATH, "credits.png"))
        self.screen.blit(logo, (220, 200))
        self.screen.blit(credit, (300, 443))
        pg.display.flip()

    def handle_events(self):
        events = pg.event.get()
        for e in events:
            if e.type == pg.QUIT:
                self.running = False

            if e.type == pg.JOYHATMOTION:

                x_hat = self.joystick.get_hat(0)[0]
                y_hat = self.joystick.get_hat(0)[1]

                if y_hat == 1:
                    self.player.up_pressed = True
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    self.player.direction = self.player.up
                elif y_hat == -1:
                    self.player.up_pressed = False
                    self.player.down_pressed = True
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    self.player.direction = self.player.down
                elif x_hat == 1:
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = True
                    self.player.direction = self.player.right
                elif x_hat == -1:
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = True
                    self.player.right_pressed = False
                    self.player.direction = self.player.left
                else:
                    door_hit_list = pg.sprite.spritecollide(
                        self.player, self.player.doors, False)
                    for door in door_hit_list:
                        self.current_chunk = door.to
                        self.player.walls = door.to.wall_list
                        self.player.rect.x = door.to.player_position[0]
                        self.player.rect.y = door.to.player_position[1]
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False

            if e.type == pg.JOYBUTTONDOWN:
                if self.joystick.get_button(0) and self.player.has_sword:  # []
                    self.player.attack_pressed = True
                    self.player.can_move = False
                    self.player.sounds["sword"].play()
                    if self.player.direction == self.player.up:
                        # play attack anim.
                        self.player.image = self.player.images["attack-up"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        self.player.rect.y -= 30
                    if self.player.direction == self.player.down:
                        # play attack anim.
                        self.player.image = self.player.images["attack-down"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x
                        self.player.rect.y = oldrect.y + 15

                    if self.player.direction == self.player.left:
                        # play attack anim.
                        self.player.image = self.player.images["attack-left"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x - 30
                        self.player.rect.y = oldrect.y

                    if self.player.direction == self.player.right:
                        # play attack anim.
                        self.player.image = self.player.images["attack-right"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x + 15
                        self.player.rect.y = oldrect.y

                        self.player.action = "attacking"
                if self.joystick.get_button(1):  # X
                    pass
                if self.joystick.get_button(2):  # ()
                    pass
                if self.joystick.get_button(3):  # /_\
                    pass
            if e.type == pg.JOYBUTTONUP and self.player.has_sword:
                self.player.can_move = True
                self.player.attack_pressed = False
                if self.player.direction == self.player.up:
                    # play attack anim.
                    self.player.image = self.player.images["idle-up"]
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    self.player.rect.y += 30
                if self.player.direction == self.player.down:
                    # play attack anim.
                    self.player.image = self.player.images["idle-down"]
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    oldrect = self.player.rect
                    self.player.rect = self.player.image.get_rect()
                    self.player.rect.x = oldrect.x
                    self.player.rect.y = oldrect.y - 15
                if self.player.direction == self.player.left:
                    # play attack anim.
                    self.player.image = self.player.images["idle-left"]
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    self.player.rect.x += 30
                if self.player.direction == self.player.right:
                    # play attack anim.
                    self.player.image = self.player.images["idle-right"]
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    oldrect = self.player.rect
                    self.player.rect = self.player.image.get_rect()
                    self.player.rect.x = oldrect.x - 15
                    self.player.rect.y = oldrect.y
            # KEYBOARD
            """
                W => Move Up
                A => Move Left
                S => Move Down
                D => Move Right
            """
            if e.type == pg.KEYDOWN and self.player.can_move == True:
                # UP

                if e.key == pg.K_w:
                    self.player.up_pressed = True
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    self.player.direction = self.player.up

                # DOWN
                if e.key == pg.K_s:
                    self.player.down_pressed = True
                    self.player.up_pressed = False
                    self.player.left_pressed = False
                    self.player.right_pressed = False
                    self.player.direction = self.player.down
                # LEFT
                if e.key == pg.K_a:
                    self.player.left_pressed = True
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.right_pressed = False
                    self.player.direction = self.player.left
                # RIGHT
                if e.key == pg.K_d:
                    self.player.right_pressed = True
                    self.player.up_pressed = False
                    self.player.down_pressed = False
                    self.player.left_pressed = False
                    self.player.direction = self.player.right
                # ATTACK
                if e.key == pg.K_SPACE and self.player.has_sword:
                    self.player.attack_pressed = True
                    self.player.can_move = False
                    self.player.sounds["sword"].play()
                    if self.player.direction == self.player.up:
                        # play attack anim.
                        self.player.image = self.player.images["attack-up"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        self.player.rect.y -= 30
                    if self.player.direction == self.player.down:
                        # play attack anim.
                        self.player.image = self.player.images["attack-down"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x
                        self.player.rect.y = oldrect.y + 15

                    if self.player.direction == self.player.left:
                        # play attack anim.
                        self.player.image = self.player.images["attack-left"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x - 30
                        self.player.rect.y = oldrect.y

                    if self.player.direction == self.player.right:
                        # play attack anim.
                        self.player.image = self.player.images["attack-right"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x + 15
                        self.player.rect.y = oldrect.y

                        self.player.action = "attacking"

            if e.type == pg.KEYUP:
                # door_hit_list = pg.sprite.spritecollide(
                #     self.player, self.player.doors, False)
                # for door in door_hit_list:
                #     self.current_chunk = door.to
                #     self.overworld.generate_chunk(1)
                #     self.player.walls = door.to.walls
                #     self.player.rect.x = door.to.player_position[0]
                #     self.player.rect.y = door.to.player_position[1]
                if e.key == pg.K_w:
                    self.player.up_pressed = False
                if e.key == pg.K_s:
                    self.player.down_pressed = False
                if e.key == pg.K_a:
                    self.player.left_pressed = False
                if e.key == pg.K_d:
                    self.player.right_pressed = False
                if e.key == pg.K_SPACE and self.player.has_sword:
                    self.player.can_move = True
                    self.player.attack_pressed = False
                    if self.player.direction == self.player.up:
                        # play attack anim.
                        self.player.image = self.player.images["idle-up"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        self.player.rect.y += 30
                    if self.player.direction == self.player.down:
                        # play attack anim.
                        self.player.image = self.player.images["idle-down"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x
                        self.player.rect.y = oldrect.y - 15

                    if self.player.direction == self.player.left:
                        # play attack anim.
                        self.player.image = self.player.images["idle-left"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        self.player.rect.x += 30

                    if self.player.direction == self.player.right:
                        # play attack anim.
                        self.player.image = self.player.images["idle-right"]
                        self.player.up_pressed = False
                        self.player.down_pressed = False
                        self.player.left_pressed = False
                        self.player.right_pressed = False
                        oldrect = self.player.rect
                        self.player.rect = self.player.image.get_rect()
                        self.player.rect.x = oldrect.x - 15
                        self.player.rect.y = oldrect.y

    def handle_title_events(self):
        events = pg.event.get()
        for e in events:
            # if the main event is quit.. then force quit the game
            if e.type == pg.QUIT:
                self.running = False
            # check for key evenets on this page
            if e.type == pg.JOYBUTTONDOWN:
                if self.joystick.get_button(9):
                    self.current_screen = "game"

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_RETURN:
                    self.current_screen = "game"


"""
   220       220
 | --  [360] -- |
    800 - 360 = 440
    440 / 2 = 220
"""
