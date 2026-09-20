# Bachelor Side Projects

A collection of Python projects I made during my bachelor's degree. Each folder
is a separate desktop game or application.

## Projects

| Project                                                       | Description                                                               |
| ------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [Battle Brawlers Card Game](Battle%20Brawlers%20Card%20Game/) | A card battle game with computer-controlled opponents.                    |
| [Eyefox puzzle](Eyefox%20puzzle/)                             | A grid puzzle where changing a tile also changes its neighbours.          |
| [It adds up](It%20adds%20up/)                                 | An arithmetic game: combine numbers and operators to reach a target.      |
| [Minidex](Minidex/)                                           | A small Pokédex that reads Pokémon information and images from Poképédia. |
| [Taquin's Sudoku](Taquin%27s%20Sudoku/)                       | Sliding puzzles, Sudoku and a mode combining both.                        |

## Run a project

The projects use Python 3 and Pygame:

```bash
python3 -m pip install pygame
```

Minidex also uses Requests, Beautiful Soup and Python's Tkinter module:

```bash
python3 -m pip install requests beautifulsoup4
```

Tkinter must be available in your Python installation. Minidex needs an internet
connection and relies on the HTML structure of [Poképédia](https://www.pokepedia.fr/).

Run the command from the directory shown below, relative to this repository.
The working directory matters because the games load assets through relative paths.

| Project                   | Working directory               | Command               |
| ------------------------- | ------------------------------- | --------------------- |
| Battle Brawlers Card Game | `Battle Brawlers Card Game/src` | `python3 __main__.py` |
| Eyefox puzzle             | `Eyefox puzzle`                 | `python3 __main__.py` |
| It adds up                | `It adds up/src`                | `python3 __main__.py` |
| Minidex                   | `Minidex`                       | `python3 Minidex.py`  |
| Taquin's Sudoku           | `Taquin's Sudoku/src`           | `python3 __main__.py` |

For example, from the repository root:

```bash
cd "Eyefox puzzle"
python3 __main__.py
```

These projects do not have a shared dependency lockfile or automated test suite.

## Asset credits

The original credit notes remain alongside the assets:

- Battle Brawlers Card Game: [font](Battle%20Brawlers%20Card%20Game/assets/font/source.txt), [images](Battle%20Brawlers%20Card%20Game/assets/images/source.txt), [buttons](Battle%20Brawlers%20Card%20Game/assets/images/boutons/source.txt), [types](Battle%20Brawlers%20Card%20Game/assets/images/type/source.txt) and [sounds](Battle%20Brawlers%20Card%20Game/assets/sounds/source.txt).
- It adds up: [buttons](It%20adds%20up/assets/images/bouton/source.txt), [game images](It%20adds%20up/assets/images/game/source.txt) and [menu images](It%20adds%20up/assets/images/maintitle/source.txt).
- Taquin's Sudoku: [asset and music credits](Taquin%27s%20Sudoku/license.txt).

Minidex retrieves its Pokémon information and images from Poképédia.
