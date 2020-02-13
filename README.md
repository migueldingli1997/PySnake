# PySnake
The classic arcade game Snake reimagined in Python using [Pygame](https://www.pygame.org/news) 🐍

## Requirements
Python 3 with Pipenv

## Run
From the project directory:

```bash
pipenv sync
pipenv run python src/main.py
```
or:
```bash
bash run.sh
```

## Configuration
Look into `config.ini`

## Gameplay and Controls

### Gameplay
The objective of the game is to eat as many apples as possible. With each apple consumed, the snake's length increases by 1. That sounds easy! However, the game gets harder as more apples are consumed. If the snakes bumps into itself, it's game over. Additionally, skulls scattered across the field cause negative consequences, but powerups sometimes appear to help out.

An extra green skull is added for each apple consumed, whereas gray skulls are less frequent. Powerups that are not picked up disappear if an apple is consumed! 

#### Skulls
- ![](img/skulls/enemy/900.png) Immediate game-over
- ![](img/skulls/poison/900.png) Reduces the snake's length by one

#### Powerups
- ![](img/powerups/shield/900.png) One-time-use protection against skulls
- ![](img/powerups/ghost/900.png) Walk through skulls and yourself for 10 seconds
- ![](img/powerups/bomb/900.png) Clear the entire field from skulls

### Controls
- Set snake direction: Up/Down/Left/Right arrows
- Boost snake speed: LShift or RSHift
- Pause: Esc or Space
- Quit: Alt+F4 or Click 'X'

### Screenshot
![](img/screenshot.png)
