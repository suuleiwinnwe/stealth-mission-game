# Mochi's Jump Quest

A 2D platformer made with Python and Pygame. Guide Mochi, a small cute cat-bunny, from the start to the goal flag, jumping over pits, saws, and spikes.

## Run it in VS Code

1. Install Python 3.10 or newer from python.org (tick "Add Python to PATH").
2. Open this folder in VS Code (File > Open Folder).
3. Open the terminal (Ctrl + `) and install pygame:
   ```
   pip install -r requirements.txt
   ```
4. Run the game:
   ```
   python main.py
   ```
   Or open `main.py` and press the Run button at the top right.

## Controls

| Key | Action |
|---|---|
| Left / Right or A / D | Move |
| Space, Up or W | Jump (hold for a higher jump) |
| R | Restart the level |
| N | Next level (after winning) |
| Esc | Back to the title screen |

## How to play

- Reach the pink goal flag at the end of the level.
- Saws and spikes cost one heart. Falling into a pit also costs one heart.
- You start with 3 hearts. Red hearts in the level give you one back (max 5).
- Gray flags are checkpoints. Touch one and you respawn there instead of at the start.
- Coins are optional and count toward your final stats.

## Project files

| File | What it does |
|---|---|
| `main.py` | Game loop, title screen, HUD, win and game over screens |
| `player.py` | `Player` class: movement, jumping, collisions, animation |
| `level.py` | `Level` class: turns a text layout into tiles, saws, spikes, coins, checkpoints, and the goal |
| `sprites.py` | All art, drawn with code (Mochi, stone tiles, saws, spikes, coins, hearts, flags) |
| `background.py` | Scrolling mountains, hills, bushes, and clouds |
| `settings.py` | Jump height, speed, gravity, lives (change these to tune difficulty) |
| `levels/level1.py` | Level 1 layout |
| `levels/level_template.py` | Starter file for a new level |

## Building a level (for each teammate)

Each level is a list of text rows. One character is one 50 x 50 tile.

| Character | Meaning |
|---|---|
| `#` | Stone block |
| `.` | Empty air |
| `S` | Start position (exactly one) |
| `F` | Goal flag (required) |
| `*` | Spinning saw |
| `^` | Spikes |
| `o` | Coin |
| `H` | Extra heart |
| `C` | Checkpoint |

Steps:

1. Copy `levels/level_template.py` to `levels/level2.py` (use your own number or name).
2. Change `NAME` and edit `LAYOUT`. Rows can be as long as you want, so levels can be short or long. Add more rows for a taller level.
3. Register it in `levels/__init__.py`:
   ```python
   from . import level1, level2
   LEVELS = [level1, level2]
   ```
4. Run the game and press the level's number on the title screen to test it.

Design tips:

- Mochi can jump about 3 tiles high and 4 tiles far, so keep gaps 3 tiles wide or less and steps up 3 tiles high or less.
- Give players a safe landing space before a hazard. Don't put spikes right where a drop lands.
- Put a checkpoint before each hard section.
- To make a level harder, add more saws, narrower platforms, and longer gaps.

## Using GitHub with the team

- Each teammate works on their own branch (for example `level-2-sam`) and only edits their own `levels/levelN.py`. This avoids merge conflicts.
- One person owns `levels/__init__.py` (the list of levels) and merges the pull requests.
- Commit small and often with clear messages, like "Add saw section to level 2".
