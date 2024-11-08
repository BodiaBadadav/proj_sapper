import tkinter as tk
from tkinter import messagebox

class MinesweeperGUI:
    def __init__(self, root, game_board):
        self.root = root
        self.game_board = game_board
        self.buttons = [[None for _ in range(self.game_board.cols)] for _ in range(self.game_board.rows)]
        self.remaining_flags_label = tk.Label(self.root, text=f"Осталось флажков: {self.game_board.remaining_flags}")
        self.remaining_flags_label.grid(row=self.game_board.rows, column=0, columnspan=self.game_board.cols)
        self.create_widgets()


    def create_widgets(self):
        """Создаёт сетку кнопок для игрового поля."""
        for row in range(self.game_board.rows):
            for col in range(self.game_board.cols):
                button = tk.Button(
                    self.root,
                    width=4,
                    height=2
                )
                button.grid(row=row, column=col)
                button.bind("<Button-1>", lambda e, r=row, c=col: self.on_cell_click(r, c))
                button.bind("<Button-3>", lambda e, r=row, c=col: self.on_right_click(r, c))
                self.buttons[row][col] = button

    def show_mine(self, row, col):
        """Отображает мину в указанной клетке."""
        button = self.buttons[row][col]
        button.config(text="*", bg="red")

    def reset_game(self):
        """Сбрасывает интерфейс игры."""
        for row in range(self.game_board.rows):
            for col in range(self.game_board.cols):
                button = self.buttons[row][col]
                button.config(text="", bg="SystemButtonFace", state="normal")
        self.game_board.reset_board()
        self.flags_count_label.config(
            text=f"Осталось флажков: {self.game_board.flags_count}")  # Обновляем счётчик флажков
        self.create_widgets()  # Пересоздаём интерфейс

    def on_right_click(self, row, col):
        """Обрабатывает правый клик для установки флажка."""
        self.game_board.toggle_flag(row, col)
        button = self.buttons[row][col]

        if self.game_board.flags[row][col]:
            button.config(text="F", fg="orange")
        else:
            button.config(text="")

        self.remaining_flags_label.config(text=f"Осталось флажков: {self.game_board.remaining_flags}")

    def on_cell_click(self, row, col):
        """Обрабатывает нажатие на клетку."""
        if self.game_board.board[row][col] == -1:
            # Если нажали на мину — показываем её и завершаем игру
            self.show_mine(row, col)
            messagebox.showinfo("Game Over", "Вы проиграли!")
            self.reset_game()
        else:
            # Иначе, показываем количество мин вокруг клетки
            mines_count = self.game_board.board[row][col]
            button = self.buttons[row][col]
            color_map = {
                1: "blue",
                2: "green",
                3: "red",
                4: "darkblue",
                5: "darkred",
                6: "cyan",
                7: "black",
                8: "gray"
            }
            text_color = color_map.get(mines_count, "black")  # Цвет по умолчанию - черный
            button.config(
                text=str(mines_count) if mines_count > 0 else "",
                state="disabled",
                disabledforeground=text_color,
                bg="lightgrey"  # Цвет открытой клетки
            )

            if mines_count == 0:
                # Если рядом нет мин, открываем соседние клетки рекурсивно
                self.game_board.reveal_empty_cells(row, col, self.on_cell_click)

            # Проверка победы после каждого нажатия
            if self.game_board.is_winner():
                messagebox.showinfo("Победа!", "Поздравляем, вы выиграли!")
                self.reset_game()
