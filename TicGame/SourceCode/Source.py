import random
from pymongo import MongoClient

# Initialize MongoDB client and database
client = MongoClient('mongodb://localhost:27017/')
db = client.TicTacPlayers
Users = db.Users

class Tic2Player:
    def __init__(self, User):
        self.board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        self.current_player = "X"
        self.winner = None
        self.game_running = True
        self.User = User

    def print_board(self):
        print(f"{self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("--+---+--")
        print(f"{self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("--+---+--")
        print(f"{self.board[6]} | {self.board[7]} | {self.board[8]}")

    def Sysinput(self, inp):
        inp = int(inp)
        if 1 <= inp <= 9 and self.board[inp - 1] == "-":
            self.board[inp - 1] = self.current_player
            return
        print("Invalid spot! Pslease try again.")

    # Function to take player input
    def player_input(self):
        while True:
            inp = input("Input a number 1-9: ")
            inp = int(inp)
            if 1 <= inp <= 9 and self.board[inp - 1] == "-":
                self.board[inp - 1] = self.current_player
                return
            print("Invalid spot! Please try again.")

    # Function to check for a winner
    def check_winner(self):
        # Check horizontal, vertical, and diagonal lines
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertical
                          (0, 4, 8), (2, 4, 6)]  # Diagonal
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != "-":
                self.winner = self.board[condition[0]]
                self.game_running = False
                return True
        return False

    def updateUserWins(self):
        if self.winner == "X":
            self.User.updateWins()

    # Function to check for a tie
    def check_tie(self):
        if "-" not in self.board:
            print("It's a tie")
            self.game_running = False

    # Function to switch player
    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    # Function for AI opponent move
    def ai_opp(self):
        while self.current_player == "O":
            position = random.randint(0, len(self.board) - 1)
            if self.board[position] == "-":
                self.board[position] = "O"
                self.switch_player()
                break

    def game_loop(self):
        while self.game_running:
            self.print_board()
            self.player_input()
            if self.check_winner():
                print(f"The winner is {self.winner}")
                self.print_board()
                self.updateUserWins()
                self.handle_menu()
            elif self.check_tie():
                self.handle_menu()
                break
            if self.game_running:
                self.switch_player()
                self.ai_opp()
                if self.check_winner():
                    print(f"The winner is {self.winner}")
                    self.game_running = False
                    self.print_board()
                    self.handle_menu()
                elif self.check_tie():
                    self.handle_menu()
                    break

    def print_menu(self):
        print("\nMenu:")
        print("1. Check total wins")
        print("2. Start a new game")
        print("3. Exit")

    def handle_menu(self):
        while True:
            self.print_menu()
            choice = input("Enter your choice (1-3): ")
            if choice == "1":
                self.User.getWins()
            elif choice == "2":
                self.reset_game()
                self.game_loop()  # Start the game loop after resetting
                break
            elif choice == "3":
                print("Thanks for playing!")
                exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    def reset_game(self):
        self.board = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
        self.winner = None
        self.current_player = "X"
        self.game_running = True

class User():
    def __init__(self):
        self.Nickname = None
        self.Wins = 0

    def updateNickname(self):
        name = input("Enter your nickname: ")
        existing_user = Users.find_one({"Nickname": name})
        if existing_user:
            print("Nickname already taken. Welcome back!")
            self.Nickname = existing_user["Nickname"]
            self.Wins = existing_user["Wins"]
        else:
            self.Nickname = name
            Users.insert_one({"Nickname": self.Nickname, "Wins": self.Wins})

    def updateWins(self):
        self.Wins += 1
        Users.update_one({"Nickname": self.Nickname}, {"$set": {"Wins": self.Wins}})

    def getWins(self):
        user_record = Users.find_one({"Nickname": self.Nickname})
        if user_record:
            pulledwins = user_record["Wins"]
            print(f"Total wins for {self.Nickname}: {pulledwins}")
        else:
            print("You have no wins")


if __name__ == "__main__":
    user = User()
    Tic2Player = Tic2Player(user)
    Tic2Player.User.updateNickname()
    Tic2Player.handle_menu()

# if __name__ == "__main__":
#     user = User()
#     Tic2Player = Tic2Player(user)
#     Tic2Player.User.updateNickname()
#
#     while Tic2Player.game_running:
#         Tic2Player.print_board()
#         Tic2Player.player_input()
#         if Tic2Player.check_winner():
#             print(f"The winner is {Tic2Player.winner}")
#             Tic2Player.updateUserWins()
#         elif Tic2Player.check_tie():
#             break
#         if Tic2Player.game_running:
#             Tic2Player.switch_player()
#             Tic2Player.ai_opp()
#             if Tic2Player.check_winner():
#                 print(f"The winner is {Tic2Player.winner}")
#                 Tic2Player.game_running = False
#             elif Tic2Player.check_tie():
#                 break