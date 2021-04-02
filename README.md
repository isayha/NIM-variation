# NIM-variation
A Python implementation of a variation of NIM. The exact rules of this variant are as follows:
- The game features `n` piles where `n` > 1
    - Each pile initially contains some arbitrary number of objects (> 0)
- Two players take turns removing `y` > 0 objects from a single pile `x` (both `y` and `x` are chosen by the player at each turn), where `y` <= the number of objects in `x`
- A player *loses* the game if, *after their turn*, any one of the following is true:
    - All `n` piles are empty
    - There exists 3 piles each with 2 objects remaining AND all other piles are empty
    - There exists 1 pile with 1 object remaining AND 1 other pile with 2 objects remaining AND a third distinct pile with 3 objects remaining AND all other piles are empty
    - (Optional) Some fourth game state that has been specified as a losing state is reached

## Instructions
### How to run
- To run the program, simply run `nim_variation.py`, either using the command `python` on the command line (while in the same directory as the source files), or the IDE of your choice
    - For reference, this program was written in Python 3.8.6 and 3.9 (due to having multiple contributors with differing versions), and requires the package `tabulate`, which can be installed using Pip by running `pip install tabulate`