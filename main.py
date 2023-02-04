import random

import pgzrun
from easyAI import AI_Player, Human_Player, Negamax
from gameOfCoins import GameOfCoins

""" CONFIGURATION """

WIDTH = 840
HEIGHT = 600

""" VARIABLES """

game = None

dices_list = []

coins_list = []

win = 0
timer = 120


""" DRAW """


def draw():
    screen.fill("white")
    draw_actors_list(dices_list)
    draw_actors_list(coins_list)
    draw_message()


def draw_actors_list(actors_list):
    for actor in actors_list:
        actor.draw()


def draw_message():
    if win == 1:
        screen.draw.text("You win!", center=(
            WIDTH / 2, HEIGHT / 3), color="blue", fontsize=120)
    elif win == 2:
        screen.draw.text("AI wins!", center=(
            WIDTH / 2, HEIGHT / 3), color="blue", fontsize=120)
    elif timer > 0 and game.current_player == 2:
        screen.draw.text("AI thinks...", center=(
            WIDTH / 2, HEIGHT - 200), color="red", fontsize=90)
    elif game.current_player == 1:
        screen.draw.text("Your move!", center=(
            WIDTH / 2, HEIGHT - 200), color="red", fontsize=90)


""" UPDATE """


def update():
    global win, timer

    timer -= 1

    if game.current_player == 2 and not game.is_over() and timer <= 0:
        move = game.get_move()
        remove_coins(int(move))
        game.play_move(move)

        if game.is_over():
            win = 1


""" EVENTS """


def on_mouse_down(pos):
    for i in range(len(dices_list)):
        if dices_list[i].collidepoint(pos) and game.current_player == 1:
            move = game.possible_moves()[i]
            make_human_move(move)


""" HELPERS """


def make_human_move(move):
    """Applies human move to game.

    Args:
        move (int): the number of coins to take from the pile.
    """
    global timer, win
    
    if int(move) <= game.pile:
        game.play_move(move)
        remove_coins(int(move))
        timer = random.randint(120, 260)

        if game.is_over():
            win = 2


def remove_coins(number):
    """Removes coins from the pile.

    Args:
        number (int): the number of coins to remove from the pile.
    """

    for i in range(number):
        coins_list.pop()


""" INITIALIZATION """


def init():
    init_game()
    init_dices()
    init_coins()


def init_game():
    """Initializes AI player and game from easyAI library
    """
    global game

    algorithm = Negamax(13)

    game = GameOfCoins([Human_Player(), AI_Player(algorithm)])


def init_dices():
    """Initializes dices.

    The dices are stored as a list of Actors, which contain the image of the
    dice and the position of the dice.
    """
    x = WIDTH / 2 - (len(game.possible_moves()) * (68 + 20) - 20) / 2 + 68 / 2
    y = HEIGHT - 68 - 20
    for move in game.possible_moves():
        dices_list.append(Actor(f"dice{move}", (x, y)))
        x += 68 + 20


def init_coins():
    """Initializes coins.
    """
    x = 55
    y = 50

    for i in range(1, game.pile + 1):
        coins_list.append(Actor("coin", (x, y)))
        x += 84 + 20

        if i % 8 == 0:
            y += 84 + 30
            x = 55


init()
pgzrun.go()
