from ..util import get_direction
from ..util import position_equals
from ..util import compute_distance


class CollectorLogic(object):
    def __init__(self):
        self.instructions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 0), (1, 0), (0, -1), (0, 1)]

    
    def return_to_base(self, self_pos, base_pos):
        return get_direction(self_pos["x"], self_pos["y"], base_pos["x"], base_pos["y"])

    def find_closest_player(self, self_pos, gameObjects):
        closest_pos = {}
        closest_dist = 10000
        for gameObj in gameObjects:
            if gameObj["type"] != 'BotGameObject' or gameObj["properties"]["name"] == "NallePuh":
                continue
            dist = compute_distance(gameObj["position"], self_pos)
            if dist < closest_dist:
                closest_dist = dist
                closest_pos = gameObj["position"]
        return closest_pos, closest_dist




    def next_move(self, board_bot, board):
        # if not at base, go back
        self_pos = board_bot["position"]
        base_pos = board_bot["properties"]["base"]
        if not position_equals(self_pos, base_pos):
            return self.return_to_base(self_pos, base_pos)

        closest_player, dist = self.find_closest_player(self_pos, board.gameObjects)
        if dist == 1:
            return get_direction(self_pos["x"], self_pos["y"], closest_player["x"], closest_player["y"])

        return 0, 0
