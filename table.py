from json import load
from random import randrange


with open('settings.json') as settings:
    setting = json.load(settings)
    TABLE_LENGTH = setting['TABLE_LENGTH']
    FIGURES_COUNT = setting['FIGURES_COUNT']

class Player:
    def __init__(self, name, pl_id, color, starting_point):
        self.name = name
        self.id_ = pl_id
        self.color = color
        self.starting_point = starting_point
        self.curr_point = starting_point
        self.figures_count = FIGURES_COUNT
        self.figures = []


class Figure:
    def __init__(self, player):
        self.moves_made = 0
        self.player = player
        self.position = self.player.curr_point % TABLE_LENGTH

    def move(self, points, game):
        old_pos = self.player.curr_point
        start_pos = self.player.starting_point
        new_pos = self._change_position(points, old_pos, start_pos)

        if len(game.table[new_pos]) == 1:
            game.table[new_pos] = -1
        else:
            game.table[new_pos].pop()

        if type(game.table[new_pos]) is int:
            game.table[new_pos] = [self]
        elif type(game.table[new_pos]) is list:
            if len(game.table[new_pos]) == 1:
                if game.table[new_pos].player.id_ == self.id_:
                    game.table[new_pos].append(self)
                else:
                    game.table[new_pos] = [self]
            else:
                game.table[new_pos].append(self)

        return new_pos

    def _change_position(self, points, old_pos, start_pos):
        goal = self.moves_made + points
        if goal <= TABLE_LENGTH:
            self.moves_made += points
            return (old_pos + points) % TABLE_LENGTH
        if goal in range(TABLE_LENGTH, TABLE_LENGTH + 7):
            self.moves_made += points
            return TABLE_LENGTH + (self.player.id_*4 + goal - TABLE_LENGTH)

    #to be defined
    def __eq__(self, other):
        pass


class Game:
    def __init__(self, current_player):
        self.players = []
        self.table = [-1 for x in range(TABLE_LENGTH + 24)]
        self.current_player = current_player
    def move_figure(self, figure, points):
        #auth required
        figure.move(points, self)

class Dice:
    @staticmethod
    def roll_dice():
        return (randrange(1,6), randrange(1,6))

