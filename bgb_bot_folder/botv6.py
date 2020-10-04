# bot.py
import os
import time

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

bot_fav_color = "blue"
turn_length = 60
end_frequency = 2 

player1_stacks = [1111, 1111, 1111, 0]
player2_stacks = [1111, 1111, 1111]

class Player:
    def __init__(self, name, fav_color, discord_id):
        
        self.name = name
        self.fav_color = fav_color
        self.discord_id = discord_id

    def __str__(self):
        if self.fav_color == "blue":
            return f"Hi {self.name} 😉! My favorite color is also blue! 🐬"
        return f"Hi {self.name} 😉! I think {self.fav_color} is an awesome color 🎨!"

class Stack:
    def __init__(self, abc):
        self.height = 4
        self.abc = abc

    def move_piece(self):
        if self.height > 0:
            self.height -= 1
        else:
            return "Stack is empty. 😯"

    def __str__(self):
        return "l" * self.height

class GobbletPlayer(Player):
    def __init__(self, name, fav_color, discord_id, wb):

        self.color = wb
        self.stack_a = Stack(name + '_a')
        self.stack_b = Stack(name + '_b')
        self.stack_c = Stack(name + '_c')
        super().__init__(name, fav_color, discord_id)

    def choose_stack(self):
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

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"""Hi {member.name}, welcome to my Discord server!
        
Dictionary:
If I message __, What does it do? 
Gobblet: You will start a new game of the game Gobblet
GoPlay: You will begin playing GobbletGobbler
Host [name] : Tells the bot who has the physical board game. 
    Example: if Jess is the host, she will type "Host Jess"
sent: Tells the bot you have sent an image of the physical board game
made: Tells the bot that a new move has been made on the physical board game. 
Quit: You will quit the game. 
p# Stack a: You would like to choose one of the four pieces from the first stack 
    *Each time you do this the stack will get smaller. 
p# Stack b: You would like to choose one of the four pieces from the second stack 
    *Each time you do this the stack will get smaller. 
p# Stack c: You would like to choose one of the four pieces from the third stack 
    *Each time you do this the stack will get smaller. 
p# Stack z: You would like to move a piece already on the board.
win: someone has won the game."""
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass

    else:

        if message.content[:4].lower() == 'sent':
            if player1_stacks[3] % 2 == 0: #for sending original board
                await message.channel.send("Player1, now specify which stack you want to move with the format 'p# stack (a/b/c/z)'.")
                player1_stacks[3] += 1
            else: #everytime player2 moves
                await message.channel.send("Player2, now specify which stack you want to move with the format 'p# stack (a/b/c/z)'.")
                player1_stacks[3] += 1

        elif message.content[:4].lower() == 'made':
            if player1_stacks[3] % 2 == 1: #everytime after player1 moved
                await message.channel.send("Host, please send a picture followed by the word 'sent'")
            else:
                await message.channel.send("Player1, now specify which stack you want to move with the format 'p# stack (a/b/c/z)'.")
                player1_stacks[3] += 1

        elif message.content[:9].lower() == 'instruct':
            await message.channel.send("""Dictionary:
If I message __, What does it do? 
Gobblet: You will start a new game of the game Gobblet
GoPlay: You will begin playing GobbletGobbler
Host [name] : Tells the bot who has the physical board game. 
    Example: if Jess is the host, she will type "Host Jess"
sent: Tells the bot you have sent an image of the physical board game
made: Tells the bot that a new move has been made on the physical board game. 
instruct: Show the dictionary.
Quit: You will quit the game. 
p# Stack a: You would like to choose one of the four pieces from the first stack 
    *Each time you do this the stack will get smaller. 
p# Stack b: You would like to choose one of the four pieces from the second stack 
    *Each time you do this the stack will get smaller. 
p# Stack c: You would like to choose one of the four pieces from the third stack 
    *Each time you do this the stack will get smaller. 
p# Stack z: You would like to move a piece already on the board.
win: someone has won the game.""")

        elif message.content[:7] == "Gobblet":
            # player1_stacks = [1111, 1111, 1111, 0]
            # player2_stacks = [1111, 1111, 1111]
            response = """Get ready to play Gobblet!

    \nYour goal in Gobblet Gobblers is to place four of your pieces in a horizontal, vertical or diagonal row. 
Your pieces can stack on top of each other and they start the game nested, off the board. 
On a turn, you either play one exposed piece from your three off-the-board piles or move one piece on the board to any other spot on the board where it fits. 

A larger piece can cover any smaller piece.
Your memory is tested as you try to remember which color one of your larger pieces is covering before you move it. 
As soon as a player has four like-colored pieces in a row, he wins — except in one case: 
If you lift your piece and reveal an opponent's piece that finishes a four-in-a-row, you don't immediately lose; 
you can't return the piece to its starting location, but if you can place it over one of the opponent's three other pieces in that row, the game continues.

Follow the instructions: 
1. Players: Enter your player#, name, favorite color, and piece color (White/Black) separated by spaces (ex. player1 Jacob blue White):
2. Type out GoPlay when ready to start playing :blush:"""
            await message.channel.send(response)

        elif message.content[3:14].lower() == 'show stacks':
            if message.content[:2].lower() == 'p1':
                await message.channel.send(f"Stack A: {player1_stacks[0]}, Stack B: {player1_stacks[1]}, Stack C: {player1_stacks[2]}")
            else:
                await message.channel.send(f"Stack A: {player2_stacks[0]}, Stack B: {player2_stacks[1]}, Stack C: {player2_stacks[2]}")
            
        elif message.content[3:8].lower() == 'stack':
            stack = message.content.split()[2].lower()
            if message.content[:2].lower() == 'p1':
                if stack == 'a':
                    if player1_stacks[0] == 0:
                        await message.channel.send("This stack is empty, please choose another stack. You can see the stacks by using 'show stack'.")
                    else:
                        player1_stacks[0] //= 10
                        await message.channel.send("Please tell the host your move in row#,col# format. Host send 'made' when done.")
                elif stack == 'b':
                    if player1_stacks[1] == 0:
                        await message.channel.send("This stack is empty, please choose another stack. You can see the stacks by using 'show stack'.")
                    else:
                        player1_stacks[1] //= 10
                        await message.channel.send("Please tell the host your move in row#,col# format. Host send 'made' when done.")
                elif stack == 'c':
                    if player1_stacks[2] == 0:
                        await message.channel.send("This stack is empty, please choose another stack. You can see the stacks by using 'show stack'.")
                    else:
                        player1_stacks[2] //= 10
                        await message.channel.send("Please tell the host your move in row#,col# format. Host send 'made' when done.")
                else:
                    await message.channel.send("Please tell the host your original piece location in row#,col# format.\nPlease tell the host your final piece location in row#,col# format. ")
            else:
                if stack == 'a':
                    if player2_stacks[0] == 0:
                        await message.channel.send("This stack is empty, please choose another stack. You can see the stacks by using 'show stack'.")
                    else:
                        player2_stacks[0] //= 10
                        await message.channel.send("Please tell the host your move in row#,col# format. Host send 'made' when done.")
                elif stack == 'b':
                    if player2_stacks[1] == 0:
                        await message.channel.send("This stack is empty, please choose another stack. You can see the stacks by using 'show stack'.")
                    else:
                        player2_stacks[1] //= 10
                        await message.channel.send("Please tell the host your move in row#,col# format. Host send 'made' when done.")
                elif stack == 'c':
                    if player2_stacks[2] == 0:
                        await message.channel.send("This stack is empty, please choose another stack. You can see the stacks by using 'show stack'.")
                    else:
                        player2_stacks[2] //= 10
                        await message.channel.send("Please tell the host your move in row#,col# format. Host send 'made' when done.")
                else:
                    await message.channel.send("Please tell the host your original piece location in row#,col# format.\nPlease tell the host your final piece location in row#,col# format. ")
                    
        elif message.content[:7].lower() == 'player1':
            name, fav, col = message.content[8:].split()
            player1 = GobbletPlayer(name, fav, message.author, col)
            await message.channel.send(player1)

        elif message.content[:7].lower() == 'player2':
            name, fav, col = message.content[8:].split()
            player2 = GobbletPlayer(name, fav, message.author, col)
            await message.channel.send(player2)

        elif message.content[:4].lower() == "host":
            host_name = message.content.split()[1]
            await message.channel.send(host_name + " is the host." + "\nSend the first picture and just keep moving forward with the appropriate commands 😃")

        elif message.content[:6] == "GoPlay":
            response = """The game is starting! Every turn consists of three parts:
    1. The Host sends a picture of the physical game 📷 with the message 'sent'
    2. The Player taking their turn will choose the stack they want to play from (send the message "p# stack a/b/c") or if they want to move an existing piece on the board (send the message "p# stack z") 
    3. The Host will make the move on their actual board, and send the message 'made'
    
    Players repeat this framework until the game is over!
    If you want to see your stacks of pieces, use 'show stacks'
    If you want to see all possible commands, use 'instruct'
    If someone has won the game, use 'win'
    Now choose the host by sending the message 'host [name]'"""
            await message.channel.send(response)
            
        elif message.content[:4].lower() == 'quit':
            await message.channel.send("Goodbye! Send the message 'Gobblet' or another game name to start a new experience.")

        elif message.content[:3].lower() == 'win':
            if player1_stacks[3] % 2 == 0:
                await message.channel.send("Congratulations, player1! Send the message 'Gobblet' or another game name to start a new experience.")
            else:
                await message.channel.send("Congratulations, player2! Send the message 'Gobblet' or another game name to start a new experience.")

        # elif message.content[:4].lower() == 'reset':
        #     await message.channel.send("Confirm resetting? If so, send 'confirm'")
            
        # elif message.content[:4].lower() == 'confirm':
        #     player1_stacks = [1111, 1111, 1111, 0]
        #     player2_stacks = [1111, 1111, 1111]

bot.run(TOKEN)
