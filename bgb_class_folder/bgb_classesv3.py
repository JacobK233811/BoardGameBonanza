import time


bot_fav_color = "blue"
turn_length = 60
end_game_ask = 2


# Creating a parent class to use for various games
class Player:
    def __init__(self, name, fav_color):
        self.name = name
        self.fav_color = fav_color

    def __str__(self):
        if self.fav_color == "blue":
            return f"Hi {self.name} 😉! My favorite color is also blue! 🐬"
        return f"Hi {self.name} 😉! I think {self.fav_color} is an awesome color 🎨!"


# Forming a repeatable stack structure
class Stack:
    def __init__(self, abc):
        self.height = 4
        self.abc = abc

    def move_piece(self):
        row, col = [int(value) for value in input("Please tell the host your move in row#,col# format. ").split(',')]
        if not -1 < row < 5 or not -1 < col < 5:
            self.move_piece()
        else:
            if self.height > 0:
                self.height -= 1
            else:
                return "Stack is empty. 😯"

    def __str__(self):
        return "l" * self.height


# To give the player 3 stacks of 4 pieces and identify whether they are playing as white or black
class GobletPlayer(Player):
    def __init__(self, name, fav_color, wb):
        self.color = wb
        self.stack_a = Stack(name + '_a')
        self.stack_b = Stack(name + '_b')
        self.stack_c = Stack(name + '_c')
        super().__init__(name, fav_color)

    def choose_stack(self):
        print(f"Stack A: {self.stack_a}, Stack B: {self.stack_b}, Stack C: {self.stack_c}")
        stack = input("Please enter which stack you will take the piece from (a, b, c, or z). ")
        # Timer functionality to encourage players to take less than 60 seconds per move
        the_time = time.time()
        end_time = time.time() + turn_length + 1
        while the_time < end_time:
            print(str(round(end_time - the_time, 1)) + " seconds left")
            if input("ready?") == "ready":
                break
            time.sleep(15)
            the_time = time.time()
        # Defined move in case stack choice is z
        move = None
        if stack == 'a':
            move = self.stack_a.move_piece()
        elif stack == 'b':
            move = self.stack_b.move_piece()
        elif stack == 'c':
            move = self.stack_c.move_piece()
        else:
            input("Please tell the host your original piece location in row#,col# format. ")
            _row, _col = [int(value) for value in input("Please tell the host your final piece location in row#,col# format. ").split(',')]
        if move is not None:
            print(move)
            self.choose_stack()


# Initializing player variables
p1name, p1fav, p1col = input("Player 1: Enter your name, favorite color, and piece color (White/Black) separated by spaces: ").split()
player1 = GobletPlayer(p1name, p1fav, p1col)
print(player1)
p2name, p2fav, p2col = input("Player 2: Enter your name, favorite color, and piece color (White/BlackJ) separated by spaces: ").split()
player2 = GobletPlayer(p2name, p2fav, p2col)
print(player2)
# Only checks if the last character is the number 1 or not because 1 and 2 are the only options
host_inquiry = input("Is Player 1 or Player 2 the host? ")
if host_inquiry[-1] == '1' or host_inquiry.lower() == 'one':
    host_name = player1.name
else:
    host_name = player2.name
# End case for while loop
game_end = False
# Increment token to not ask about winning the game before round 5
i = 0
print('''\nYour goal in Gobblet Gobblers is to place four of your pieces in a horizontal, vertical or diagonal row. 
Your pieces can stack on top of each other and they start the game nested, off the board. 
On a turn, you either play one exposed piece from your three off-the-board piles or move one piece on the board to any other spot on the board where it fits. 
A larger piece can cover any smaller piece.

Your memory is tested as you try to remember which color one of your larger pieces is covering before you move it. 
As soon as a player has four like-colored pieces in a row, he wins — except in one case: 
If you lift your piece and reveal an opponent's piece that finishes a four-in-a-row, you don't immediately lose; 
you can't return the piece to its starting location, but if you can place it over one of the opponent's two other pieces in that row, the game continues.

For this Discord bot, players use stack z to designate a move of a piece already on the board.\n''')
turn_length = int(input("Please specify desired turn length in seconds (15 second increments). "))
end_game_ask = int(input("Please specify how frequently we should ask if you want to leave the game (positive integer please). "))

while not game_end:
    print("\n" + host_name + ", send game picture. 📷")
    # Spacer input ask that can take any text
    input("Did you send the picture? ")
    print(player1.name + ": " + player1.color)
    player1.choose_stack()
    print(host_name + ", make the move.\n")
    # Switch to player 2 move
    print(player2.name + ": " + player2.color)
    player2.choose_stack()
    print(host_name + ", make the move.")
    # Only start asking about winning once it's feasible
    i += 1
    if i > 4:
        won_game = input("Has anyone won yet? 👑 (y/n) ")
        if won_game == 'y' and input("Really? 😲 (y/n) ") == 'y':
            game_end = True
    # Double confirmed decision to leave the game asked once every 2 turns
    if i % 2 == 0 and input("Would you like to keep playing? (y/n) 🎲 ") == 'n' and input("\nAre you sure you want to end the game? (y/n) ❌ ") == 'y':
        game_end = True
else:
    "Thanks for playing the game! 💙"
