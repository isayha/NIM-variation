# Team Project (NIM Variation)
# Python Source Code
# CPSC 482
# Derik Dreher, Sofia Jones, Isayha Raposo

from custom_io import *
from original_cpu import *
from better_cpu import *
from tabulate import tabulate # Requires package "tabulate" (pip install tabulate)
from collections import Counter

def print_reduction(player, reduction, pile_index):
    print(player + " removes " + str(reduction) + " object(s) from pile " + str(pile_index) + ":")

def human_plays(pile_count, piles, non_empty_pile_indexes):
    # Get selected pile:
    while True:
        pile_index = get_user_int("Please enter the index of the pile you would like to remove objects from: ", 0, pile_count - 1)
        if piles[pile_index] != 0:
            break
        print("ERROR: Pile " + str(pile_index) + " is empty.")

    # Get reduction:
    while True:
        reduction = get_user_int("Please enter the number of objects you would like to remove from pile " + str(pile_index) + ": ", 1, piles[pile_index])
        if reduction <= piles[pile_index]:
            break
        print("ERROR: Pile " + str(pile_index) + " currently only contains " + str(piles(pile_index)) + " objects.")

    return(reduction, pile_index)

# Blacklist (List of specified constrained/immediate-loss game states)
blacklist = {}
# Chen's constraints (hard-coded)
blacklist.update({frozenset(Counter([1,2,3]).items()) : False}) # False is an arbitrary value
blacklist.update({frozenset(Counter([2,2,2]).items()) : False}) # False is an arbitrary value

# Main function:
def main():
    # Game setup:
    # Get CPU player choice:
    print("Welcome to NIM-variation!")
    print("You can play against a simple (basic) CPU player, or a CPU player based on the minimax algorithm with memoization (advanced).")
    cpu_type = get_user_int("Please enter the desired CPU player type (0 for basic, 1 for advanced): ", 0, 1)

    # Get pile count:
    pile_count = get_user_int("Please enter the desired number of piles (> 1): ", 2, None)

    piles = []
    non_empty_pile_indexes = list(pile_index for pile_index in range(pile_count))

    # Get pile sizes:
    for pile_index in range(pile_count):
        pile_size = get_user_int("Please enter the desired number of objects in pile " + str(pile_index) + ": ", 1, None)
        piles.append(pile_size)

    # Get custom constraint:
    add_constraint = get_user_int("Would you like to add a custom constraint? (0 for N, 1 for Y): ", 0, 1)
    if add_constraint:
        # Get custom constraint pile count:
        constraint_pile_count = get_user_int("How many piles should the custom constraint involve? (NOT INCLUDING: Piles containing 0 objects): ", 1, pile_count)
        constraint = []
        for pile_index in range(constraint_pile_count):
            constraint.append(get_user_int("Please enter a pile size to add to the custom constraint: ", 1, None))
        blacklist.update({frozenset(Counter(constraint).items()) : False}) # False is an arbitrary value
    
    # Handle immediate loss:
    if frozenset(piles) in blacklist:
        print("WARNING: Custom constraint is equivalent to initial pile state.")
        print("Game may not function as expected (was this an accident?)...")

    # Get turn order:
    turn_order = get_user_int("Please enter the desired turn order (0 for human-first, 1 for cpu-first): ", 0, 1)
    cpus_turn = bool(turn_order) # For code readability

    # Game logic:
    game_over = False
    while not game_over:
        # Print status of piles
        print(tabulate(enumerate(piles), headers=["Pile Index:", "Objects in Pile:"]))

        # Human's turn logic
        if not cpus_turn:
            # Get reduction/pile index:
            reduction, pile_index = human_plays(pile_count, piles, non_empty_pile_indexes)
            print_reduction("Human", reduction, pile_index)

        # CPU's turn logic
        else:
            # Get reduction/pile index:
            if cpu_type == 0:
                reduction, pile_index = cpu_plays(piles, non_empty_pile_indexes, blacklist)
            if cpu_type == 1:
                reduction, pile_index = better_cpu_plays(piles, blacklist)
                if reduction is None and pile_index is None:
                    print("ERROR: Advanced CPU player could not find a move. Switching to Basic CPU player...")
            
            if reduction is None or pile_index is None:
                print("ERROR: CPU could not find move. Defaulting...")
                reduction = 1
                pile_index = non_empty_pile_indexes[0]

            print_reduction("CPU", reduction, pile_index)

        # Reduction logic:
        piles[pile_index] -= reduction
        if piles[pile_index] == 0:
            non_empty_pile_indexes.remove(pile_index)

        # Check if game is over:
        if not non_empty_pile_indexes: # Check if all piles are empty
            print("All piles are empty.")
            game_over = True
        elif frozenset(Counter([pile_size for pile_size in piles if pile_size > 0]).items()) in blacklist:
            print("A constrained/immediate-loss game state has been reached.")
            game_over = True
        else:
            cpus_turn = not(cpus_turn) # Rotate turns

    if not cpus_turn:
        print("CPU wins!")
    else:
        print("Human wins!")

# Driver:
if __name__ == "__main__":
    main()