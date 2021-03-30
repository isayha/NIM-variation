# Team Project (NIM Variation)
# Python Source Code
# CPSC 482
# Derik Dreher, Sofia Jones, Isayha Raposo

# !!! = Notes for future development

from custom_io import *
from tabulate import tabulate # Requires package "tabulate" (pip install tabulate)

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

def cpu_plays(pile_count, piles, non_empty_pile_indexes):
    # Calculate NIM-sum
    nim_sum = 0
    for pile_size in piles:
        nim_sum ^= pile_size

    # If the NIM-sum is 0 prior to the CPU's turn, the CPU is losing, and will remove 1 object from an arbitrary non-empty pile
    # !!! There could be some strategy implemented here, not sure what yet
    # !!! e.g: Increasing the NIM-sum as much as possible may be a good strategy (would have to check math)
    if nim_sum == 0:
        for pile_index in non_empty_pile_indexes:
            return(1, pile_index)
    # If the NIM-sum is NOT 0 prior to the CPU's turn, the CPU can win as long as the NIM-sum is 0 at the END of it's turn
    else:
        # Strategy for states in which the non-empty pile count is greater than 2 (Keep the NIM-sum equal to 0)
        if len(non_empty_pile_indexes) > 2:
            for pile_index in non_empty_pile_indexes:
                nim_sum_xor_pile_size = nim_sum ^ piles[pile_index]
                if piles[pile_index] >= nim_sum_xor_pile_size:
                    reduction = piles[pile_index] - nim_sum_xor_pile_size
                    return(reduction, pile_index)
        # Strategy for states in which the non-empty pile count is less than or equal to 2
        else:
            # If the non-empty pile count is equal to 1, remove all but 1 object from the single non-empty pile, forcing the human player's hand
            if len(non_empty_pile_indexes) == 1:
                for pile_index in non_empty_pile_indexes:
                    reduction = piles[pile_index] - 1
                    return(reduction, pile_index)
            # If the non-empty pile count is equal to 2...
            else:
                # ...and 1 of the 2 non-empty piles contains just 1 object, remove all of the objects from the OPPOSITE pile, forcing the human player's hand
                if any(piles[pile_index] == 1 for pile_index in non_empty_pile_indexes):
                    for pile_index in non_empty_pile_indexes:
                        if piles[pile_index] > 1:
                            reduction = piles[pile_index]
                            return(reduction, pile_index)
                else:
                    # ...and none of the 2 non-empty piles contains just 1 object, ensure the 2 non-empty piles have an equal number of objects
                    # In other words, ensure the NIM-sum is 0 at the end of the turn
                    smallest_pile_size = min(pile_size for pile_size in piles if pile_size > 0)
                    for pile_index in non_empty_pile_indexes:
                        if piles[pile_index] != smallest_pile_size:
                            reduction = piles[pile_index] - smallest_pile_size
                            return(reduction, pile_index)

# Main function:
def main():
    # Game setup:
    # Get pile count:
    pile_count = get_user_int("Please enter the desired number of piles (> 1): ", 2, None)

    piles = []
    non_empty_pile_indexes = list(pile_index for pile_index in range(pile_count))

    # Get pile sizes:
    for pile_index in range(pile_count):
        pile_size = get_user_int("Please enter the desired number of objects in pile " + str(pile_index) + ": ", 1, None)
        piles.append(pile_size)

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
            reduction, pile_index = human_plays(pile_count, piles, non_empty_pile_indexes) # !!! If we don't have to pass any variables by adjusting scope, that would be ideal
            print_reduction("Human", reduction, pile_index)

        # CPU's turn logic
        else:
            reduction, pile_index = cpu_plays(pile_count, piles, non_empty_pile_indexes) # !!! If we don't have to pass any variables by adjusting scope, that would be ideal
            if reduction < 1: # !!! We need real strategy here lol
                reduction = 1
            print_reduction("CPU", reduction, pile_index)

        # Reduction logic:
        piles[pile_index] -= reduction
        if piles[pile_index] == 0:
            non_empty_pile_indexes.remove(pile_index) # !!! May have a hit on performance, could look into an alternative

        # Check if game is over:
        if not non_empty_pile_indexes: # Check if all piles are empty
            print("All piles are empty.")
            game_over = True
        elif len(non_empty_pile_indexes) == 3 and sum(piles[pile_index] for pile_index in non_empty_pile_indexes) == 6:
            if any(piles[pile_index] != 2 for pile_index in non_empty_pile_indexes):
                print("3 non-empty piles remain, containing exactly 1, 2, and 3 objects (respectively).")
            else:
                print("3 non-empty piles remain, each containing exactly 2 objects.")
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