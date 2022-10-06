import random
import time
import pickle
import player
from win_pics import WIN_PIC_LIST


def my_symbol(pair):
    """
    Returns the character to output for the given cell for the player's field.
    :param pair: first element: 1 if it's a ship here, otherwise 0.
                 second element: 1 if a shot has been fired at the cell, otherwise 0.
    :return: the symbol to be output in the given cell
    """
    if pair == [0, 0]:
        return " "
    if pair == [0, 1] or pair == [0, 2]:
        return "*"
    if pair == [1, 0]:
        return "O"
    if pair == [1, 1]:
        return "X"


def opp_symbol(pair):
    """
    Returns the character to output for the given cell for the opponent's field.
    :param pair: list of two elements
                first element: 1 if it's a ship here, otherwise 0.
                second element: 1 if a shot has been fired at the cell, otherwise 0.
    :return: the symbol to be output in the given cell
    """
    if pair == [0, 0] or pair == [1, 0]:
        return " "
    if pair == [0, 1] or pair == [0, 2]:
        return "*"
    if pair == [1, 1]:
        return "X"


class BattleField(object):
    """
    Battle field in sea battle game.
    """

    def __init__(self, n, k):
        self.me = player.Player(n, k)
        self.opp = player.Player(n, k)
        self.me.auto_fill()
        self.opp.auto_fill()
        self.difficulty = ""

    def show_start_screen(self):
        """
        Outputs the start screen and returns the ownership of the first move and also sets the difficulty of the game.
        :return 1 if player want to start, otherwise 0
        """
        print("###############################################", sep="", end="")
        # Adds grids if the number is two-digit.
        if self.me.n >= 10:
            print("#", sep="", end="")
        if self.me.k >= 10:
            print("#", sep="", end="")
        print("\n", sep="", end="")
        print(
            "###Welcome to Sea battle game with ",
            self.me.n,
            "x",
            self.me.k,
            " field###\n",
            sep="",
            end="",
        )
        print("###############################################", sep="", end="")
        # Adds grids if the number is two-digit.
        if self.me.n >= 10:
            print("#", sep="", end="")
        if self.me.k >= 10:
            print("#", sep="", end="")
        print("\n", sep="", end="")
        print("\n\n\n\n\n\n\n\n\n\n", sep="", end="")
        while not (self.difficulty == "easy" or self.difficulty == "medium"):
            print(
                "Choose the difficulty of the game. (easy or medium)\n",
                sep="",
                end="",
            )
            self.difficulty = input()
            if not (self.difficulty == "easy" or self.difficulty == "medium"):
                print("Please, type easy or medium.\n", sep="", end="")
        input_str = ""
        while not (input_str == "yes" or input_str == "no"):
            print("Do you want to move first?\n", sep="", end="")
            input_str = input()
            if not (input_str == "yes" or input_str == "no"):
                print("Please, type yes or no\n", sep="", end="")
        if input_str == "yes":
            return 1
        else:
            return 0

    def show_my_field(self):
        """
        Outputs my playing field.
        :return: None
        """
        print("   ", sep="", end="")
        for i in range(self.me.n):
            letter = chr(ord("A") + i)
            print(letter, " ", sep="", end="")
        print("\n", sep="", end="")
        for j in range(self.me.k):
            print(j + 1, sep="", end="")
            if j + 1 < 10:
                print(" ", sep="", end="")
            for i in range(self.me.n):
                print("|", sep="", end="")
                print(my_symbol(self.me.field[i][j]), sep="", end="")
            print("|\n", sep="", end="")

    def show_opp_field(self):
        """
        Outputs the opponent's playing field.
        :return: None
        """
        print("   ", sep="", end="")
        for i in range(self.opp.n):
            letter = chr(ord("A") + i)
            print(letter, " ", sep="", end="")
        print("\n", sep="", end="")
        for j in range(self.opp.k):
            print(j + 1, sep="", end="")
            if j + 1 < 10:
                print(" ", sep="", end="")
            for i in range(self.opp.n):
                print("|", sep="", end="")
                print(opp_symbol(self.opp.field[i][j]), sep="", end="")
            print("|\n", sep="", end="")

    def show_field(self):
        """
        Outputs current playing field.
        :return: None
        """
        print("***", sep="", end="")
        for i in range(self.opp.n):
            print("**", sep="", end="")
        print("\n", sep="", end="")
        for i in range(int((2 * self.opp.n - 8) / 2)):
            print("*", sep="", end="")
        print("Opp", "'", "s Field", sep="", end="")
        for i in range(int((2 * self.opp.n - 8) / 2)):
            print("*", sep="", end="")
        print("\n", sep="", end="")
        print("***", sep="", end="")
        for i in range(self.opp.n):
            print("**", sep="", end="")
        print("\n", sep="", end="")

        self.show_opp_field()

        print("***", sep="", end="")
        for i in range(self.me.n):
            print("**", sep="", end="")
        print("\n", sep="", end="")
        for i in range(int((2 * self.me.n - 8) / 2)):
            print("*", sep="", end="")
        print("Your Field ", sep="", end="")
        for i in range(int((2 * self.me.n - 8) / 2)):
            print("*", sep="", end="")
        print("\n", sep="", end="")
        print("***", sep="", end="")
        for i in range(self.me.n):
            print("**", sep="", end="")
        print("\n", sep="", end="")

        self.show_my_field()

    def opp_fire(self):
        """
        Processes the opponent's shot and triggers the next turn.
        :return: None
        """
        self.show_field()

        x = 0
        y = 0

        if self.difficulty == "easy":
            coordinates = self.me.easy_turn()
            x = coordinates[0]
            y = coordinates[1]
        elif self.difficulty == "medium":
            coordinates = self.me.medium_turn()
            x = coordinates[0]
            y = coordinates[1]

        self.me.field[x][y][1] = 1

        print(
            "Your opponent shot at the cell ",
            chr(ord("A") + x),
            y + 1,
            ".\n",
            sep="",
            end="",
        )
        time.sleep(3)
        if self.me.field[x][y][0]:
            self.me.cur_ship_cell -= 1
            if not self.me.cur_ship_cell:
                print(
                    "Unfortunately, you lost. You'll be lucky next time!\n",
                    sep="",
                    end="",
                )
                time.sleep(3)
            else:
                print("Hit! The opponent makes an additional move.\n", sep="", end="")
                self.me.not_destroyed_yet = 1
                self.me.not_destroyed_coordinates = [x, y]
                time.sleep(3)
                if self.me.is_destroyed(x, y):
                    self.me.not_destroyed_yet = 0
                self.opp_fire()
        else:
            print("Miss! The move passes to you.\n", sep="", end="")
            time.sleep(3)
            self.my_fire()

    def my_fire(self):
        """
        Processes the player's shot and triggers the next turn.
        :return: None
        """
        self.show_field()

        print("Your turn:\n", sep="", end="")
        input_str = input()
        # Handling an empty string.
        while input_str == "":
            input_str = input()
        # Exit processing.
        if input_str == "end":
            return
        # Save processing.
        if input_str.split()[0] == "save":
            name = "auto_save.pickle"
            if len(input_str.split()) > 1:
                name = input_str.split()[1] + ".pickle"
            f = open(name, "wb")
            pickle.dump([self.me, self.opp, self.difficulty], f)
            f.close()
            print("Saving was successful.\n")
            time.sleep(2)
            return self.my_fire()
        # Load processing.
        if input_str.split()[0] == "load":
            name = "auto_save.pickle"
            if len(input_str.split()) > 1:
                name = input_str.split()[1] + ".pickle"
            try:
                f = open(name, "rb")
                fields = pickle.load(f)
                self.me = fields[0]
                self.opp = fields[1]
                self.difficulty = fields[2]
                f.close()
                return self.my_fire()
            except OSError:
                print("There is no save with this name.\n")
                time.sleep(5)
                return self.my_fire()
        # Wrong move processing.
        if not (
            ord("A") <= ord(input_str[0]) < ord("A") + self.opp.n
            and ord("1") <= ord(input_str[1]) <= ord("9")
        ):
            print(
                "Wrong Move. Your turn should consist of two symbols: Letters from A to ",
                chr(ord("A") + self.opp.n - 1),
                " and numbers from 1 to ",
                self.opp.k,
                ". Try again:\n",
                sep="",
                end="",
            )
            time.sleep(5)
            return self.my_fire()

        x = ord(input_str[0]) - ord("A")
        y = int(input_str[1])
        # Checking a number for two digits.
        if len(input_str) > 2:
            if not (
                ord("0") <= ord(input_str[2]) <= ord("9")
                and y * 10 + int(input_str[2]) <= self.opp.k
            ):
                print(
                    "Wrong Move. Your turn should consist of two symbols: Letters from A to ",
                    chr(ord("A") + self.opp.n - 1),
                    " and numbers from 1 to ",
                    self.opp.k,
                    ". Try again:\n",
                    sep="",
                    end="",
                )
                time.sleep(5)
                return self.my_fire()
            else:
                y = y * 10 + int(input_str[2])
        y -= 1

        if self.opp.field[x][y][1] == 1:
            print("You have already shot at this cell. Try again:\n", sep="", end="")
            time.sleep(3)
            return self.my_fire()

        self.opp.field[x][y][1] = 1

        # Auto save
        f = open("auto_save.pickle", "wb")
        pickle.dump([self.me, self.opp, self.difficulty], f)
        f.close()
        if self.opp.field[x][y][0]:
            self.opp.cur_ship_cell -= 1
            if not self.opp.cur_ship_cell:
                print("Congratulations! You won!\n", sep="", end="")
                time.sleep(3)
                # Reward for the winner.
                print(random.choice(WIN_PIC_LIST))
            else:
                if self.opp.is_destroyed(x, y):
                    print(
                        "Destroyed! You can make an additional move.\n", sep="", end=""
                    )
                    time.sleep(3)
                    self.my_fire()
                else:
                    print("Hit! You can make an additional move.\n", sep="", end="")
                    time.sleep(3)
                    self.my_fire()
        else:
            print("Miss! The move goes to the opponent.\n", sep="", end="")
            time.sleep(3)
            self.opp_fire()
