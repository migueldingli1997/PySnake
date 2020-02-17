# PySnake
The classic arcade game Snake reimagined in Python using [Pygame](https://www.pygame.org/news) 🐍

## Requirements
Python 3 with Pipenv

## Run Game
From the project directory:

```bash
pipenv sync
pipenv run python src/main.py
```
or:
```bash
bash run_game.sh
```

## Configuration
Look into `config.ini`

## Gameplay and Controls

### Gameplay
The objective of the game is to eat as many apples as possible. With each apple consumed, the snake's length increases by 1. That sounds easy! However, the game gets harder as more apples are consumed. If the snakes bumps into itself, it's game over. Additionally, skulls scattered across the field cause negative consequences, but powerups sometimes appear to help out.

An extra green skull is added for each apple consumed, whereas gray skulls are less frequent. Powerups that are not picked up disappear if an apple is consumed! 

#### Skulls
- ![](img/skulls/enemy/900.png) **Gray**: Immediate game-over
- ![](img/skulls/poison/900.png) **Green**: Reduces the snake's length by one

#### Powerups
- ![](img/powerups/shield/900.png) **Shield**: one-time-use protection against skulls and bullets
- ![](img/powerups/ghost/900.png) **Ghost**: walk through skulls and yourself for 10 seconds
- ![](img/powerups/bullets/900.png) **Bullets**: receive 10 bullets capable of destroying skulls
- ![](img/powerups/bomb/900.png) **Bomb**: immediately clears any skull from the entire field

Firing bullets at yourself has the same effect as a green skull, i.e. the snake's length is reduced by one. Similarly, if the snake is shielded, the shield gets destroyed instead of the snake shrinking.

### Controls
#### Default Controls
- Set snake direction: `Up`/`Down`/`Left`/`Right` arrows
- Boost snake speed: `LShift` or `RSHift`
- Fire bullets: `X`
- Pause: `Esc` or `Space`
- Quit: `Alt`+`F4` or close the window

#### Reconfigure Controls
From the project directory:

```bash
pipenv sync
pipenv run python src/reconfig_controls.py
```
or:
```bash
bash run_reconfig_controls.sh
```

### Screenshot
![](img/screenshot.png)
