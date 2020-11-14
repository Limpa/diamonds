import random
from ..util import get_direction


class SuiciderLogic(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1
        self.goal_base = "NallePuh"
        self.goal_base_pos = -1

    def find_closest_diamond(self, board, position):
        closest = 10000
        closest_index = -1
        for i in range(len(board.diamonds)):
            dist = abs(position["x"] - board.diamonds[i].get('position')["x"]) + abs(position["y"] - board.diamonds[i].get('position')["y"])
            if dist < closest:
                closest = dist
                closest_index = i

        ## FIX IF EMPTY BOARD
        return board.diamonds[closest_index].get('position')

    def find_suicide_position(self, board, board_bot):
        name = board_bot["properties"]["name"]
        offset = (0, 0)
        if name == "helpNorth":
            offset = (0, -1)
        elif name == "helpSouth":
            offset = (0, 1)
        elif name == "helpWest":
            offset = (-1, 0)
        elif name == "helpEast":
            offset = (1, 0)

        for gameObj in board.gameObjects:
            if gameObj['type'] == 'BaseGameObject' and gameObj['properties']['name'] == self.goal_base:
                pos = gameObj['position']
                pos['x'] += offset[0]
                pos['y'] += offset[1] 
                return pos
        return board_bot["properties"]["base"]

    def dump(self, obj):
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))
            

    def next_move(self, board_bot, board):
        props = board_bot["properties"]

        # Analyze new state
        if props["diamonds"] == 5:
            # Move to base if we are full of diamonds
            if self.goal_base_pos == -1:
                self.goal_base_pos = self.find_suicide_position(board, board_bot)
            self.goal_position = self.goal_base_pos 
        else:
            # Move towards first diamond on board
            self.goal_position = self.find_closest_diamond(board, board_bot["position"]) 

        if self.goal_position:
            # Calculate move according to goal position
            current_position = board_bot["position"]
            cur_x = current_position["x"]
            cur_y = current_position["y"]
            delta_x, delta_y = get_direction(
                cur_x,
                cur_y,
                self.goal_position["x"],
                self.goal_position["y"],
            )

            if (cur_x, cur_y) == self.previous_position:
                # We did not manage to move, lets take a turn to hopefully get out stuck position
                if delta_x != 0:
                    delta_y = delta_x * self.turn_direction
                    delta_x = 0
                elif delta_y != 0:
                    delta_x = delta_y * self.turn_direction
                    delta_y = 0
                # Switch turn direction for next time
                self.turn_direction = -self.turn_direction
            self.previous_position = (cur_x, cur_y)

            print(delta_x, delta_y)
            return delta_x, delta_y

        return 0, 0
