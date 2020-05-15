import pygame as pg
from settings import *
from os import path


class Pickup(pg.sprite.Sprite):
    def __init__(self, pos_x=0, pos_y=0, image=""):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * TILESIZE
        self.rect.y = pos_y * TILESIZE


class Door(pg.sprite.Sprite):
    to = None

    def __init__(self, pos_x=0, pos_y=0):
        pg.sprite.Sprite.__init__(self)
        # load an image the size of the player..
        # just so that we can be able to walk into it
        self.image = pg.image.load(TREES_BOT_MIDDLE)
        # create the rectangle
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0))
        self.rect.x = pos_x * TILESIZE
        self.rect.y = pos_y * TILESIZE
        self.destructable = False


class Wall(pg.sprite.Sprite):
    def __init__(self, pos_x=0, pos_y=0, sprite=None, destructable=False, scale=(0, 0)):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(sprite)
        self.image = pg.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x * TILESIZE
        self.rect.y = pos_y * TILESIZE
        self.destructable = destructable


class Chunk(object):
    exit_n = None,
    exit_e = None,
    exit_s = None,
    exit_w = None,
    player_position = []

    def __init__(self, chunk_id=0, walls=[], doors=[], pickups=[], is_dungeon=False):
        self.wall_list = pg.sprite.Group()
        self.door_list = pg.sprite.Group()
        self.pickup_list = pg.sprite.Group()
        self.walls = walls
        self.doors = doors
        self.pickups = pickups
        self.is_dungeon = is_dungeon
        self.show = False
        self.chunk_id = chunk_id

        for wall in walls:
            self.wall_list.add(wall)
        for door in self.doors:
            self.door_list.add(door)
        for pickup in self.pickups:
            self.pickup_list.add(pickup)

    # def __repr__(self):
    #     return self.doors
    def get_id(self):
        return self.chunk_id
    # def __str__(self):
    #     return "walls: {walls}\n doors: {doors} ".format(walls=self.walls, doors=self.doors)


def read_file():
    # read all lines from file
    # remove all '\n' -> strip
    # separate by ~ for each chunk
    # separate by line to get each row
    # empty spaces .
    # walls => 1, 2, 3
    # dungeon walls =>  4, 5, 6

    rows = []
    print("hey for some reason i am reading a file")

    with open('bin/overworld.txt', 'r') as f:
        lines = f.read()
        blocks = lines.split("~")
        for block in blocks:
            rows.append(block.split("\n"))

    f.closed
    names = []
    walls_data = []
    # each chunk needs a name and a Room()
    # names

    # walls_data = []
    for (i, row) in enumerate(rows):
        # walls data += [...[]]
        # after 3 runs = [[], [], [],]
        walls_data.append([])
        # pull the names from the first index of the row.
        # [ [NAME , ...DATA], [NAME2, ...DATA2] ]
        names.append(row[0])
        # splits the data into rows
        for col in row[1:]:
            # walls_data [
            #        row [
            #              col ["1","1","1"],
            #              col ["1",".","1"],
            #              col ["1","1","1"],
            #           ],
            #       row [
            #              col ["1","1","1"],
            #              col ["1",".","1"],
            #              col ["1","1","1"],
            #            ],
            #        row [
            #              col ["1","1","1"],
            #              col ["1",".","1"],
            #              col ["1","1","1"],
            #            ]
            #       ]
            # add the lists to a new list.. but split them first
            cols = col.split()
            # add the list to the wall data at the current index we are looking at
            walls_data[i].append(cols)
    # Rooms
    return walls_data, names

# generate_overworld()


class OverWorld:
    pickups = {
        "wooden-sword": Pickup(7, 5, WOODEN_SWORD)
    }

    def __init__(self):
        self.walls_data, self.chunk_names = read_file()
        self.chunks = {}
        self.generate_chunk(0)
        self.link_chunks()
        self.player_position = []

    def generate_chunk(self, chunk_id):
        # walls data is a 3D array
        # 1 holding the chunk_whole data
        # 1 holding each chunk
        # 1 holding each of the chunks row data {WALLS, PICKUPS, SPAWN}
        # so we need to go three layers deep wth an x y z approach
        print("hey for some reason i am generating a chunk")
        _walls = []
        _doors = []
        _chunk = {}
        for data in self.walls_data:
            # this will allow us to get each chunk
            # <----- this is where i have to splice the generation
            for (x, chunk) in enumerate(self.walls_data[chunk_id]):
                # _walls_data[0]
                # this will allow us to get each wall
                for (y, wall) in enumerate(chunk):
                    if wall == "1":
                        _walls.append(Wall(y, x, TREES_BOT_RIGHT))
                    if wall == "2":
                        _walls.append(Wall(y, x, TREES_BOT_MIDDLE))
                    if wall == "3":
                        _walls.append(Wall(y, x, TREES_BOT_LEFT))
                    if wall == "4":
                        _walls.append(Wall(y, x, TREES_TOP_RIGHT))
                    if wall == "5":
                        _walls.append(Wall(y, x, TREES_TOP_MIDDLE))
                    if wall == "6":
                        _walls.append(Wall(y, x, TREES_TOP_LEFT))
                    if wall == "T":
                        _walls.append(Wall(y, x, SINGLE_TREE))
                    elif wall == "*":
                        _doors.append(Door(y, x))
        # return _walls, _doors

        # finally create the level
        for (i, row) in enumerate(self.walls_data):
            # print(row, self.chunks[i])
            self.chunks[self.chunk_names[i]] = Chunk(
                chunk_id=i, walls=_walls, doors=_doors, is_dungeon=False)
            self.doors = _doors
            self.walls = _walls

        _chunk = self.chunks
        self.current_chunk = _chunk[self.chunk_names[chunk_id]]
        # self.current_chunk.doors = self.doors
        self.link_chunks()
        return self.current_chunk
        # return _chunk

    def link_chunks(self):
        # [ g7 ] [ h7 ] [ i7 ]
        # [ g8 ] [ h8 ] [ i8 ]

        # self.chunks["secret-room"].exit_s = self.chunks["overworld-H-8"]
        # self.chunks["secret-room"].player_position = [512, 700]
        # self.chunks["overworld-H-8"].doors[0].to = self.chunks["secret-room"]
        self.chunks["overworld-H-7"].exit_s = self.chunks["overworld-H-8"]
        self.chunks["overworld-H-8"].exit_n = self.chunks["overworld-H-7"]
        self.chunks["overworld-H-8"].exit_e = self.chunks["overworld-H-9"]
        self.chunks["overworld-H-9"].exit_w = self.chunks["overworld-H-8"]
