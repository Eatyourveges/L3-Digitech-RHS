# Whack The Mole
# Imports all functions from that library
import sys
import random
import time
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtCore import QTimer

# This class defines the entire process of the game
class WhackAMoleGame(QWidget):
    def __init__(self):
        super().__init__()

        # Game settings
        self.num_holes = 25  # Total number of holes for the moles
        self.mole_hole = None  # Current hole where the mole appears
        self.score = 0  # Player's score
        self.time_left = 0  # Time left for the game
        self.game_running = True  # Indicates if the game is currently running

        self.setWindowTitle('Whack-The-Mole')  # Set the window title

        # Layouts
        self.main_layout = QVBoxLayout()  # Main vertical layout for score and timer
        self.grid_layout = QHBoxLayout()  # Horizontal layout for buttons
    
        # Timer input dialog to set game time
        self.timer_limit, ok = QInputDialog.getInt(self, 'Whack-the-Mole Timer', 'Enter the game time in seconds between 15 sec to 60 sec:', min=15, max=60)
        
        # Initialize timer and score display
        self.time_left = self.timer_limit
        self.timer_label = QLabel(f'Time Left: {self.time_left} sec')  # Timer display
        self.score_label = QLabel(f'Score: {self.score}')  # Score display
        self.main_layout.addWidget(self.score_label)  # Add score label to main layout
        self.main_layout.addWidget(self.timer_label)  # Add timer label to main layout

        # Create buttons for mole holes
        self.buttons = [QPushButton('') for _ in range(self.num_holes)]  # Create buttons for each hole
        self.buttons_layout = QVBoxLayout()  # Layout for button grid
        
        # Creates the grid layout for buttons
        for i in range(5):
            row_layout = QHBoxLayout()  # Horizontal layout for each row
            for j in range(5):
                button = self.buttons[i*5 + j]  # Get button for the current hole
                button.setFixedSize(100, 100)  # Set button size
                button.clicked.connect(self.on_button_click)  # Connect button click to handler
                row_layout.addWidget(button)  # Add button to row layout
            self.buttons_layout.addLayout(row_layout)  # Add row layout to button layout

        self.main_layout.addLayout(self.buttons_layout)  # Add button layout to main layout
        self.setLayout(self.main_layout)  # Set the main layout for the widget

        # Timer for the countdown
        self.countdown_timer = QTimer(self)  # Create a timer for countdown
        self.countdown_timer.timeout.connect(self.update_timer)  # Connect timer timeout to update function
        self.countdown_timer.start(1000)  # Start timer, updates every second

        # Timer for the moles to spawn
        self.show_mole_timer = QTimer()  # Create a timer for showing moles
        self.show_mole_timer.timeout.connect(self.show_mole)  # Connect timer timeout to show mole function
        self.show_mole_timer.start(1000)  # Start timer, moles appear every second

    # Updates the countdown timer display
    def update_timer(self):
        self.time_left -= 1  # Decrease time left by 1 second
        self.timer_label.setText(f'Time Left: {self.time_left} sec')  # Update timer display
        if self.time_left == 0:  # If time is up
            self.end_game()  # End the game

    # Defines what the mole looks like 
    def show_mole(self):
        if self.mole_hole is not None:  # If there is an active mole
            self.buttons[self.mole_hole].setText('')  # Clear the previous mole
        
        # Randomly choose a hole for the mole
        self.mole_hole = random.randint(0, self.num_holes - 1)
        self.buttons[self.mole_hole].setText('ʕ•ᴥ•ʔ')  # Show mole in the selected hole

    # Defines what happens when the mole is clicked 
    def on_button_click(self):
        button = self.sender()  # Get the button that was clicked
        if button.text() == 'ʕ•ᴥ•ʔ':  # If the clicked button has a mole
            self.score += 1  # Increase score
            self.score_label.setText(f'Score: {self.score}')  # Update score display
            button.setText('')  # Clear the button text (remove mole)
            self.mole_hole = None  # Reset mole hole

    # Defines what happens when the timer is over
    def end_game(self):
        self.countdown_timer.stop()  # Stop the countdown timer
        self.show_mole_timer.stop()  # Stop the mole timer
        QMessageBox.information(self, 'Game Over', f'Game over! Final score: {self.score}')  # Show game over message
        print('Game Over!')  # Print game over to console
        self.close()  # Close the game window
        file = open('Whack The Mole Score', 'w')  # Open file to save score
        file.write(f'You scored: {self.score}')  # Write score to file
        file.close()  # Close the file

# Closes the game
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create the application
    game = WhackAMoleGame()  # Initialize the game
    game.show()  # Show the game window
    sys.exit(app.exec_())  # Run the application
