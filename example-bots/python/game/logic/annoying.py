import random
from ..util import get_direction
from ..util import random_move
from ..util import compute_distance
from ..util import position_equals


class AnnoyingLogic(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1
        self.goal_base = "NallePuh"
        self.goal_base_pos = -1

    def find_closest_diamond(self, board, position, single):
        closest = 10000
        closest_index = -1
        for i in range(len(board.diamonds)):
            if single and board.diamonds[i]["properties"]["points"] == 2:
                continue
            dist = compute_distance(position, board.diamonds[i].get('position'))
            if dist < closest:
                closest = dist
                closest_index = i

        ## FIX IF EMPTY BOARD
        return board.diamonds[closest_index].get('position')

    def find_suicide_position(self, board, board_bot):
        name = board_bot["properties"]["name"]
        offset = (0, 0)
        if name == "helpNorth" or name == "Ior":
            offset = (0, -1)
        elif name == "helpSouth" or name == "Tiger":
            offset = (0, 1)
        elif name == "helpWest" or name == "Uggla":
            offset = (-1, 0)
        elif name == "helpEast" or name == "Nasse":
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
            
    def get_reset_pos(self, board):
        for gameObj in board.gameObjects:
            if gameObj['type'] == 'DiamondButtonGameObject':
                return gameObj['position']

    def avoid_home_and_players(self, delta_x, delta_y, self_pos, base_pos, gameObjects):
        if delta_x == 0 and delta_y == 0:
            return delta_x, delta_y
        new_pos = {"x": self_pos["x"] + delta_x, "y": self_pos["y"] + delta_y}
        rand_dir = 1 if random.random() > 0.5 else -1
        if position_equals(new_pos, base_pos):
            if delta_x != 0:
                return 0, rand_dir
            else:
                return rand_dir, 0

        for gameObj in gameObjects:
            if gameObj["type"] != 'BotGameObject':
                continue
            if position_equals(new_pos, gameObj['position']):
                if delta_x != 0:
                    return 0, rand_dir
                else:
                    return rand_dir, 0

        return delta_x, delta_y



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
            self.goal_position = self.find_closest_diamond(board, board_bot["position"], props['diamonds'] == 4) 
        

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

            if (delta_x, delta_y) == (0, 0) and props["diamonds"] != 5: 
                return random_move()

            return delta_x, delta_y

        return 0, 0
