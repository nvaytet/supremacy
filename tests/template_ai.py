import numpy as np

from supremacy.core.ai import Ai
from supremacy import config

CREATOR = 'JohnDoe'


class PlayerAi(Ai):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, creator=CREATOR, **kwargs)
        self.previous_positions = {}
        # self.previous_health = 0

    def run(self, t: float, dt: float, info: dict, batch):

        myinfo = info[self.creator]
        for base in myinfo['bases']:
            # print(base._data)
            if base['mines'] < 2:
                if base['crystal'] > config.cost['mine']:
                    base.build_mine()
            elif base['crystal'] > config.cost['ship']:
                base.build_ship(heading=360 * np.random.random(), batch=batch)
            # elif base.crystal > config.cost['tank']:
            #     base.build_tank(heading=360 * np.random.random(), batch=batch)

        if 'tanks' in myinfo:
            for tank in myinfo['tanks']:
                if tank['uid'] in self.previous_positions:
                    if all(tank.get_position() == self.previous_positions[tank['uid']]):
                        tank.set_heading(np.random.random() * 360.0)
                self.previous_positions[tank['uid']] = tank.get_position()

        if 'ships' in myinfo:
            for ship in myinfo['ships']:
                if ship['uid'] in self.previous_positions:
                    if all(ship.get_position() == self.previous_positions[ship['uid']]):
                        if ship.get_distance([ship['owner']['x'], ship['owner']['y']
                                              ]) > 20:
                            ship.convert_to_base()
                        else:
                            ship.set_heading(np.random.random() * 360.0)
                self.previous_positions[ship['uid']] = ship.get_position()

            # for v in base.vehicles:
            #     if hasattr(v, 'previous_position'):
            #         if all(v.position == v.previous_position):
            #             v.heading = np.random.random() * 360.0
            #     v.previous_position = v.position
