import sys

import names
import pygame as pg

from src.utils.config import Config, Player


def add_players():
    # Create screen
    screen: pg.Surface = pg.display.set_mode((100, 100))
    screen.fill(pg.Color('black'))

    # Load
    cfg = Config('config.ini')
    cfg.read()

    # Controls
    control_messages = [
        'point snake up',
        'point snake down',
        'point snake left',
        'point snake right',
        'pause game',
        'boost snake',
        'shoot bullet',
    ]

    # Input controls
    controls = []
    for cm in control_messages:
        print('Press button for "{}"...'.format(cm))
        print('ENTER to submit new button/s')
        sys.stdout.flush()

        buttons = []
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if len(buttons) == 0:
                            screen.fill(pg.Color('red'))
                            pg.display.update()
                            print("No button set yet.")
                            sys.stdout.flush()
                        else:
                            controls.append(buttons)
                            done = True
                            print("Button/s saved.")
                            sys.stdout.flush()
                            break
                    elif event.key in buttons:
                        screen.fill(pg.Color('red'))
                        pg.display.update()
                        print("Button already used.")
                        sys.stdout.flush()
                    else:
                        screen.fill(pg.Color('green'))
                        pg.display.update()
                        buttons.append(event.key)
                        print('Added: {}'.format(pg.key.name(event.key)))
                        sys.stdout.flush()
                elif event.type == pg.KEYUP:
                    screen.fill(pg.Color('black'))
                    pg.display.update()
                elif event.type == pg.QUIT:
                    return  # discard changes

    # Close screen
    pg.quit()

    # Player name
    name = input('Please insert a player name (blank for random): ')
    if name == "":
        name = names.get_first_name()
        print('Picked random name: {}'.format(name))

    # Save name and controls
    cfg.add_player(Player(name, controls[0], controls[1], controls[2],
                          controls[3], controls[4], controls[5], controls[6]))
    cfg.write()


def del_players():
    # Load
    cfg = Config('config.ini')
    cfg.read()

    while True:
        # List of players
        print('Players:')
        for p in cfg.players:
            print('\t{}'.format(p.name))

        # Get name to delete
        name = input('Please insert a player name to remove '
                     '(blank to save and quit): ')
        if name == "":
            break

        filtered_players = [p for p in cfg.players if p.name != name]
        if len(cfg.players) > len(filtered_players):
            print('Deleted {} players.'.format(
                len(cfg.players) - len(filtered_players)))
            cfg.players = filtered_players
        else:
            print('No players with that name.')

    # Save new list of players
    cfg.write()
