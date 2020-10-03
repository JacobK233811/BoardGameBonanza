# bot.py
import os
import random
import time

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

class Player:
    def __init__(self, name, fav_color, discord_ID):
        self.name = name
        self.fav_color = fav_color
        self.discord_ID = discord_ID

    def __str__(self):
        if self.fav_color == "blue":
            return f"Hi {self.name} 😉! My favorite color is also blue! 🐬"
        return f"Hi {self.name} 😉! I think {self.fav_color} is an awesome color 🎨!"

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

class GobbletPlayer(Player):
    def __init__(self, name, fav_color, discord_ID, wb):
        self.color = wb
        self.stack_a = Stack(name + '_a')
        self.stack_b = Stack(name + '_b')
        self.stack_c = Stack(name + '_c')
        super().__init__(name, fav_color, discord_ID)

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
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass
    else:
        if message.content[:7] == 'player1':
            name, fav, col = message.content[8:].split()
            player1 = GobbletPlayer(name, fav, message.author, col)
            await message.channel.send(player1)
        elif message.content[:7] == 'player2':
            name, fav, col = message.content[8:].split()
            player2 = GobbletPlayer(name, fav, message.author, col)
            await message.channel.send(player2)
        elif message.content[:4] == "host":
            host_name = message.content.split()[1]
            await message.channel.send(host_name + " is the host.")

        elif message.content[:4] == "test":
            pass
            
        elif message.content[:7] == "Gobblet":
            response = """Get ready to play Gobblet!
    \nYour goal in Gobblet Gobblers is to place four of your pieces in a horizontal, vertical or diagonal row. 
Your pieces can stack on top of each other and they start the game nested, off the board. 
On a turn, you either play one exposed piece from your three off-the-board piles or move one piece on the board to any other spot on the board where it fits. 
A larger piece can cover any smaller piece.

Your memory is tested as you try to remember which color one of your larger pieces is covering before you move it. 
As soon as a player has four like-colored pieces in a row, he wins — except in one case: 
If you lift your piece and reveal an opponent's piece that finishes a four-in-a-row, you don't immediately lose; 
you can't return the piece to its starting location, but if you can place it over one of the opponent's three other pieces in that row, the game continues.

For this Discord bot, players use stack z to designate a move of a piece already on the board. Command !quit will end the game.\n
    """ + "\nMove to player set-up." + "\n\nFollow the instructions and type out GoPlay when ready to start playing 😊 \nPlayers: Enter your name, favorite color, and piece color (White/Black) separated by spaces and preceded by the word player#: "
            await message.channel.send(response)

        elif message.content[:6] == "GoPlay":
            response = """The game is starting! Every turn consists of three parts:
    1. Host sends the game picture 📷, and send "sent"
    2. Player states their move using message 'stack (a/b/c/z)'
    3. Host makes the move on the actual board, and send "made"
    
    Players repeat this framework until the game is over!"""
            await message.channel.send(response)

bot.run(TOKEN)