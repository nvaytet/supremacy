import datetime
import pyglet

from .. import config


class Graphics:

    def __init__(self, game_map):

        # self.game_map = game_map
        # self.nx = self.game_map.nx
        # self.ny = self.game_map.ny
        # self.ng = self.game_map.ng

        self.window = pyglet.window.Window(game_map.nx,
                                           game_map.ny + 32,
                                           caption='Supremacy')
        self.background = pyglet.resource.image('background.png')
        self.main_batch = pyglet.graphics.Batch()

        self.economy_label = pyglet.text.Label('Economy [score]:',
                                               color=(255, 255, 255, 255),
                                               font_size=14,
                                               x=10,
                                               y=config.ny + 5,
                                               batch=self.main_batch)
        self.time_label = pyglet.text.Label(f'Time left:',
                                            color=(255, 255, 255, 255),
                                            font_size=14,
                                            x=config.nx - 150,
                                            y=config.ny + 5,
                                            batch=self.main_batch)

        self.scoreboard_label = None

        @self.window.event
        def on_draw():
            self.window.clear()
            self.background.blit(0, 0)
            self.main_batch.draw()

    def update_scoreboard(self, t, players):
        if self.scoreboard_label is not None:
            self.scoreboard_label.delete()
        t_str = str(datetime.timedelta(seconds=int(t)))[2:]
        font_size = min(14, 100 / len(players))
        p_str = [f'{name}: {value}' for name, value in players.items()]
        text = (' ' * 20).join(p_str + [t_str])
        self.scoreboard_label = pyglet.text.Label(text,
                                                  color=(255, 255, 255, 255),
                                                  font_size=font_size,
                                                  x=180,
                                                  y=config.ny + 5,
                                                  batch=self.main_batch)
