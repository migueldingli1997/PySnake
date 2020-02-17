import sys

import pygame as pg

from helpers.config import Config


def reconfig_controls():
    # Create screen
    screen: pg.Surface = pg.display.set_mode((100, 100))
    screen.fill(pg.Color('black'))

    # Load
    cfg = Config('config.ini')
    cfg.read()

    # Controls
    controls = [
        ('point snake up', cfg.ctrl_up),
        ('point snake down', cfg.ctrl_down),
        ('point snake left', cfg.ctrl_left),
        ('point snake right', cfg.ctrl_right),
        ('pause game', cfg.ctrl_pause),
        ('boost snake', cfg.ctrl_boost),
        ('shoot bullet', cfg.ctrl_shoot),
    ]

    for i, control in enumerate(controls):
        control_title = control[0]
        control_buttons = control[1]
        control_button_names = [pg.key.name(c) for c in control_buttons]
        print('Press button for "{}"...'.format(control_title))
        print('Current: {}'.format(', '.join(control_button_names)))
        print('ESCAPE to keep current button/s')
        print('ENTER to submit new button/s')
        sys.stdout.flush()

        new_control_buttons = []

        done_keep = False
        done_save = False
        while not done_keep and not done_save:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        done_keep = True
                        print("Keeping old buttons.")
                        sys.stdout.flush()
                        break
                    elif event.key == pg.K_RETURN:
                        if len(new_control_buttons) == 0:
                            screen.fill(pg.Color('red'))
                            pg.display.update()
                            print("No button set yet.")
                            sys.stdout.flush()
                        else:
                            done_save = True
                            print("Button/s saved.")
                            sys.stdout.flush()
                            break
                    elif event.key in new_control_buttons:
                        screen.fill(pg.Color('red'))
                        pg.display.update()
                        print("Button already used.")
                        sys.stdout.flush()
                    else:
                        screen.fill(pg.Color('green'))
                        pg.display.update()
                        new_control_buttons.append(event.key)
                        print('Added: {}'.format(pg.key.name(event.key)))
                        sys.stdout.flush()
                elif event.type == pg.KEYUP:
                    screen.fill(pg.Color('black'))
                    pg.display.update()
                elif event.type == pg.QUIT:
                    return  # discard changes

        if done_save:
            controls[i] = (controls[i][0], new_control_buttons)

        print()

    cfg.ctrl_up = controls[0][1]
    cfg.ctrl_down = controls[1][1]
    cfg.ctrl_left = controls[2][1]
    cfg.ctrl_right = controls[3][1]
    cfg.ctrl_pause = controls[4][1]
    cfg.ctrl_boost = controls[5][1]
    cfg.ctrl_shoot = controls[6][1]
    cfg.write()


if __name__ == '__main__':
    reconfig_controls()
