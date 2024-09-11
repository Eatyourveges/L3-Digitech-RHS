# Whack The Mole 
# Imports all functions from that library
import sys
import random
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtCore import QTimer

# This class is to define the entire process of the game
class WhackAMoleGame(QWidget):
    def __init__(self):
        super().__init__()

        # Game settings
        self.num_holes = 25
        self.mole_hole = None
        self.score = 0
        self.time_left = 0
        self.game_running = True

        self.setWindowTitle('Whack-The-Mole')

        # Layouts
        self.main_layout = QVBoxLayout()
        self.grid_layout = QHBoxLayout()
    
        # Timer input
        self.timer_limit, ok = QInputDialog.getInt(self, 'Whack-the-Mole Timer', 'Enter the game time in seconds between 15 sec to 60 sec:', min=15, max=60)

        # Mole speed input
        self.mole_speed, ok = QInputDialog.getInt(self, 'Mole Speed', 'Enter mole speed in seconds (500(Hard) - 1000(Normal)):', min=500, max=1000)
        
        # Timer and score display
        self.time_left = self.timer_limit
        self.timer_label = QLabel(f'Time Left: {self.time_left} sec')
        self.score_label = QLabel(f'Score: {self.score}')
        self.main_layout.addWidget(self.score_label)
        self.main_layout.addWidget(self.timer_label)

        # Buttons for holes
        self.buttons = [QPushButton('') for _ in range(self.num_holes)]
        self.buttons_layout = QVBoxLayout()
        
        # Creates the grid
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

        # Timer for the countdown
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self.update_timer)
        self.countdown_timer.start(1000)  # Update every second

        # Timer for the moles to spawn
        self.show_mole_timer = QTimer()
        self.show_mole_timer.timeout.connect(self.show_mole)
        self.show_mole_timer.start(self.mole_speed)  # Start with user-defined mole speed

    # Updates the countdown timer display
    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f'Time Left: {self.time_left} sec')
        if self.time_left == 0:
            self.end_game()

    # Defines what the mole looks like 
    def show_mole(self):
        if self.mole_hole is not None:
            self.buttons[self.mole_hole].setText('')
        
        # Creates what hole the mole is located 
        self.mole_hole = random.randint(0, self.num_holes - 1)
        self.buttons[self.mole_hole].setText('ʕ•ᴥ•ʔ')

    # Defines what happens when the mole is clicked 
    def on_button_click(self):
        button = self.sender()
        if button.text() == 'ʕ•ᴥ•ʔ':
            self.score += 1
            self.score_label.setText(f'Score: {self.score}')
            button.setText('')
            self.mole_hole = None

    # Defines what happens when the timer is over
    def end_game(self):
        self.countdown_timer.stop()
        self.show_mole_timer.stop()
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