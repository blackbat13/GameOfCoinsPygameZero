import pgzrun
from gameOfCoins import GameOfCoins
from easyAI import *
import random

WIDTH = 840
HEIGHT = 600

game = None

dices = []

coins = []

win = 0
timer = 120


def draw():
    screen.fill("white")
    for die in dices:
        die.draw()

    for cn in coins:
        cn.draw()

    if win == 1:
        screen.draw.text("You win!", center=(WIDTH / 2, HEIGHT / 3), color="blue", fontsize=120)
    elif win == 2:
        screen.draw.text("AI wins!", center=(WIDTH / 2, HEIGHT / 3), color="blue", fontsize=120)
    elif timer > 0 and game.current_player == 2:
        screen.draw.text("AI thinks...", center=(WIDTH / 2, HEIGHT - 200), color="red", fontsize=90)
    elif game.current_player == 1:
        screen.draw.text("Your move!", center=(WIDTH / 2, HEIGHT - 200), color="red", fontsize=90)


def update():
    global win, timer

    timer -= 1

    if game.current_player == 2 and not game.is_over() and timer <= 0:
        move = game.get_move()
        remove_coins(int(move))
        game.play_move(move)
        print(move)

        if game.is_over():
            win = 1


def on_mouse_down(pos):
    global win, timer

    for i in range(len(dices)):
        if dices[i].collidepoint(pos) and game.current_player == 1:
            move = game.possible_moves()[i]
            if int(move) <= game.pile:
                game.play_move(move)
                remove_coins(int(move))
                timer = random.randint(120, 260)

                if game.is_over():
                    win = 2
            # print(game.possible_moves()[i])


def remove_coins(number):
    for i in range(number):
        coins.pop()


def init():
    global game

    tt = TranspositionTable()
    GameOfCoins.ttentry = lambda game: game.pile
    r, d, m = solve_with_iterative_deepening(
        GameOfCoins(),
        ai_depths=range(2, 20),
        win_score=100,
        tt=tt
    )

    algorithm = Negamax(13)

    game = GameOfCoins([Human_Player(), AI_Player(algorithm)])

    x = WIDTH / 2 - (len(game.possible_moves()) * (68 + 20) - 20) / 2 + 68 / 2
    y = HEIGHT - 68 - 20
    for move in game.possible_moves():
        dices.append(Actor(f"dice{move}", (x, y)))
        x += 68 + 20

    x = 55
    y = 50

    for i in range(1, game.pile + 1):
        coins.append(Actor("coin", (x, y)))
        x += 84 + 20

        if i % 8 == 0:
            y += 84 + 30
            x = 55


init()
pgzrun.go()
