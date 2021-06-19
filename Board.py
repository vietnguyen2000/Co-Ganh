class Board: 
    def __init__(self, board, player):
        self.size = len(board)
        self.board = board
        self.player = player

    def move(self, fromPosition, toPosition):
        piece = self.getPiece(fromPosition)
        if (piece != self.player): raise RuntimeError('Piece at from position is not match with current player')

        sucessors = self.getSuccessors(fromPosition)
        if (sucessors.index(toPosition) == -1): raise RuntimeError('Wrong move position')

        newBoard = self._updateBoard(fromPosition, toPosition)
        return Board(newBoard, self.player * -1)

    def getSuccessors(self, position):
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
        return self.board[position[0]][position[1]]

    def _updateBoard(self, fromPosition, toPosition):
        newBoard = [x[:] for x in self.board]
        newBoard[toPosition[0]][toPosition[1]] = newBoard[fromPosition[0]][toPosition[1]]
        newBoard[fromPosition[0]][toPosition[1]] = 0
        return newBoard

    def _getNearbyPosition(self, position):
        x = position[0]
        y = position[1]
        if ((x+y)%2 == 0):
            return self._getHorizontalVerticalPosition(position) + self._getDiagonalPosition(position)
        else:
            return self._getHorizontalVerticalPosition(position)

    def _getHorizontalVerticalPosition(self, position):
        result =    self._getHorizontalPosition(position) + \
                    self._getVerticalPosition(position)
        return result
    
    def _getDiagonalPosition(self, position):
        result =    self._getDiagonal1Position(position) + \
                    self._getDiagonal2Position(position)
        return result

    def _getHorizontalPosition(self, position):
        x = position[0]
        y = position[1]
        maxSize = self.size - 1
        result = []
        if (x > 0 ): result.append((x-1, y))
        if (x < maxSize): result.append((x+1, y))

        return result

    def _getVerticalPosition(self, position):
        x = position[0]
        y = position[1]
        maxSize = self.size - 1
        result = []

        if (y > 0): result.append((x, y-1))
        if (y < maxSize): result.append((x, y+1))

        return result

    def _getDiagonal1Position(self, position):
        x = position[0]
        y = position[1]
        maxSize = self.size - 1
        if ((x+y)%2 == 1): return []

        result = []
        if (x > 0 and y > 0): result.append((x-1, y-1))
        if (x < maxSize and y < maxSize): result.append((x+1, y+1))

        return result 

    def _getDiagonal2Position(self, position):
        x = position[0]
        y = position[1]
        maxSize = self.size - 1
        if ((x+y)%2 == 1): return []

        result = []
        if (x > 0 and y < maxSize): result.append((x-1, y+1))
        if (x < maxSize and y > 0): result.append((x+1, y-1))

        return result

        