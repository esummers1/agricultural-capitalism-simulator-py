from acs.game import *
from acs.input_providers import *


if __name__ == "__main__":

    # Create game state with max years and initial funds
    game = Game(20, 500)

    # Ask if user wants human or AI version
    print('\nDo you wish to play manually (1), or launch the algorithm (2)?')

    while True:
        selection = int(input())

        if selection == 1:
            input_provider = PlayerInputProvider(game)
            break
        elif selection == 2:
            input_provider = AIInputProvider(game)
            break

    game.input_provider = input_provider
    game.run()


