from acs.launchers import *


if __name__ == "__main__":

    # Ask if user wants human or AI version
    print('\nDo you wish to play manually (1), or launch the algorithm (2)?')

    while True:
        selection = int(input())

        if selection == 1:
            launcher = PlayerLauncher()
            launcher.execute()
            break
        elif selection == 2:
            launcher = AILauncher()
            launcher.execute()
            break
