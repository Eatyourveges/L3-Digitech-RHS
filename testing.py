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
        self.num_holes = 25  # Total number of holes
        self.mole_hole = None  # Current mole hole
        self.score = 0  # Player's score
        self.time_left = 0  # Remaining time
        self.game_running = True  # Game state

        self.setWindowTitle('Whack-The-Mole')  # Set the window title

        # Layouts
        self.main_layout = QVBoxLayout()  # Main vertical layout
        self.grid_layout = QHBoxLayout()  # Horizontal layout for buttons
    
        # Timer input: Get user-defined game time
        self.timer_limit, ok = QInputDialog.getInt(self, 'Whack-the-Mole Timer', 'Enter the game time in seconds between 15 sec to 60 sec:', min=15, max=60)

        # Mole speed input: Get user-defined mole speed
        self.mole_speed, ok = QInputDialog.getInt(self, 'Mole Speed', 'Enter mole speed in seconds (500(Hard) - 1000(Normal)):', min=500, max=1000)
        
        # Timer and score display
        self.time_left = self.timer_limit  # Set initial time left
        self.timer_label = QLabel(f'Time Left: {self.time_left} sec')  # Display time left
        self.score_label = QLabel(f'Score: {self.score}')  # Display score
        self.main_layout.addWidget(self.score_label)  # Add score label to main layout
        self.main_layout.addWidget(self.timer_label)  # Add timer label to main layout

        # Buttons for holes
        self.buttons = [QPushButton('') for _ in range(self.num_holes)]  # Create buttons for each hole
        self.buttons_layout = QVBoxLayout()  # Layout for button grid
        
        # Creates the grid layout for buttons
        for i in range(5):
            row_layout = QHBoxLayout()  # Horizontal layout for each row
            for j in range(5):
                button = self.buttons[i*5 + j]  # Get the button for the current hole
                button.setFixedSize(100, 100)  # Set button size
                button.clicked.connect(self.on_button_click)  # Connect button click to handler
                row_layout.addWidget(button)  # Add button to row layout
            self.buttons_layout.addLayout(row_layout)  # Add row layout to buttons layout

        self.main_layout.addLayout(self.buttons_layout)  # Add button layout to main layout
        self.setLayout(self.main_layout)  # Set the main layout

        # Timer for the countdown
        self.countdown_timer = QTimer(self)  # Create a countdown timer
        self.countdown_timer.timeout.connect(self.update_timer)  # Connect timeout to update function
        self.countdown_timer.start(1000)  # Update every second

        # Timer for the moles to spawn
        self.show_mole_timer = QTimer()  # Create a timer for mole visibility
        self.show_mole_timer.timeout.connect(self.show_mole)  # Connect timeout to mole display function
        self.show_mole_timer.start(self.mole_speed)  # Start with user-defined mole speed

    # Updates the countdown timer display
    def update_timer(self):
        self.time_left -= 1  # Decrease time left
        self.timer_label.setText(f'Time Left: {self.time_left} sec')  # Update timer display
        if self.time_left == 0:  # Check if time is up
            self.end_game()  # End the game

    # Defines what the mole looks like 
    def show_mole(self):
        if self.mole_hole is not None:  # If there was a mole previously
            self.buttons[self.mole_hole].setText('')  # Remove the mole from the previous hole
        
        # Randomly select a hole for the mole to appear
        self.mole_hole = random.randint(0, self.num_holes - 1)
        self.buttons[self.mole_hole].setText('ʕ•ᴥ•ʔ')  # Show mole character in the selected hole

    # Defines what happens when the mole is clicked 
    def on_button_click(self):
        button = self.sender()  # Get the button that was clicked
        if button.text() == 'ʕ•ᴥ•ʔ':  # Check if the mole is clicked
            self.score += 1  # Increase score
            self.score_label.setText(f'Score: {self.score}')  # Update score display
            button.setText('')  # Remove mole from the button
            self.mole_hole = None  # Reset mole hole

    # Defines what happens when the timer is over
    def end_game(self):
        self.countdown_timer.stop()  # Stop countdown timer
        self.show_mole_timer.stop()  # Stop mole spawning timer
        QMessageBox.information(self, 'Game Over', f'Game over! Final score: {self.score}')  # Show game over message
        print ('Game Over!')  # Print game over message in console
        self.close()  # Close the game window
        # Save the final score to a file
        file = open('Whack The Mole Score', 'w')
        file.write(f'You scored: {self.score}')  # Write score to file
        file.close()  # Close the file

# Closes the game
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create the application
    game = WhackAMoleGame()  # Create an instance of the game
    game.show()  # Show the game window
    sys.exit(app.exec_())  # Execute the application
