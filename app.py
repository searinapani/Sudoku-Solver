from flask import Flask, request, render_template
import copy

app = Flask(__name__)

# Function to check if the board is valid
def is_valid(board, num, pos):
    row, col = pos
    # Check row
    for i in range(9):
        if board[row][i] == num and i != col:
            return False
    
    # Check column
    for i in range(9):
        if board[i][col] == num and i != row:
            return False
    
    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    
    return True

# Function to solve the Sudoku puzzle using backtracking
def solve_sudoku(board):
    # Find an empty spot
    empty_spot = None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                empty_spot = (i, j)
                break
        if empty_spot:
            break
    
    if not empty_spot:
        return True
    
    row, col = empty_spot
    
    # Try placing numbers 1-9
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            
            if solve_sudoku(board):
                return True
            
            # Backtrack
            board[row][col] = 0
    
    return False

# Home route for displaying the Sudoku input form
@app.route('/')
def home():
    return render_template('index.html')

# Route for solving the Sudoku puzzle
@app.route('/solve', methods=['POST'])
def solve():
    # Get the puzzle data from the form
    puzzle = request.form.getlist('puzzle[]')
    
    # Convert the puzzle data to a 2D list
    board = []
    for i in range(9):
        row = []
        for j in range(9):
            num = int(puzzle[i * 9 + j])
            row.append(num)
        board.append(row)
    
    # Make a deep copy of the board to solve the puzzle
    board_copy = copy.deepcopy(board)
    
    # Solve the puzzle
    solved = solve_sudoku(board_copy)
    
    if solved:
        return render_template('solution.html', board=board_copy)
    else:
        return render_template('index.html', error="No solution found.")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
