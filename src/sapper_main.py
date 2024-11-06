from tkinter import Tk
from Gameboard import GameBoard  # Импорт логики игры
from sapper_GUI import MinesweeperGUI  # Импорт интерфейса игры

class MinesweeperGame:
    def __init__(self, rows, cols, mines):
        self.root = Tk()
        self.root.title("Сапер")

        # Создаём объект логики и объект интерфейса, передавая board в GUI
        self.game_board = GameBoard(rows, cols, mines)
        self.gui = MinesweeperGUI(self.root, self.game_board)

    def start(self):
        """Запуск основного цикла Tkinter."""
        self.root.mainloop()

    # Запуск игры при выполнении файла minesweeper_game.py
if __name__ == "__main__":
    # Задаём параметры игры: количество строк, столбцов и мин
    game = MinesweeperGame(rows=10, cols=10, mines=10)
    game.start()
