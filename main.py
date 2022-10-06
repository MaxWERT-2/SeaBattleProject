import typer
from battle_field import BattleField


def main(n: int, k: int):

    if n > 26 or k > 26:
        print("The size of the playing field cannot exceed 26")
        return

    if n < 5 or k < 5:
        print("the size of the playing field cannot be less than 5")
        return

    game = BattleField(n, k)

    if game.show_start_screen():
        game.my_fire()
    else:
        game.opp_fire()


if __name__ == "__main__":
    typer.run(main)
