import random

class GameBoard:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visible = [[False for _ in range(cols)] for _ in range(rows)]
        self.place_mines()
        self.calculate_numbers()

    def reset_board(self):
        """Сбрасывает игровое поле для новой игры."""
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.visible = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        """Размещаем мины на поле случайным образом."""
        placed_mines = 0
        while placed_mines < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] == 0:  # Проверяем, что здесь ещё нет мины
                self.board[row][col] = -1  # -1 обозначает мину
                placed_mines += 1

    def calculate_numbers(self):
        """Вычисляем числа для клеток в зависимости от соседних мин."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    continue

                mines_count = 0
                for r in range(row - 1, row + 2):
                    for c in range(col - 1, col + 2):
                        if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == -1:
                            mines_count += 1
                self.board[row][col] = mines_count

    def is_mine(self, row, col):
        """Проверяем, является ли клетка миной."""
        return self.board[row][col] == -1

    def open_cell(self, row, col):
        """Открываем клетку и все соседние пустые клетки, если они есть."""
        if not (0 <= row < self.rows and 0 <= col < self.cols):  # Проверка границ
            return
        if self.visible[row][col]:  # Если клетка уже открыта, выходим
            return

        self.visible[row][col] = True  # Отмечаем клетку как открытую

        # Если клетка с миной, конец игры
        if self.board[row][col] == -1:
            return "game_over"

        if self.board[row][col] == 0:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        self.open_cell(r, c)

    def is_winner(self):
        """Проверяем, открыты ли все клетки без мин."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != -1 and not self.visible[row][col]:
                    return False
        return True

    def reveal_empty_cells(self, row, col, on_cell_click):
        """Рекурсивно открывает пустые клетки вокруг нажатой клетки."""
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if 0 <= r < self.rows and 0 <= c < self.cols and not self.visible[r][c]:
                    self.visible[r][c] = True
                    mines_count = self.board[r][c]

                    # Открываем клетку через callback `on_cell_click`
                    on_cell_click(r, c)

                    # Если рядом нет мин, продолжаем рекурсивное открытие
                    if mines_count == 0:
                        self.reveal_empty_cells(r, c, on_cell_click)
