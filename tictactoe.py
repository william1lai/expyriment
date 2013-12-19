
def winner(board):
    if board[0] == board[1] and board[1] == board[2] and board[0] != "-":
        return board[0]
    if board[0] == board[3] and board[3] == board[6] and board[0] != "-":
        return board[0]
    if board[0] == board[4] and board[4] == board[8] and board[0] != "-":
        return board[0]
    if board[1] == board[4] and board[4] == board[7] and board[1] != "-":
        return board[1]
    if board[2] == board[4] and board[4] == board[6] and board[2] != "-":
        return board[2]
    if board[2] == board[5] and board[5] == board[8] and board[2] != "-":
        return board[2]
    if board[3] == board[4] and board[4] == board[5] and board[3] != "-":
        return board[3]
    if board[6] == board[7] and board[7] == board[8] and board[6] != "-":
       return board[6]

def printBoard(board):
    print board[0], board[1], board[2]
    print board[3], board[4], board[5]
    print board[6], board[7], board[8]

def flip(turn):
    if turn == "O":
        return "X"
    else:
        return "O"

board = [ "-", "-", "-", "-", "-", "-", "-", "-", "-" ]
turn = "O"
while not winner(board) and "-" in board:
    printBoard(board)
    print turn, "'s turn: "
    query = input()
    while board[query] != "-":
        print "Not a valid move"
        query = input()
    board[query] = turn
    turn = flip(turn)
    print ""

if winner(board):
    print winner(board), " has won!"
else:
    print "Tie!"
