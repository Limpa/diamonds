import random
import time
from ..util import get_direction
from ..util import random_move
from ..util import compute_distance
from ..util import position_equals


class SuiciderLogic(object):
    def __init__(self):
        self.goal_position = None
        self.previous_position = (None, None)
        self.turn_direction = 1
        self.goal_base = "NallePuh"
        self.goal_base_pos = -1
        self.goal_base_valid = False

    def find_teleports(self, board, self_pos):
        teleports = []
        for gameObj in board.gameObjects:
            if gameObj["type"] == 'TeleportGameObject':
                teleports.append(gameObj["position"])
                if len(teleports) == 2:
                    break
        dist_1 = compute_distance(self_pos, teleports[0])
        dist_2 = compute_distance(self_pos, teleports[1])
        return (teleports[0], teleports[1]) if dist_1 < dist_2 else (teleports[1], teleports[0])


    def find_closest_diamond(self, board, position, single):
        closest = 10000
        closest_index = -1
        using_tele = False

        tele_in, tele_out = self.find_teleports(board, position)
        tele_dist = compute_distance(position, tele_in)

        for i in range(len(board.diamonds)):
            if single and board.diamonds[i]["properties"]["points"] == 2:
                continue
            dist = compute_distance(position, board.diamonds[i].get('position'))
            diamond_dist = compute_distance(tele_out, board.diamonds[i].get('position')) + tele_dist
            if dist < closest:
                closest = dist
                closest_index = i
                using_tele = False
            if diamond_dist < closest:
                closest = diamond_dist
                closest_index = i
                using_tele = True

        return board.diamonds[closest_index].get('position') if not using_tele else tele_in

    def find_goal_base_pos(self, board, board_bot):
        for gameObj in board.gameObjects:
            if gameObj['type'] == 'BaseGameObject' and gameObj['properties']['name'] == self.goal_base:
                pos = gameObj['position']
                pos['x'] += offset[0]
                pos['y'] += offset[1] 
                return pos
        raise

    def find_suicide_position(self, board, board_bot):
        name = board_bot["properties"]["name"]
        offset = (0, 0)
        if name == "helpNorth" or name == "Ior" or name == "limpis":
            offset = (0, -1)
        elif name == "helpSouth" or name == "Tiger" or name == "hejhopp":
            offset = (0, 1)
        elif name == "helpWest" or name == "Uggla" or name == "LilleRu":
            offset = (-1, 0)
        elif name == "helpEast" or name == "Nasse" or name == "Kengu":
            offset = (1, 0)

        for gameObj in board.gameObjects:
            if gameObj['type'] == 'BaseGameObject' and gameObj['properties']['name'] == self.goal_base:
                pos = gameObj['position']
                pos['x'] += offset[0]
                pos['y'] += offset[1] 
                return pos
        raise

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
        reset_pos = self.get_reset_pos(board)
        reset_dist = compute_distance(board_bot["position"], reset_pos)

        # Analyze new state
        if props["diamonds"] == 5 or props['millisecondsLeft'] < 5000:
            # find position of goal
            if not self.goal_base_valid:
                try:
                    self.goal_base_pos = self.find_suicide_position(board, board_bot) 
                    self.goal_base_valid = True
                except:
                    self.goal_base_pos = board_bot["position"]

            self.goal_position = self.goal_base_pos

            # Use teleporter if it is closer
            self_pos = board_bot["position"]
            tele_in, tele_out = self.find_teleports(board, self_pos)
            if compute_distance(self_pos, tele_in) + compute_distance(self.goal_position, tele_out) < compute_distance(self_pos, self.goal_position):
                self.goal_position = tele_in
        elif reset_dist <= 2 or len(props["diamonds"]) < 3:
            self.goal_position = reset_pos
        else:
            # Move towards first diamond on board
            self.goal_position = self.find_closest_diamond(board, board_bot["position"], props['diamonds'] == 4) 
        

        if self.goal_position:
            # Calculate move according to goal position
            delta_x, delta_y = get_direction(board_bot["position"], self.goal_position)

            # if (delta_x, delta_y) == (0, 0) and props["diamonds"] != 5: 
                # return random_move()

            return self.avoid_home_and_players(delta_x, delta_y, board_bot["position"], props["base"], board.gameObjects)
            # return delta_x, delta_y

        return 0, 0
