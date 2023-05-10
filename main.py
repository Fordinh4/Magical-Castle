from game import Game


def main(filename):
    """
    Create the game object and proper game loop
    """
    quit = False
    game = Game()
    game.initialize_from_file(filename)

    while not quit:

        print(f"It's player {game.get_turn() + 1} turn")

        try:
            game.move()

        except Exception as e:
            print(e)

        # .count() is for the case if there is only one player left so the turn will be 0 all the time. 
        # To check the case where the player 1 win but player 2 is not so instead of indexing in a list of [player 1, player 2] 
        # using 0 (because the count is only 1 -> 1%1 = 0) in a loop, I will check for index of False in finished list!
        count = game.finished.count(False)
        if True in game.finished and count > 0:
            new_turn = game.finished.index(False)

        else:
            if count > 0:
                new_turn = (game.get_turn() + 1) % count

        game.set_turn(new_turn)     

        if game.is_finished():
            quit = True
            print(
                f"Final score is Player 1: {game.players[0].get_diamonds()} diamonds, Player 2: {game.players[1].get_diamonds()} diamonds! Good game!")


if __name__ == '__main__':
    filename = "castle.txt"
    main(filename)
