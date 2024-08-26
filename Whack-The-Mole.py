# Whack The Mole 
# Imports all functions from that library
import sys
import random
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer

# This class is to define the entire process of the game
class WhackAMoleGame(QWidget):
    def __init__(self):
        super().__init__()

        # Game settings
        self.num_holes = 25
        self.mole_hole = None
        self.score = 0
        self.timer_left = 0
        self.game_running = True
        
        self.setWindowTitle('Whack-The-Mole')

        # Layouts
        self.main_layout = QVBoxLayout()
        self.grid_layout = QHBoxLayout()
    
        # Score and Time display  
        self.timer_left = self.timer_limit
        self.score_label = QLabel(f'Score: {self.score}')
        self.timer_label = QLabel(f"Time Left: {self.timer_left} seconds",self)
        
        self.main_layout.addWidget(self.score_label)
        self.main_layout.addWidget(self.timer_label)

        # Buttons for holes
        self.buttons = [QPushButton('') for _ in range(self.num_holes)]
        self.buttons_layout = QVBoxLayout()
        
        # Creates the grid layout
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

        # Timer for the player
        self.timer_limit = QTimer()
        self.timer_limit.timeout.connect(self.timer_limit)
        self.timer_limit, ok = QInputDialog.getInt(self, 'Whack-the-Mole Timer', f'Enter the game time in seconds between 15 sec to 60 sec:', min=15, max=60)
        QTimer.singleShot(self.timer_limit * 1000, self.end_game)
        
        # Timer for the moles to spawn
        self.show_mole_timer = QTimer()
        self.show_mole_timer.timeout.connect(self.show_mole)
        self.show_mole_timer.start(1000)

    # Defines what the mole looks like 
    def show_mole(self):
        if self.mole_hole is not None:
            self.buttons[self.mole_hole].setText('')
        
        # Creates what hole the mole is located 
        self.mole_hole = random.randint(0, self.num_holes - 1)
        self.buttons[self.mole_hole].setText('ʕ•ᴥ•ʔ')

    # Defines what happens when the mole is cilcked 
    def on_button_click(self):
        button = self.sender()
        if button.text() == 'ʕ•ᴥ•ʔ':
            self.score += 1
            self.score_label.setText(f'Score: {self.score}')
            button.setText('')
            self.mole_hole = random.randint(0, self.num_holes - 1)
            self.buttons[self.mole_hole].setText('')
            self.mole_hole = None

    def update_timer(self):
        self.timer_left -= 1 
        self.timer_label.setText(f'Time Left: {self.timer_left} sec')
        if self.timer_left == 0:
            self.end_game

    # Defines what happens when the timer is over
    def end_game(self):
        QMessageBox.information(self, 'Game Over', f'Game over! Final score: {self.score}')
        print ('Game Over!')
        self.close()
        file = open('Whack The Mole Score', 'w')
        file.write(f'You scored: {self.score}')
        file.close()

# Closes the game
if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WhackAMoleGame()
    game.show()
    sys.exit(app.exec_())