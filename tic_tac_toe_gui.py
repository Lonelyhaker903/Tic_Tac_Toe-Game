import tkinter as tk
from tkinter import messagebox
import random

# Global variables
current_player = "X"
game_mode = None
board = [[None for _ in range(3)] for _ in range(3)]

# Function to handle player and AI moves
def on_click(row, col):
    global current_player

    # If the cell is already filled, do nothing
    if board[row][col]["text"] != "":
        return

    # Update the button with the current player's symbol
    board[row][col]["text"] = current_player
    board[row][col]["fg"] = "blue" if current_player == "X" else "red"

    # Check for a winner
    if check_winner(current_player):
        messagebox.showinfo("Game Over", f"Player {current_player} wins!")
        reset_board()
        return

    # Check for a draw
    if is_draw():
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_board()
        return

    # Switch players
    current_player = "O" if current_player == "X" else "X"
    status_label.config(text=f"Player {current_player}'s Turn")

    # If AI's turn, make a move
    if game_mode == "ai" and current_player == "O":
        root.after(500, ai_move)  # Delay AI move slightly for better UX

# Function for AI to make a random move
def ai_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j]["text"] == ""]
    if empty_cells:
        row, col = random.choice(empty_cells)
        on_click(row, col)

# Function to check for a winner
def check_winner(player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j]["text"] == player for j in range(3)):
            return True
        if all(board[j][i]["text"] == player for j in range(3)):
            return True

    if all(board[i][i]["text"] == player for i in range(3)):
        return True
    if all(board[i][2-i]["text"] == player for i in range(3)):
        return True

    return False

# Function to check for a draw
def is_draw():
    return all(board[i][j]["text"] != "" for i in range(3) for j in range(3))

# Function to reset the board
def reset_board():
    global current_player
    for i in range(3):
        for j in range(3):
            board[i][j]["text"] = ""
    current_player = "X"
    status_label.config(text=f"Player {current_player}'s Turn")

# Function to set the game mode
def set_game_mode(mode):
    global game_mode
    game_mode = mode
    mode_frame.pack_forget()
    game_frame.pack()
    status_label.config(text=f"Player {current_player}'s Turn")

# Initialize the main window
root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg="#f0f0f0")

# Game mode selection frame
mode_frame = tk.Frame(root, bg="#f0f0f0")
mode_frame.pack(pady=20)

tk.Label(mode_frame, text="Choose Game Mode", font=("Helvetica", 18, "bold"), bg="#f0f0f0").pack(pady=10)
tk.Button(mode_frame, text="Play Against Player", font=("Helvetica", 16), command=lambda: set_game_mode("player")).pack(pady=5)
tk.Button(mode_frame, text="Play Against AI", font=("Helvetica", 16), command=lambda: set_game_mode("ai")).pack(pady=5)

# Game frame (hidden until mode is selected)
game_frame = tk.Frame(root, bg="#f0f0f0")

# Create a 3x3 board of buttons
button_font = ("Helvetica", 24, "bold")
button_color = "#ffffff"
button_bg = "#444444"

for i in range(3):
    for j in range(3):
        button = tk.Button(game_frame, text="", font=button_font, width=5, height=2,
                           bg=button_bg, fg=button_color,
                           command=lambda row=i, col=j: on_click(row, col))
        button.grid(row=i, column=j, padx=5, pady=5)
        board[i][j] = button

# Status label to indicate turns
status_label = tk.Label(game_frame, text=f"Player {current_player}'s Turn", font=("Helvetica", 18), bg="#f0f0f0")
status_label.grid(row=3, column=0, columnspan=3, pady=10)

# Reset button
reset_button = tk.Button(game_frame, text="Reset Game", font=("Helvetica", 16), command=reset_board, bg="#ff6347", fg="#ffffff")
reset_button.grid(row=4, column=0, columnspan=3, pady=10)

# Start the Tkinter event loop
root.mainloop()
