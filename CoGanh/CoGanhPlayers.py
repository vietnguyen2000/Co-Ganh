import numpy as np

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):

        valids = self.game.getValidMoves(board, 1)
        temp = list(filter(lambda v: v[1] == 1, enumerate(valids)))
        index = np.random.randint(len(temp))
        a = temp[index][0]
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a