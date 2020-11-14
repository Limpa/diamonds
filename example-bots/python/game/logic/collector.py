from ..util import get_direction


class CollectorLogic(object):
    def __init__(self):
        self.instructions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        self.base_pos = -1
        self.reset_values()

    def reset_values(self):
        self.current_instruction = -1 
        self.error = False 
    
    def return_to_base(self, board_bot, board):
        if self.base_pos == -1:
            self.base_pos = board_bot["properties"]["base"]
        delta_x, delta_y = get_direction(board_bot["position"]["x"], board_bot["position"]["y"], self.base_pos["x"], self.base_pos["y"])
        if delta_x != 0 and delta_y != 0:
            return delta_x, delta_y
        self.reset_values()
        return self.next_move(board_bot, board)



    def next_move(self, board_bot, board):
        self.current_instruction = (self.current_instruction + 1) % len(self.instructions)
        if self.current_instruction % 2 == 0 and board_bot["position"] != self.base_pos:
            self.error = True
        if self.error:
            return self.return_to_base(board_bot, board)
        return self.instructions[self.current_instruction]
