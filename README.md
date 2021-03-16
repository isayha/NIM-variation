# NIM-variation
A Python implementation of a variation of NIM. The exact rules of this variant are as follows:
- The game features `n` piles where `n` > 1
    - Each pile contains an arbitrary number of objects
- Two players take turns removing `y` > 0 objects from a single pile `x` (both `y` and `x` are chosen by the player at each turn)
- A player *loses* the game if, after their turn, any one of the following is true:
    - All `n` piles are empty
    - There exists 3 piles each with 2 objects remaining AND all other piles are empty
    - There exists 1 pile with 1 object remaining AND 1 other pile with 2 objects remaining AND a third distinct pile with 3 objects remaining AND all other piles are empty

## Instructions
### How to run
- To run the program, simply run `nim_variation.py`, either using the command `python` on the command line (while in the same directory as the source files), or the IDE of your choice