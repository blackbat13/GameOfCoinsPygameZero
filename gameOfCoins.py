from easyAI import (AI_Player, Human_Player, TranspositionTable, TwoPlayerGame,
                    solve_with_iterative_deepening)


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
        print(f"{self.pile} coins remaining")

    def scoring(self):
        if self.pile <= 0:
            return 100
        else:
            return 0


if __name__ == "__main__":
    tt = TranspositionTable()
    GameOfCoins.ttentry = lambda game: game.pile
    r, d, m = solve_with_iterative_deepening(
        GameOfCoins(),
        ai_depths=range(2, 20),
        win_score=100,
        tt=tt
    )

    print(f"Can first player always win; {r}")
    print(f"Maximal number of moves to win: {d}")
    print(f"What should be the first move: {m}")

    game = GameOfCoins([AI_Player(tt), Human_Player()])
    history = game.play()
