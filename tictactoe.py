import copy

# Function to determine whose turn it is
def player(s):
    cross = 0
    letter = 0
    for i in range(3):
        for j in range(3):
            if s[i][j] == 'X':
                cross += 1
            elif s[i][j] == 'O':
                letter += 1
    return 'X' if cross == letter else 'O'

# Function to get all possible actions (empty cells)
def actions(s):
    empty = []
    for i in range(3):
        for j in range(3):
            if s[i][j] == 0:
                empty.append((i, j))
    return empty

# Function to apply an action to the state and return a new state
def result(s, a):
    new_state = copy.deepcopy(s)
    i, j = a
    new_state[i][j] = player(s)
    return new_state

# Function to check if the game is over
def terminal(s):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if s[i][0] == s[i][1] == s[i][2] != 0:  # Row
            return True
        if s[0][i] == s[1][i] == s[2][i] != 0:  # Column
            return True
    if s[0][0] == s[1][1] == s[2][2] != 0:  # Diagonal
        return True
    if s[0][2] == s[1][1] == s[2][0] != 0:  # Anti-diagonal
        return True
    # Check if the board is full (draw)
    if not any(0 in row for row in s):
        return True
    return False

# Function to evaluate the utility of a terminal state
def utility(s):
    # Check rows, columns, and diagonals for a win by X or O
    for i in range(3):
        if s[i][0] == s[i][1] == s[i][2]:  # Row
            if s[i][0] == 'X':
                return 1
            elif s[i][0] == 'O':
                return -1
        if s[0][i] == s[1][i] == s[2][i]:  # Column
            if s[0][i] == 'X':
                return 1
            elif s[0][i] == 'O':
                return -1
    if s[0][0] == s[1][1] == s[2][2]:  # Diagonal
        if s[0][0] == 'X':
            return 1
        elif s[0][0] == 'O':
            return -1
    if s[0][2] == s[1][1] == s[2][0]:  # Anti-diagonal
        if s[0][2] == 'X':
            return 1
        elif s[0][2] == 'O':
            return -1
    return 0  # Draw

# Minimax algorithm with Alpha-Beta Pruning
def max_value(s, alpha, beta):
    if terminal(s):
        return utility(s), None
    v = -float('inf')
    best_action = None
    for action in actions(s):
        new_v, _ = min_value(result(s, action), alpha, beta)
        if new_v > v:
            v = new_v
            best_action = action
        if v >= beta:
            return v, best_action  # Beta cutoff
        alpha = max(alpha, v)
    return v, best_action

def min_value(s, alpha, beta):
    if terminal(s):
        return utility(s), None
    v = float('inf')
    best_action = None
    for action in actions(s):
        new_v, _ = max_value(result(s, action), alpha, beta)
        if new_v < v:
            v = new_v
            best_action = action
        if v <= alpha:
            return v, best_action  # Alpha cutoff
        beta = min(beta, v)
    return v, best_action

def alphabeta(s):
    current_player = player(s)
    if current_player == 'X':
        _, best_action = max_value(s, -float('inf'), float('inf'))
    else:
        _, best_action = min_value(s, -float('inf'), float('inf'))
    return best_action

# Display the board
def display_board(s):
    print("\nCurrent Board:")
    for row in s:
        print(" | ".join([str(cell) if cell != 0 else " " for cell in row]))
        print("-" * 9)

# Play the game interactively
def play_game():
    # Initialize the board
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    print("Welcome to Tic-Tac-Toe!")
    print("You are 'X', and the AI is 'O'.")
    while not terminal(board):
        display_board(board)
        if player(board) == 'X':  # Human's turn
            print("Your turn (enter row and column as 'row col'):")
            try:
                row, col = map(int, input().split())
                if board[row][col] == 0:
                    board[row][col] = 'X'
                else:
                    print("Cell already occupied. Try again.")
                    continue
            except (ValueError, IndexError):
                print("Invalid input. Please enter row and column as 'row col'.")
                continue
        else:  # AI's turn
            print("AI's turn...")
            action = alphabeta(board)
            board[action[0]][action[1]] = 'O'
    
    # Game over
    display_board(board)
    score = utility(board)
    if score == 1:
        print("You win!")
    elif score == -1:
        print("AI wins!")
    else:
        print("It's a draw!")

# Start the game
# if __name__ == "__main__":
    
play_game()