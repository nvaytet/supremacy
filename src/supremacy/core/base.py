from matplotlib import colors
import pyglet
import uuid

from .. import config
from .vehicles import Tank, Ship, Jet
from .tools import wrap_position


class Base:

    def __init__(self, x, y, team, number, batch, owner):
        self.x = x
        self.y = y
        self.team = team
        self.number = number
        self.owner = owner
        self.batch = batch
        self.tanks = {}
        self.ships = {}
        self.jets = {}
        self.uid = uuid.uuid4().hex
        self.transformed_ships = []
        self.mines = 1
        self.crystal = 0
        # self.graphics = graphics
        # self.draw_base()
        self.owner.update_player_map(x=self.x, y=self.y)
        self.avatar = pyglet.sprite.Sprite(img=config.images[f'base_{self.number}'],
                                           x=self.x,
                                           y=self.y,
                                           batch=batch)
        self.label = None
        self.make_label()
        # self.label = pyglet.text.Label(
        #     str(self.mines),
        #     #   font_name='Times New Roman',
        #     font_size=12,
        #     x=self.x,
        #     y=self.y + 10,
        #     anchor_x='center',
        #     anchor_y='center',
        #     batch=batch)

        ix = int(x)
        iy = int(y)
        dx = config.vehicle_offset
        offset = None
        while (offset is None):
            xx, yy = wrap_position(ix + dx, iy + dx)
            if self.owner.game_map[yy, xx] == 1:
                offset = (dx, dx)
                break
            xx, yy = wrap_position(ix + dx, iy - dx)
            if self.owner.game_map[yy, xx] == 1:
                offset = (dx, -dx)
                break
            xx, yy = wrap_position(ix - dx, iy + dx)
            if self.owner.game_map[yy, xx] == 1:
                offset = (-dx, dx)
                break
            xx, yy = wrap_position(ix - dx, iy - dx)
            if self.owner.game_map[yy, xx] == 1:
                offset = (-dx, -dx)
                break
            dx += 1
        self.tank_offset = offset

        dx = config.vehicle_offset
        offset = None
        while (offset is None):
            xx, yy = wrap_position(ix + dx, iy + dx)
            if self.owner.game_map[yy, xx] == 0:
                offset = (dx, dx)
                break
            xx, yy = wrap_position(ix + dx, iy - dx)
            if self.owner.game_map[yy, xx] == 0:
                offset = (dx, -dx)
                break
            xx, yy = wrap_position(ix - dx, iy + dx)
            if self.owner.game_map[yy, xx] == 0:
                offset = (-dx, dx)
                break
            xx, yy = wrap_position(ix - dx, iy - dx)
            if self.owner.game_map[yy, xx] == 0:
                offset = (-dx, -dx)
                break
            dx += 1
        self.ship_offset = offset

    # def draw_base(self):
    #     size = 15
    #     geom = p3.SphereGeometry(radius=size, widthSegments=8, heightSegments=6)
    #     mat = p3.MeshBasicMaterial(color=self.color)
    #     self.graphics.add(
    #         p3.Mesh(geometry=geom, material=mat, position=[self.x, self.y, 0]))

    def make_label(self):
        if self.label is not None:
            self.label.delete()
        color = colors.to_rgba(f'C{self.number}')
        self.label = pyglet.text.Label(
            str(self.mines),
            #   font_name='Times New Roman',
            color=tuple(int(c * 255) for c in color),
            font_size=10,
            x=self.x,
            y=self.y + 18,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)

    @property
    def vehicles(self):
        return list(self.tanks.values()) + list(self.ships.values()) + list(
            self.jets.values())

    def as_info(self):
        return {
            'x': self.x,
            'y': self.y,
            'team': self.team,
            'number': self.number,
            'mines': self.mines,
            'crystal': self.crystal,
            'uid': self.uid
        }

    def init_dt(self):
        self.transformed_ships.clear()

    def not_enough_crystal(self, kind):
        return self.crystal < config.cost[kind]

    def build_mine(self):
        if self.not_enough_crystal('mine'):
            return
        self.mines += 1
        self.make_label()
        self.crystal -= config.cost['mine']
        print('Building mine', self.mines)

    def build_tank(self, heading, batch):
        if self.not_enough_crystal('tank'):
            return
        print('Building tank')
        uid = uuid.uuid4().hex
        self.tanks[uid] = Tank(x=self.x + self.tank_offset[0],
                               y=self.y + self.tank_offset[1],
                               team=self.team,
                               number=self.number,
                               heading=heading,
                               batch=batch,
                               owner=self,
                               uid=uid)
        self.crystal -= config.cost['tank']
        # self.graphics.add(self.tanks[vid].avatar)

    def build_ship(self, heading, batch):
        if self.not_enough_crystal('ship'):
            return
        print('Building ship')
        uid = uuid.uuid4().hex
        self.ships[uid] = Ship(x=self.x + self.ship_offset[0],
                               y=self.y + self.ship_offset[1],
                               team=self.team,
                               number=self.number,
                               heading=heading,
                               batch=batch,
                               owner=self,
                               uid=uid)
        self.crystal -= config.cost['ship']
        # self.graphics.add(self.tanks[vid].avatar)

    def build_jet(self, heading, batch):
        if self.not_enough_crystal('jet'):
            return
        print('Building jet')
        uid = uuid.uuid4().hex
        self.jets[uid] = Jet(x=self.x,
                             y=self.y,
                             team=self.team,
                             number=self.number,
                             heading=heading,
                             batch=batch,
                             owner=self,
                             uid=uid)
        self.crystal -= config.cost['jet']
        # self.graphics.add(self.tanks[vid].avatar)


class BaseProxy:

    def __init__(self, base):
        self._data = base.as_info()
        self.build_mine = base.build_mine
        self.build_tank = base.build_tank
        self.build_ship = base.build_ship
        self.build_jet = base.build_jet

    def __getitem__(self, key):
        return self._data[key]

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()
