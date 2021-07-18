from typing import Tuple, List 
from utils import flatten
BoardList = List[List[int]]
Position = Tuple[int]


class Board: 
    def __init__(self, board: BoardList, player: int):
        self.size = len(board)
        self.board = board
        self.player = player

    def isEnd(self):
        flatBoard = flatten(self.board)
        NUM_OF_PIECE = self.size*4 - 4
        numOfPeice = flatBoard.count(1)
        if (numOfPeice == NUM_OF_PIECE): return 1
        numOfPeice = flatBoard.count(-1)
        if (numOfPeice == NUM_OF_PIECE): return -1
        return 0

    def move(self, fromPosition: Position, toPosition: Position):
        piece = self.getPiece(fromPosition)
        if (piece != self.player): raise RuntimeError('Piece at from position is not match with current player')

        sucessors = self.getSuccessorsAt(fromPosition)
        if (sucessors.index(toPosition) == -1): raise RuntimeError('Wrong move position')

        newBoard = self._getNewBoard(fromPosition, toPosition)
        return newBoard

    def getSuccessorsAt(self, position: Position):
        piece = self.getPiece(position)
        if piece != self.player: return []

        nearPosition = self._getNearbyPosition(position)
        result = []
        for pos in nearPosition: 
            piece = self.getPiece(pos)
            if piece == 0:
                result.append(pos)

        return result
    
    def getPiece(self, position):
        x, y = position
        if (x < 0 or y < 0 or x >= self.size or y >= self.size): return 0
        return self.board[x][y]

    # Gánh 
    def getCarried(self, position: Position):
        piece = self.getPiece(position)
        if (piece == 0): return []
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

        return result

    # Vây
    def getEmbraced(self, position: Position):
        x, y = position
        piece = self.getPiece(position)
        result = []
        if (self.getPiece((x-1, y)) == piece * -1 and \
            self.getPiece((x-2, y)) == piece):
            result.append((x-1, y))
        if (self.getPiece((x+1, y)) == piece * -1 and \
            self.getPiece((x+2, y)) == piece):
            result.append((x+1, y))
        if (self.getPiece((x, y-1)) == piece * -1 and \
            self.getPiece((x, y-2)) == piece):
            result.append((x, y-1))
        if (self.getPiece((x, y+1)) == piece * -1 and \
            self.getPiece((x, y+2)) == piece):
            result.append((x, y+1))

        if ((x+y)%2 == 0): 
            if (self.getPiece((x-1, y-1)) == piece * -1 and \
                self.getPiece((x-2, y-2)) == piece):
                result.append((x-1, y-1))
            if (self.getPiece((x+1, y+1)) == piece * -1 and \
                self.getPiece((x+2, y+2)) == piece):
                result.append((x+1, y+1))
            
            if (self.getPiece((x+1, y-1)) == piece * 1 and \
                self.getPiece((x+2, y-2)) == piece):
                result.append((x+1, y-1))
            if (self.getPiece((x-1, y+1)) == piece * 1 and \
                self.getPiece((x-2, y+2)) == piece):
                result.append((x-1, y+1))
        
        return result

    def _getNewBoard(self, fromPosition: Position, toPosition: Position):
        newBoardList = [x[:] for x in self.board]
        newBoard = Board(newBoardList, self.player * -1)
        newBoard._updateBoard(toPosition, self.player)
        newBoard._updateBoard(fromPosition, 0)
        carriedPosition = newBoard.getCarried(toPosition)
        embracedPosition = newBoard.getEmbraced(toPosition)
        
        list(map(lambda pos: newBoard._updateBoard(pos, self.player), flatten(carriedPosition) + embracedPosition))
        return newBoard

    def _updateBoard(self, position: Position, value: int):
        self.board[position[0]][position[1]] = value
        return self

    def _getNearbyPosition(self, position: Position):
        x, y = position
        if ((x+y)%2 == 0):
            return self._getHorizontalVerticalPosition(position) + self._getDiagonalPosition(position)
        else:
            return self._getHorizontalVerticalPosition(position)

    def _getHorizontalVerticalPosition(self, position: Position):
        result =    self._getHorizontalPosition(position) + \
                    self._getVerticalPosition(position)
        return result
    
    def _getDiagonalPosition(self, position: Position):
        result =    self._getDiagonal1Position(position) + \
                    self._getDiagonal2Position(position)
        return result

    def _getHorizontalPosition(self, position: Position):
        x, y = position
        maxSize = self.size - 1
        result = []
        if (x > 0 ): result.append((x-1, y))
        if (x < maxSize): result.append((x+1, y))

        return result

    def _getVerticalPosition(self, position: Position):
        x, y = position
        maxSize = self.size - 1
        result = []

        if (y > 0): result.append((x, y-1))
        if (y < maxSize): result.append((x, y+1))

        return result

    def _getDiagonal1Position(self, position: Position):
        x, y = position
        maxSize = self.size - 1
        if ((x+y)%2 == 1): return []

        result = []
        if (x > 0 and y > 0): result.append((x-1, y-1))
        if (x < maxSize and y < maxSize): result.append((x+1, y+1))

        return result 

    def _getDiagonal2Position(self, position: Position):
        x, y = position
        maxSize = self.size - 1
        if ((x+y)%2 == 1): return []

        result = []
        if (x > 0 and y < maxSize): result.append((x-1, y+1))
        if (x < maxSize and y > 0): result.append((x+1, y-1))

        return result

        