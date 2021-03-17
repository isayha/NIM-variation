# Team Project (NIM Variation)
# Python Source Code
# CPSC 482
# Derik Dreher, Sofia Jones, Isayha Raposo

# !!! = Notes for future development

from custom_io import *
from tabulate import tabulate # Requires package "tabulate" (pip install tabulate)

# Main function:
def main():
    # Game setup:
    # Get pile count:
    pile_count = get_user_int("Please enter the desired number of piles (> 1): ", 2, None)

    piles = []
    non_empty_pile_indexes = list(pile_index for pile_index in range(pile_count))
    print(non_empty_pile_indexes) # TEST ONLY

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
        print(tabulate(enumerate(piles), headers=["Pile Index:", "Objects in Pile:"]))

        # Human's turn logic
        if not cpus_turn:
            # Get selected pile:
            while True:
                pile_index = get_user_int("Please enter the index of the pile you would like to remove objects from: ", 0, pile_count - 1)
                if piles[pile_index] != 0:
                    break
                print("ERROR: Pile " + str(pile_index) + "is empty.")

            # Get reduction:
            while True:
                reduction = get_user_int("Please enter the number of objects you would like to remove from pile " + str(pile_index) + ": ", 1, piles[pile_index])
                if reduction <= piles[pile_index]:
                    break
                print("ERROR: Pile " + str(pile_index) + "currently only contains " + str(piles(pile_index)) + " objects.")

            # Reduction logic:
            print("You remove " + str(reduction) + " object(s) from pile " + str(pile_index) + ".")
            piles[pile_index] -= reduction
            if piles[pile_index] == 0:
                non_empty_pile_indexes.remove(pile_index) # !!! May have a hit on performance, could look into an alternative
        
        # CPU's turn logic
        if cpus_turn:
            # Calculate NIM-sum
            nim_sum = 0
            for pile_size in piles:
                nim_sum ^= pile_size

            # If the NIM-sum is 0 prior to the CPU's turn, the CPU is losing, and will remove 1 object from an arbitrary non-empty pile
            # !!! There could be some strategy implemented here, not sure what yet
            if nim_sum == 0:
                for pile_index in non_empty_pile_indexes:
                    print("CPU removes 1 object(s) from pile " + str(pile_index) + ".")
                    piles[pile_index] -= 1
                    if piles[pile_index] == 0:
                        non_empty_pile_indexes.remove(pile_index) # !!! May have a hit on performance, could look into an alternative
                    break
            else:
                # If the NIM-sum is NOT 0 prior to the CPU's turn, the CPU can win as long as the NIM-sum is 0 at the END of it's turn
                if len(non_empty_pile_indexes) > 2:
                    for pile_index in non_empty_pile_indexes:
                        nim_sum_xor_pile_size = nim_sum ^ piles[pile_index]
                        if piles[pile_index] >= nim_sum_xor_pile_size:
                            print("CPU removes " + str(piles[pile_index] - nim_sum_xor_pile_size) + " object(s) from pile " + str(pile_index) + ".")
                            piles[pile_index] -= piles[pile_index] - nim_sum_xor_pile_size
                            if piles[pile_index] == 0:
                                non_empty_pile_indexes.remove(pile_index) # !!! May have a hit on performance, could look into an alternative
                            break
                else:
                    if len(non_empty_pile_indexes) == 1:
                        for pile_index in non_empty_pile_indexes:
                            print("CPU removes " + str(piles[pile_index] - 1) + " object(s) from pile " + str(pile_index) + ".")
                            piles[pile_index] = 1
                            break
                    else:
                        if any(piles[pile_index] == 1 for pile_index in non_empty_pile_indexes):
                            for pile_index in non_empty_pile_indexes:
                                if piles[pile_index] > 1:
                                    print("CPU removes " + str(piles[pile_index]) + " object(s) from pile " + str(pile_index) + ".")
                                    piles[pile_index] = 0
                                    non_empty_pile_indexes.remove(pile_index) # !!! May have a hit on performance, could look into an alternative
                                    break
                        else:
                            smallest_pile_size = min(pile_size for pile_size in piles if pile_size > 0)
                            for pile_index in non_empty_pile_indexes:
                                if piles[pile_index] != smallest_pile_size:
                                    print("CPU removes " + str(piles[pile_index] - (piles[pile_index] - smallest_pile_size)) + " object(s) from pile " + str(pile_index) + ".")
                                    piles[pile_index] = smallest_pile_size
                                    break
        
        # Check if game is over:
        if not non_empty_pile_indexes: # Check if all piles are empty
            print("All piles are empty.")
            game_over = True
        # !!! Add logic for Chen's constraints HERE as an ELIF
        else:
            cpus_turn = not(cpus_turn) # Rotate turns

    if not cpus_turn:
        print("CPU wins!")
    else:
        print("Human wins!")

# Driver:
if __name__ == "__main__":
    main()