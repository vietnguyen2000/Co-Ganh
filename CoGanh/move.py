from Board import Board
# defaultBoard =  [[1, 1, 1, 1, 1],
#                 [1, 0, 0, 0, 1],
#                 [1, 0, 0, 0, -1],
#                 [-1, 0, 0, 0, -1],
#                 [-1, -1, -1, -1, -1]]
# test
# defaultBoard =  [[0, 0, -1, 0, -1],
#                 [1, 1, 0, 0, -1],
#                 [1, 1, 1, 0, 0],
#                 [1, 0, 1, -1, -1],
#                 [1, -1, 1, 0, -1]]
defaultBoard =  [[1, 0, -1, 0, -1],
                [0, 1, 0, 0, -1],
                [-1, -1, 1, 0, 0],
                [1, 1, -1, -1, -1],
                [1, 0, 0, 1, 1]]
# defaultBoard =  [[0, 0, -1, 0, -1],
#                 [1, 1, 0, 0, -1],
#                 [1, 1, -1, 0, 0],
#                 [1, 1, -1, -1, -1],
#                 [1, -1, 0, 0, -1]]
# defaultBoard =  [[0, 1, -1, -1, -1],
#                 [1, 1, 1, 1, -1],
#                 [1, 0, -1, 0, -1],
#                 [1, 0, 0, 1, 1],
#                 [1, 0, 0, 0, 0]]
                
b = Board(defaultBoard, 1)

m = {
    "-1": 'X',
    "0": '-',
    "1": 'O'
}

def move(board, player): 
    b = b.move((0,1), (1,1))

def render(board: Board):
    raw = board.board
    for x in range(0, 5):
        for y in range(0, 5):
            
            print(m[str(raw[x][y])] + '\t', end='')

        print()
    print('is game complete? ', board.isEnd())
    print('current player: ', m[str(board.player)])
    print('All sucessors:')
    sucessors = board.getAllSuccessor()
    for s in sucessors:
        print(s)

render(b)
while(True):
    move = input()
    move = list(map(int, move.split()))
    x1 = move[0]
    y1 = move[1]
    x2 = move[2]
    y2 = move[3]
    print('Moving: (', x1, y1, ') to (', x2 ,y2,')')
    b = b.move((x1,y1), (x2, y2))
    render(b)

# move(defaultBoard, 1)
# render(b)