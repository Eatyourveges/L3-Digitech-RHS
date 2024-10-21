# * imports all functions from that library
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer
import random 


#This class is to define the entire process of the game
class ButtonGrid(QWidget):
    #This function has all the variables in it and initializes the code
    def __init__(self):
        super().__init__()
        # Game settings
        self.num_holes = 25
        self.mole_hole = None
        self.score = 0
        self.game_ended = False
        self.init_ui()

        # Layouts
        self.main_layout = QVBoxLayout
        self.grid_layout = QHBoxLayout

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


    #This function creates the board 
    def init_ui(self):
        self.setWindowTitle('Wack-The-Moe')

        #Sets the time limit for the game 

        self.time_limit, ok = QInputDialog.getInt(self, 'Wack-the-Moe Timer', f'Enter the game time in seconds between 30sec to 60sec:', min=30, max=60)


        self.buttons = [QPushButton('') for _ in range(self.num_holes)]
        self.buttons_layout = ()

        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.buttons = [[QPushButton(' ') for _ in range(5)] for _ in range(5)]

        self.buttons = [QPushButton('') for _ in range(self.num_holes)]
        self.buttons_layout = QVBoxLayout()
        
        for i in range(3):
            row_layout = QHBoxLayout()
            for j in range(3):
                button = self.buttons[i*3 + j]
                button.setFixedSize(100, 100)
                button.clicked.connect(self.on_button_click)
                row_layout.addWidget(button)
            self.buttons_layout.addLayout(row_layout)

        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

        for row in range(self.number_of_rows):
            for col in range(self.number_of_cols):
                button = self.buttons[row][col]
                button.setFixedSize(100,100)
                button.clicked.connect(lambda ch, row=row, col=col: self.button_clicked(row, col))
                self.grid.addWidget(button, row, col)

    def show_mole(self):
        if self.mole_hole is not None:
            self.buttons[self.mole_hole].setText('')
        
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
        QMessageBox.information(self, 'Game Over', f'Game over! Final score: {self.score}')
        print('Game Over')
        file = open('file.txt', 'w')
        file.write(f'You had {self.score} turns')
        self.close()


# Makes sure it is running the Main code
if __name__ == '__main__':

     # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Create a main application window (QWidget)
    game = ButtonGrid()
    game.show()
    # Execute the application's event loop
    sys.exit(app.exec_())