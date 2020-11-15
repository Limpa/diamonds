import random
from ..util import get_direction


class ResetterLogic(object):
    def __init__(self):
        self.goal_position = None

    def get_reset_pos(self, board):
        for gameObj in board.gameObjects:
            if gameObj['type'] == 'DiamondButtonGameObject':
                return gameObj['position']

    def next_move(self, board_bot, board):
        return get_direction(board_bot["position"], self.get_reset_pos(board))

