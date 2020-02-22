# PySnake
The classic arcade game Snake reimagined in Python using [Pygame](https://www.pygame.org/news) 🐍

## Run Game
**Note**: requires Python 3 with Pipenv

```bash
bash run_game.sh
```

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

### Reconfigure Player Name and Controls

#### Reconfigure Player
```bash
bash run_reconfig_player.sh
```

This will simply ask for a new player name, which is used for the highscores list. The default player name is 'Unnamed Player'. This can also be changed manually from the config file `config.ini`.

#### Reconfigure Controls
```bash
bash run_reconfig_controls.sh
```

Pay special attention to the console output (stdout) as it will guide you through the reconfiguration process. For each control, you may either keep the current button/s by pressing ESCAPE, or input a new list with at least one button by pressing the button/s one by one and pressing ENTER at the end to submit the list.

If something goes wrong with the reconfiguration, a `config_default.ini` file is included and can be used to replace a bad `config.ini`. 

### Highscores
The top 10 saved scores are stored in a highscores list. This can be printed by running:
```bash
bash run_highscores.sh
```

Scores can be saved from the game-over screen by pressing a "Save Score" button.

### Screenshot
![](img/screenshot.png)
