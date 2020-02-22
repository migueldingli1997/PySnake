import sys

from helpers.reconfig import reconfig_player, reconfig_controls

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Incorrect number of arguments.')
    elif sys.argv[1] == 'player':
        reconfig_player()
    elif sys.argv[1] == 'controls':
        reconfig_controls()
    else:
        print('Unexpected argument.')
