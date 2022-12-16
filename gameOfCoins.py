from easyAI import *


class GameOfCoins(TwoPlayerGame):
    def __init__(self, players=None):
        self.players = players
        self.pile = 17
        self.current_player = 1

    def possible_moves(self):
        return ["1", "3", "4"]

    def make_move(self, move):
        self.pile -= int(move)

    def is_over(self):
        return self.pile <= 0

    def show(self):
        print(f"{self.pile} monet pozostało na stole")

    def scoring(self):
        if self.pile <= 0:
            return 100
        else:
            return 0


if __name__ == "__main__":
    # algorithm = Negamax(13)
    # game = GameOfCoins([Human_Player(), AI_Player(algorithm)])
    # history = game.play()

    tt = TranspositionTable()
    GameOfCoins.ttentry = lambda game: game.pile
    r, d, m = solve_with_iterative_deepening(
        GameOfCoins(),
        ai_depths=range(2, 20),
        win_score=100,
        tt=tt
    )

    print("Czy pierwszy gracz może zawsze wygrać:", r)
    print("Ile maksymalnie ruchów potrzeba do wygrania:", d)
    print("Jaki powinien być pierwszy ruch:", m)

    game = GameOfCoins([AI_Player(tt), Human_Player()])
    history = game.play()
