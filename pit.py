import Arena
from MCTS import MCTS
from CoGanh.CoGanhGame import CoGanhGame as Game
from CoGanh.CoGanhPlayers import *
from CoGanh.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *


def display(board):
    m = {
        "-1": "O",
        "0": "-",
        "1": "X",
    }
    print("---------------------")
    raw = board.board
    print('player', board.player, 'on turn:')
    for x in range(0, 5):
        for y in range(0, 5):
            print(m[str(raw[x][y])] + ' ', end='')

        print()
    print()
    print("---------------------")

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""
human_vs_cpu = False

g = Game()

# all players
rp = RandomPlayer(g).play


# nnet players
n1 = NNet(g)
n1.load_checkpoint('./temp','temp.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

if human_vs_cpu:
    player2 = hp
else:
    player2 = rp
    # n2 = NNet(g)
    # n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
    # args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
    # mcts2 = MCTS(g, n2, args2)
    # n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

    # player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(n1p, player2, g, display)

print(arena.playGames(20, verbose=False))
