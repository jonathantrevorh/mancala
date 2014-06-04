import json
import urllib2
import re
from flask import Flask
from flask import request
from pprint import pprint
app = Flask(__name__)

users = {}

@app.route("/sms")
def sms():
    sender = request.args.get('From')
    command = request.args.get('Body')
    board = get_board(sender)
    board.play(command)
    response = str(board)
    return response

def get_board(phone):
    if phone not in users:
        users[phone] = Board()
    return users[phone]

class Board:
    def __init__(self):
        initial_marbles = 3
        self.side_size = 6
        self.data = [initial_marbles if x is not 0 and x is not self.side_size+1 else 0 for x in range(self.side_size*2+2)]
        self.message = ""

    def __str__(self):
        output = self.message
        if len(output) > 0:
            output += "\n"
        end = "  {0}\n"
        output += end.format(self.data[0])
        for x in range(1, self.side_size+1):
            output += self.row_as_string(x)
        output += end.format(self.data[self.side_size+1])
        return output

    def row_as_string(self, row):
        middle = "{0}{1} {2}{3}\n"
        left_index = row
        left = self.data[left_index]
        left_letter = self.get_letter(left_index)
        middle_index = self.side_size+1
        right_index = middle_index*2 - row
        right = self.data[right_index]
        right_letter = self.get_letter(right_index)
        return middle.format(left_letter, left, right_letter, right)

    def play(self, command):
        self.message = ""
        command = command.lower()
        length = len(command)
        if length == 1:
            position = self.get_position(command)
            if self.is_valid_position(position):
                can_play_again = self.play_position(position)
                if can_play_again:
                    self.message = "Your go again"
                else:
                    self.computer_play()
                if self.game_is_over():
                    self.reset()
            else:
                self.message = "Out of bounds"
        else:
            try:
                getattr(self, command)()
            except AttributeError:
                self.message = "Invalid move"

    def computer_play(self):
        available_positions = [self.get_letter(x) for x in range(self.side_size+2, self.side_size*2+2)]
        print available_positions
        moves = []
        while True:
            chosen_position = self.pick_good_position(available_positions)
            moves.append(chosen_position)
            can_play_again = self.play_position(self.get_position(chosen_position))
            if not can_play_again:
                break
        self.message = "Computer played {0}".format("".join(moves))

    def pick_good_position(self, positions):
        for position in positions:
            if self.data[self.get_position(position)] is not 0:
                return position
        return positions[0]

    def start(self):
        self.message = "Let the games begin\nEnter a letter to play that slot (you're left, gonig anti-clockwise)"

    def reset(self):
        self.message = "Game reset"

    def quit(self):
        reset()

    def play_position(self, position):
        marbles = self.data[position]
        self.data[position] = 0
        position += 1
        for x in range(position, position + marbles):
            self.data[x % len(self.data)] += 1
            position += 1
        position -= 1
        landed_in_end = position is 0 or position is self.side_size+1
        return landed_in_end

    def get_position(self, command):
        command = command.lower()
        ordinal = ord(command)
        ordinal -= 97
        return ordinal

    def get_letter(self, index):
        return chr(index+97).upper()

    def is_valid_position(self, position):
        return position >= 1 and len(self.data)/2-1

if __name__ == "__main__":
    app.debug = True
    app.run()