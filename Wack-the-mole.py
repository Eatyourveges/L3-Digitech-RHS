# Imports all functions from that library
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer
import random 

# This class is to define the entire process of the game
class WhackAMoleGame(QWidget):
    def __init__(self):
        super().__init__()

        # Game settings
        self.num_holes = 25
        self.mole_hole = None
        self.score = 0
        self.game_running = True

        self.setWindowTitle('Wack-The-Mole')

        # Layouts
        self.main_layout = QVBoxLayout()
        self.grid_layout = QHBoxLayout()

        # Score display
        self.score_label = QLabel(f'Score: {self.score}')
        self.main_layout.addWidget(self.score_label)

        # Buttons for holes
        self.buttons = [QPushButton('') for _ in range(self.num_holes)]
        self.buttons_layout = QVBoxLayout()
        
        for i in range(5):
            row_layout = QHBoxLayout()
            for j in range(5):
                button = self.buttons[i*5 + j]
                button.setFixedSize(100, 100)
                button.clicked.connect(self.on_button_click)
                row_layout.addWidget(button)
            self.buttons_layout.addLayout(row_layout)

        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

        # Start the game
        self.timer_limit = QTimer()
        self.timer_limit, ok = QInputDialog.getInt(self, 'Wack-the-Moe Timer', f'Enter the game time in seconds between 30sec to 60sec:', min=30, max=60)
        
        self.show_mole_timer = QTimer()
        self.show_mole_timer.timeout.connect(self.show_mole)
        self.show_mole_timer.start(1000)
        
    def show_mole(self):
        if self.mole_hole is not None:
            self.buttons[self.mole_hole].setText('ʕ•ᴥ•ʔ')
        
        self.mole_hole = random.randint(0, self.num_holes - 1)
        self.buttons[self.mole_hole].setText('ʕ•ᴥ•ʔ')

    def on_button_click(self):
        button = self.sender()
        if button.text() == 'ʕ•ᴥ•ʔ':
            self.score += 1
            self.score_label.setText(f'Score: {self.score}')
            button.setText('')
            self.mole_hole = None

    def end_game(self):
        self.timer_limit.stop()
        QMessageBox.information(self, 'Game Over', f'Game over! Final score: {self.score}')
        print ('Game Over!')
        self.close()
        file = open('file.txt', 'w')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WhackAMoleGame()
    game.show()
    sys.exit(app.exec_())
