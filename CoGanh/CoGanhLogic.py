from typing import Tuple, List
from utils import flatten
import numpy as np
BoardList = List[List[int]]
Position = Tuple[int]


class Board:
    def __init__(self, board: BoardList, player: int, moveCount = 0):
        self.size = len(board)
        self.board = board
        self.player = player
        self.isTrap = False
        self.moveCount = moveCount

    def __str__(self):
        if not self.isTrap:
            return str(self.player) + ''.join(str(r) for v in self.board for r in v)
            
        return str(self.player) + ''.join(str(r) for v in self.board for r in v) + str(self.isTrap)

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return np.array(self.board)[index]

    def astype(self, t):
        return np.array(self.board).astype(t)

    def isEnd(self):
        flatBoard = flatten(self.board)
        NUM_OF_PIECE = self.size*4 - 4
        numOfPeice = flatBoard.count(1)
        if (numOfPeice == NUM_OF_PIECE):
            return 1
        numOfPeice = flatBoard.count(-1)
        if (numOfPeice == NUM_OF_PIECE):
            return -1
        return 0

    def move(self, fromPosition: Position, toPosition: Position):
        piece = self.getPiece(fromPosition)
        if (piece != self.player):
            self.display()
            print(fromPosition, toPosition)
            raise RuntimeError(
                'Piece at from position is not match with current player')

        sucessors = self.getSuccessorsAt(fromPosition, self.player)
        if (sucessors.index(toPosition) == -1):
            raise RuntimeError('Wrong move position')

        newBoard, _ = self._getNewBoard(fromPosition, toPosition)
        return newBoard

    def getAllSuccessor(self):
        if (self.isTrap):
            return self.isTrap
        res = []
        for x in range(0, self.size):
            for y in range(0, self.size):
                if (self.board[x][y] == self.player):
                    successors = self.getSuccessorsAt((x, y), self.player)
                    for s in successors:
                        res.append((x, y, s[0], s[1]))
        return res

    def getCanonicalForm(self):
        if (self.player == 1):
            return self

        else:
            newBoardList = [x[:] for x in self.board]
            res = Board(newBoardList, self.player * -1, self.moveCount)
            for x in range(self.size):
                for y in range(self.size):
                    res.board[x][y] = -self.board[x][y]

            res.isTrap = self.isTrap
            # print('before')
            # self.display()
            # print('after')
            # res.display()
            return res

    def getSuccessorsAt(self, position: Position, player):
        piece = self.getPiece(position)
        if piece != player:
            return []

        nearPosition = self._getNearbyPosition(position)
        result = []
        for pos in nearPosition:
            piece = self.getPiece(pos)
            if piece == 0:
                result.append(pos)

        return result

    def getPiece(self, position):
        x, y = position
        if (x < 0 or y < 0 or x >= self.size or y >= self.size):
            return 0
        return self.board[x][y]

    def getCaptured(self, position: Position):
        carriedPosition = self.getCarried(position)
        embracedPosition = self.getEmbraced(position)
        return list(set(carriedPosition + embracedPosition))

    # Gánh
    def getCarried(self, position: Position):
        piece = self.getPiece(position)
        if (piece == 0):
            return []
        result = []

        def checkAndAddResult(lst):
            numOfAcceptPieces = list(map(self.getPiece, lst)).count(piece * -1)
            if (numOfAcceptPieces == 2):
                result.append(lst)
        horizontal = self._getHorizontalPosition(position)
        checkAndAddResult(horizontal)

        vertical = self._getVerticalPosition(position)
        checkAndAddResult(vertical)

        diagonal1 = self._getDiagonal1Position(position)
        checkAndAddResult(diagonal1)

        diagonal2 = self._getDiagonal2Position(position)
        checkAndAddResult(diagonal2)

        return flatten(result)

    # Vây
    def getEmbraced(self, position: Position):
        x, y = position
        piece = self.getPiece(position)
        result = []
        nearPosition = self._getNearbyPosition(position)
        for pos in nearPosition:
            if (self.getPiece(pos) == -piece):
                isCapture = True
                lst = []
                newlst = [pos]
                while (len(newlst) != 0):
                    lst += newlst
                    newnew = []
                    for p in newlst:
                        alln = self._getNearbyPosition(p)
                        for npos in alln:
                            pi = self.getPiece(npos)
                            if (pi == -piece and npos not in lst):
                                newnew.append(npos)
                    newlst = newnew

                for p in lst:
                    alln = self._getNearbyPosition(p)
                    for npos in alln:
                        pi = self.getPiece(npos)
                        if (pi == 0):
                            # ko bi chan
                            isCapture = False
                            break
                    if not isCapture:
                        break

                if (isCapture):
                    result += lst

        return list(set(result))

    def __getShallowNewBoard(self, fromPosition: Position, toPosition: Position):
        newBoardList = [x[:] for x in self.board]
        newBoard = Board(newBoardList, self.player * -1, self.moveCount + 1)
        newBoard._updateBoard(toPosition, self.player)
        newBoard._updateBoard(fromPosition, 0)
        capturePosition = newBoard.getCaptured(toPosition)
        return newBoard, capturePosition

    def _getNewBoard(self, fromPosition: Position, toPosition: Position):
        newBoard, capturePosition = self.__getShallowNewBoard(
            fromPosition, toPosition)

        if (len(capturePosition) > 0):
            newCapture = capturePosition
            while (len(newCapture) != 0):
                for pos in newCapture:
                    newBoard._updateBoard(pos, self.player)
                new = []
                for pos in newCapture:
                    new += newBoard.getEmbraced(pos)
                newCapture = new
                capturePosition += newCapture

            # list(map(lambda pos: newBoard._updateBoard(pos, self.player), capturePosition))
        else:
            newBoard.isTrap = newBoard._isTrap(fromPosition)

        return newBoard, capturePosition

    def _isTrap(self, position: Position):
        nearPosition = self._getNearbyPosition(position)
        pieceCanMove = []

        for pos in nearPosition:
            piece = self.getPiece(pos)
            if piece == self.player:
                pieceCanMove.append(pos)

        res = []
        for pos in pieceCanMove:
            newBoard, capturePosition = self.__getShallowNewBoard(
                pos, position)
            if (len(capturePosition) > 0):
                res.append((pos[0], pos[1], position[0], position[1]))

        if (len(res) > 0):
            return res
        else:
            return False

    def _updateBoard(self, position: Position, value: int):
        self.board[position[0]][position[1]] = value
        return self

    def _getNearbyPosition(self, position: Position):
        x, y = position
        if ((x+y) % 2 == 0):
            return self._getHorizontalVerticalPosition(position) + self._getDiagonalPosition(position)
        else:
            return self._getHorizontalVerticalPosition(position)

    def _getHorizontalVerticalPosition(self, position: Position):
        result = self._getHorizontalPosition(position) + \
            self._getVerticalPosition(position)
        return result

    def _getDiagonalPosition(self, position: Position):
        result = self._getDiagonal1Position(position) + \
            self._getDiagonal2Position(position)
        return result

    def _getHorizontalPosition(self, position: Position):
        x, y = position
        maxSize = self.size - 1
        result = []
        if (x > 0):
            result.append((x-1, y))
        if (x < maxSize):
            result.append((x+1, y))

        return result

    def _getVerticalPosition(self, position: Position):
        x, y = position
        maxSize = self.size - 1
        result = []

        if (y > 0):
            result.append((x, y-1))
        if (y < maxSize):
            result.append((x, y+1))

        return result

    def _getDiagonal1Position(self, position: Position):
        x, y = position
        maxSize = self.size - 1
        if ((x+y) % 2 == 1):
            return []

        result = []
        if (x > 0 and y > 0):
            result.append((x-1, y-1))
        if (x < maxSize and y < maxSize):
            result.append((x+1, y+1))

        return result

    def _getDiagonal2Position(self, position: Position):
        x, y = position
        maxSize = self.size - 1
        if ((x+y) % 2 == 1):
            return []

        result = []
        if (x > 0 and y < maxSize):
            result.append((x-1, y+1))
        if (x < maxSize and y > 0):
            result.append((x+1, y-1))

        return result

    def display(self):
        m = {
            "-1": "O",
            "0": "-",
            "1": "X",
        }
        print("---------------------")
        raw = self.board
        print('player', self.player, 'on turn:')
        for x in range(0, 5):
            for y in range(0, 5):
                print(m[str(raw[x][y])] + ' ', end='')
            
            print()
        print()
        print(self)
        print(self.getAllSuccessor())
        print("---------------------")
