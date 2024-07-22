import tkinter as tk
import random

class Square:
    def __init__(self, row, col, frame, game):
        self.row = row
        self.col = col
        self.mark = None
        self.button = tk.Button(frame, text="", width=10, height=5, bg='#f0f0f0', command=lambda: self.mark_square(game))
        self.button.grid(row=row, column=col)

    def mark_square(self, game):
        if not self.mark and game.current_player == "X":
            self.button.configure(text=game.current_player, bg='#feb9b9', fg='black')
            self.mark = game.current_player
            game.evaluate_game()
            if not game.game_over:
                game.current_player = "O"
                game.status_label.configure(text="O's turn", bg='#ffeb99')
                game.window.after(500, game.computer_move)

    def reset(self):
        self.button.configure(text="", bg='#f0f0f0', state='normal')
        self.mark = None

class TicTacToeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.resizable(False, False)

        self.frame = tk.Frame(self.window, width=300, height=300, bg='#ffffff')
        self.frame.pack(pady=10, padx=10)

        self.grid = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(Square(i, j, self.frame, self))
            self.grid.append(row)

        self.status_label = tk.Label(self.window, text="X's turn", font=('Arial', 15), bg='#99ff99', fg='black')
        self.status_label.pack()

        self.restart_button = tk.Button(self.window, text="Restart", font=('Arial', 12), bg='#ffcccc', fg='black', command=self.restart_game)
        self.restart_button.pack(pady=10)
        self.restart_button.pack_forget()  # Hide the restart button initially

        self.current_player = "X"
        self.game_over = False

        self.window.mainloop()

    def evaluate_game(self):
        winner = None
        for row in self.grid:
            if row[0].mark == row[1].mark == row[2].mark and row[0].mark is not None:
                winner = row[0].mark
        for col in range(3):
            if self.grid[0][col].mark == self.grid[1][col].mark == self.grid[2][col].mark and self.grid[0][col].mark is not None:
                winner = self.grid[0][col].mark
        if self.grid[0][0].mark == self.grid[1][1].mark == self.grid[2][2].mark and self.grid[0][0].mark is not None:
            winner = self.grid[0][0].mark
        if self.grid[0][2].mark == self.grid[1][1].mark == self.grid[2][0].mark and self.grid[0][2].mark is not None:
            winner = self.grid[0][2].mark
        if winner:
            self.status_label.configure(text=f"{winner} won!", bg='#ccffcc')
            self.disable_board()
            self.game_over = True
            self.restart_button.pack()  # Show the restart button
        elif all(square.mark is not None for row in self.grid for square in row):
            self.status_label.configure(text="Draw!", bg='#ccccff')
            self.disable_board()
            self.game_over = True
            self.restart_button.pack()  # Show the restart button

    def disable_board(self):
        for row in self.grid:
            for square in row:
                square.button.configure(state='disabled')

    def restart_game(self):
        for row in self.grid:
            for square in row:
                square.reset()
        self.current_player = "X"
        self.game_over = False
        self.status_label.configure(text="X's turn", bg='#99ff99')
        self.restart_button.pack_forget()  # Hide the restart button

    def computer_move(self):
        if self.current_player == "O" and not self.game_over:
            best_score = -float('inf')
            best_move = None
            for i in range(3):
                for j in range(3):
                    if self.grid[i][j].mark is None:
                        self.grid[i][j].mark = "O"
                        score = self.minimax(0, False, -float('inf'), float('inf'))
                        self.grid[i][j].mark = None
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
            if best_move:
                self.grid[best_move[0]][best_move[1]].button.configure(text="O", bg='#cceeff', fg='black')
                self.grid[best_move[0]][best_move[1]].mark = "O"
                self.current_player = "X"
                self.status_label.configure(text="X's turn", bg='#ffeb99')
                self.evaluate_game()

    def minimax(self, depth, is_maximizing, alpha, beta):
        result = self.check_winner()
        if result is not None:
            return result

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if self.grid[i][j].mark is None:
                        self.grid[i][j].mark = "O"
                        score = self.minimax(depth + 1, False, alpha, beta)
                        self.grid[i][j].mark = None
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.grid[i][j].mark is None:
                        self.grid[i][j].mark = "X"
                        score = self.minimax(depth + 1, True, alpha, beta)
                        self.grid[i][j].mark = None
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score

    def check_winner(self):
        for row in self.grid:
            if row[0].mark == row[1].mark == row[2].mark:
                if row[0].mark == "O":
                    return 1
                elif row[0].mark == "X":
                    return -1
        for col in range(3):
            if self.grid[0][col].mark == self.grid[1][col].mark == self.grid[2][col].mark:
                if self.grid[0][col].mark == "O":
                    return 1
                elif self.grid[0][col].mark == "X":
                    return -1
        if self.grid[0][0].mark == self.grid[1][1].mark == self.grid[2][2].mark:
            if self.grid[0][0].mark == "O":
                return 1
            elif self.grid[0][0].mark == "X":
                return -1
        if self.grid[0][2].mark == self.grid[1][1].mark == self.grid[2][0].mark:
            if self.grid[0][2].mark == "O":
                return 1
            elif self.grid[0][2].mark == "X":
                return -1
        if all(square.mark is not None for row in self.grid for square in row):
            return 0
        return None

TicTacToeGame()
