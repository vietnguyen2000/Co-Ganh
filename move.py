from Board import Board
def move(board, player): 
    b = Board(board, player)
    print(b.move((0,1), (1,1)).board)


defaultBoard =  [[1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, -1],
                [-1, 0, 0, 0, -1],
                [-1, -1, -1, -1, -1]]

move(defaultBoard, 1)