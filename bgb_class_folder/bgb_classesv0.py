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
        coordinates = input("Please tell the host your move in row#,col# format.")
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
        super.__init__(name, fav_color)
        
    def choose_stack(self):
        print(f"Stack A: {self.stack_a}, Stack B: {self.stack_b}, Stack C: {self.stack_c}")
        stack = input("Please enter which stack you will take the piece from (a, b, or c).")
        if stack == 'a':
            self.stack_a.move_piece()
        elif stack == 'b':
            self.stack_b.move_piece()
        else:
            self.stack_c.move_piece()
