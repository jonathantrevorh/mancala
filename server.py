import json
import urllib2
import re
from flask import Flask
from flask import request
from flask import Response
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
    return Response(response, mimetype='text/plain')

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
        end = "     {0}\n"
        output += end.format(self.data[0])
        for x in range(1, self.side_size+1):
            output += self.row_as_string(x)
        output += end.format(self.data[self.side_size+1])
        return output

    def row_as_string(self, row):
        middle = "{0}{1}\t  {2}{3}\n"
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
            if self.is_valid_position(position) and self.is_valid_user_position(position):
                try:
                    can_play_again = self.play_position(position)
                    has_winner = self.check_win()
                    if not has_winner:
                        if can_play_again:
                            self.message = "Your go again"
                        else:
                            self.computer_play()
                except IndexError:
                    self.message = "Bad position"
            else:
                self.message = "Out of bounds"
        else:
            try:
                getattr(self, command)()
            except AttributeError:
                self.message = "Invalid move"
            self.check_win()

    def computer_play(self):
        available_positions = [self.get_letter(x) for x in self.get_computer_range()]
        moves = []
        has_win = False
        while True:
            chosen_position = self.pick_good_position(available_positions)
            moves.append(chosen_position)
            can_play_again = self.play_position(self.get_position(chosen_position))
            has_win = self.check_win()
            if not can_play_again or has_win:
                break
        if not has_win:
            self.message = "Computer played {0}".format("".join(moves))

    def pick_good_position(self, positions):
        can = []
        should = []
        for position in positions:
            p = self.get_position(position)
            num_marbles = self.data[p]
            can_play = num_marbles is not 0
            should_play = (p + num_marbles)%len(self.data) is 0
            if can_play:
                can.append(position)
                if should_play:
                    return position
        return can.pop()

    def get_winner(self):
        user_marbles = sum([self.data[x] for x in self.get_user_range()])
        computer_marbles = sum([self.data[x] for x in self.get_computer_range()])
        user_well_marbles = self.data[self.get_user_well()]
        computer_well_marbles = self.data[self.get_computer_well()]
        if user_marbles is 0 or computer_marbles is 0:
            if user_well_marbles > computer_well_marbles:
                return "User"
            elif user_well_marbles < computer_well_marbles:
                return "Computer"
            else:
                return "Both"
        return False

    def get_user_range(self):
        start = 1
        end = start + self.side_size
        return range(start, end)

    def get_user_well(self):
        return self.side_size + 1

    def get_computer_range(self):
        start = self.side_size+2
        end = start + self.side_size
        return range(start, end)

    def get_computer_well(self):
        return 0

    def check_win(self):
        winner = self.get_winner()
        if winner is not False:
            self.reset()
            self.message = "{0} wins! Game reset.".format(winner)
            return True

    def start(self):
        self.message = "Enter a letter to play that slot (you're on the left, going anti-clockwise)"

    def help(self):
        self.start()

    def reset(self):
        self.__init__()
        self.message = "Game reset"

    def win(self):
        user_positions = [x for x in self.get_user_range()]
        for position in user_positions:
            self.data[position] = 0
        self.data[self.get_user_well()] = 100

    def quit(self):
        self.reset()

    def play_position(self, position):
        marbles = self.data[position]
        if marbles is 0:
            raise IndexError()
        self.data[position] = 0
        position += 1
        for x in range(position, position + marbles):
            self.data[x % len(self.data)] += 1
            position += 1
        position -= 1
        position = position % len(self.data)
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
        return position >= 1 and position < len(self.data)

    def is_valid_user_position(self, position):
        return position in self.get_user_range()

if __name__ == "__main__":
    app.debug = True
    app.run()
