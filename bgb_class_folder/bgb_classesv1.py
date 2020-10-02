bot_fav_color = "blue"


# Creating a parent class to use for various games
class Player:
    def __init__(self, name, fav_color):
        self.name = name
        self.fav_color = fav_color

    def __str__(self):
        if self.fav_color == "blue":
            return f"Hi {self.name}! My favorite color is also blue!"
        return f"Hi {self.name}! {self.fav_color} is an awesome color!"


# Forming a repeatable stack structure
class Stack:
    def __init__(self, abc):
        self.height = 4
        self.abc = abc

    def move_piece(self):
        _coordinates = input("Please tell the host your move in row#,col# format. ")
        self.height -= 1

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
        stack = input("Please enter which stack you will take the piece from (a, b, or c). ")
        if stack == 'a':
            self.stack_a.move_piece()
        elif stack == 'b':
            self.stack_b.move_piece()
        else:
            self.stack_c.move_piece()


# Initializing player variables
p1name, p1fav, p1col = input("Player 1: Enter your name, favorite color, and piece color (w/b) separated by spaces: ").split()
player1 = GobletPlayer(p1name, p1fav, p1col)
print(player1)
p2name, p2fav, p2col = input("Player 2: Enter your name, favorite color, and piece color (w/b) separated by spaces: ").split()
player2 = GobletPlayer(p2name, p2fav, p2col)
print(player2)
# End case for while loop
game_end = False
while not game_end:
    print("Host, send game picture.")
    # Spacer input ask that can take any text
    input("Did you send the picture? ")
    print(player1.name + ": ")
    player1.choose_stack()
    print("Host, make the move.\n")
    # Switch to player 2 move
    print(player2.name + ": ")
    player2.choose_stack()
    print("Host, make the move.")
    input("Did you send the picture? ")
    # Double confirmed decision to leave the game
    continue_game = input("Would you like to keep playing? (y/n) \n")
    if continue_game == 'n':
        if input("Are you sure you want to end the game? (y/n) ") == 'y':
            game_end = True
else:
    "Thanks for playing the game!"
