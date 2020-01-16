from PyQt5.QtWidgets import QApplication, QWidget, QShortcut, QPushButton, QGridLayout, QCheckBox

from PyQt5.QtGui import QKeySequence

from pygame import mixer
from functools import partial
import time


class Guitar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):            
        self.grid = QGridLayout()
        self.note_layout = QGridLayout()
        self.string_layout = QGridLayout()
        self.chord_layout = QGridLayout()
        
        self.create_notes()
        self.create_strings()
        self.create_chords()

        self.shortcut = QShortcut(QKeySequence("S"), self)
        self.shortcut.activated.connect(self.strum)

        self.grid.addLayout(self.note_layout, 0, 0)
        self.grid.addLayout(self.string_layout, 1, 0)
        self.grid.addLayout(self.chord_layout, 2, 0)
        
        self.setLayout(self.grid)
        self.setWindowTitle('Johns Guitar')
        self.show()

##############################################################################################################################

    def create_notes(self):
        self.buttons = []
        x_pos = 0
        y_pos = 0
        for i in range(36):
            note = str(i // 6) + '_' + str(i % 6)
            button = QPushButton(note)
            button.clicked.connect(partial(self.play_note, note, i))
            self.note_layout.addWidget(button, x_pos, y_pos)
            self.buttons.append(button)
            
            x_pos += 1
            if x_pos % 6 == 0:
                y_pos += 1
                x_pos = 0

##############################################################################################################################

    def create_chords(self):
        self.chords = {'G': [3, 2, 0, 0, 3, 3], 'A': [0, 0, 2, 2, 2, 0],
                       'E': [0, 2, 2, 1, 0, 0], 'Bm': [2, 2, 4, 4, 3, 2],
                       'Fm': [2, 4, 4, 3, 2, 2], 'C': [0, 3, 2, 0, 1, 0],
                       'Am': [0, 0, 2, 2, 1, 0], 'D': [0, 0, 0, 2, 3, 2],
                       'Cadd': [0, 3, 2, 0, 3, 3], 'B': [2, 2, 4, 4, 4, 2],
                       'Bb': [1, 1, 3, 3, 3, 1]}
        x_pos = 0
        y_pos = 0
        for i, j in self.chords.items():
            button = QPushButton(i)
            button.clicked.connect(partial(self.load_chord, j))
            self.chord_layout.addWidget(button, x_pos, y_pos)
            
            y_pos += 1
            if y_pos % 6 == 0:
                x_pos += 1
                y_pos = 0

        self.create_extras(x_pos, y_pos)

##############################################################################################################################

    def create_strings(self):
        self.current_string_note = []
        self.strings = []
        keys = ["1", "2", "3", "4", "5", "6"]
        for i in range(6):
            button = QPushButton(str(i))
            self.current_string_note.append(str(i) + '_0')

            self.shortcut = QShortcut(QKeySequence(keys[i]), self)
            self.shortcut.activated.connect(partial(self.play_string, i))
            
            button.clicked.connect(partial(self.play_string, i))
            self.string_layout.addWidget(button, 0, i)
            self.strings.append(button)

##############################################################################################################################

    def play_string(self, string):
        self.play_note(self.current_string_note[string], (int(self.current_string_note[string][0]) * 6) +
                       int(self.current_string_note[string][2]))
        
##############################################################################################################################
        
    def create_extras(self, x_pos, y_pos):
        self.last_played = lambda : print()
        last_played = QPushButton('Last played')
        last_played.clicked.connect(self.play_last)
        self.chord_layout.addWidget(last_played, x_pos, y_pos)

        strum = QPushButton('Strum')
        strum.clicked.connect(self.strum)
        self.chord_layout.addWidget(strum, x_pos + 1, 0)

        self.instant_strum = QCheckBox('Strum Instantly')
        self.chord_layout.addWidget(self.instant_strum, x_pos + 1, 1, 1, 2)

##############################################################################################################################        

    def play_note(self, note, identity):
        mixer.Channel(int(note[0])).play(mixer.Sound('faded sounds/' + note + '.wav'))
        
        for i in self.buttons:
            i.setStyleSheet("background-color: light grey")
            
        self.buttons[identity].setStyleSheet("background-color: red")

        self.last_played = partial(self.play_note, note, identity)
        self.current_string_note[int(note[0])] = note
        print('Note played')
        print(self.current_string_note)
        print(self.last_played)
        print(identity)

##############################################################################################################################

    def load_chord(self, chord):
        self.current_string_note = []
        for i in range(len(chord)):
            self.current_string_note.append(str(i) + '_' + str(chord[i]))

        if self.instant_strum.isChecked() == True:
                self.strum()
            
        self.last_played = partial(self.strum)

##############################################################################################################################

    def play_last(self):
        self.last_played()

##############################################################################################################################

    def strum(self):
        for i in self.current_string_note:
            self.play_note(i, ((int(i[0]) * 6) + int(i[2])))
            #time.sleep(0.005)

mixer.init()
mixer.set_num_channels(6)
app = QApplication([])
run = Guitar()
app.exec_()
