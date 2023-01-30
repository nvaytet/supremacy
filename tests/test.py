from supremacy.core.engine import Engine

from template_ai import PlayerAi

neil = PlayerAi()
neil.creator = 'Neil'

drew = PlayerAi()
drew.creator = 'Drew'

simon = PlayerAi()
simon.creator = 'Simon'

jankas = PlayerAi()
jankas.creator = 'Jankas'

players = [neil, drew, simon, jankas]

eng = Engine(players=players)
eng.run()

input()