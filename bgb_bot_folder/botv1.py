# bot.py
import os
import random
import time

import discord
from dotenv import load_dotenv
from discord.ext import commands

# A complete class definition code follows:
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


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

# @client.event
# async def on_ready():
#     guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})'
#     )


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.event
async def on_message(message):
    if message.author != bot.user:
        if message.content[:7] == 'player1':
            player1 = GobletPlayer(message.content[8:].split())
            await message.channel.send(player1)
        elif message.content[:7] == 'player2':
            player2 = GobletPlayer(message.content[8:].split())
            await message.channel.send(player2)
    else:
        if 'Move to player set-up.' in message.content:
            response = "Players: Enter your name, favorite color, and piece color (White/Black) separated by spaces and preceded by the word player#: "
            await message.channel.send(response)
        elif message.content == 'raise-exception':
            raise discord.DiscordException


@bot.command(name='99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='Gobblet')
async def game_start(ctx):
    response = """Get ready to play Gobblet!
    \nYour goal in Gobblet Gobblers is to place four of your pieces in a horizontal, vertical or diagonal row. 
Your pieces can stack on top of each other and they start the game nested, off the board. 
On a turn, you either play one exposed piece from your three off-the-board piles or move one piece on the board to any other spot on the board where it fits. 
A larger piece can cover any smaller piece.

Your memory is tested as you try to remember which color one of your larger pieces is covering before you move it. 
As soon as a player has four like-colored pieces in a row, he wins — except in one case: 
If you lift your piece and reveal an opponent's piece that finishes a four-in-a-row, you don't immediately lose; 
you can't return the piece to its starting location, but if you can place it over one of the opponent's two other pieces in that row, the game continues.

For this Discord bot, players use stack z to designate a move of a piece already on the board.\n
    """ + "\nMove to player set-up."
    await ctx.send(response)

bot.run(TOKEN)
