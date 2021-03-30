# Team Project (NIM Variation)
# Python Source Code
# CPSC 482
# Derik Dreher, Sofia Jones, Isayha Raposo

from custom_io import *
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

def cpu_plays(piles, non_empty_pile_indexes):
    # Used in cases where any and all moves that change the NIM-sum to 0 also put the CPU player into a constrained/immediate-loss game state
    flagged_state = None

    # Calculate NIM-sum
    nim_sum = 0
    for pile_index in non_empty_pile_indexes:
        nim_sum ^= piles[pile_index]

    # If the NIM-sum is NOT 0 prior to the CPU's turn, the CPU can win as long as the NIM-sum is 0 at the END of it's turn
    if nim_sum != 0:
        # Strategy for states in which the non-empty pile count is greater than 2 (Keep the NIM-sum equal to 0)
        if len(non_empty_pile_indexes) > 2:
            for pile_index in non_empty_pile_indexes:
                nim_sum_xor_pile_size = nim_sum ^ piles[pile_index]
                if piles[pile_index] >= nim_sum_xor_pile_size:
                    reduction = piles[pile_index] - nim_sum_xor_pile_size
                    # Check for constrained/immediate-loss game states
                    temp_piles = piles.copy()
                    temp_piles[pile_index] -= reduction
                    temp_piles = [pile_size for pile_size in temp_piles if pile_size > 0]
                    if frozenset(Counter(temp_piles).items()) in blacklist:
                        flagged_state = temp_piles
                        continue
                    else:
                        return(reduction, pile_index)
        # Strategy for states in which the non-empty pile count is less than or equal to 2
        else:
            # If the non-empty pile count is equal to 1, remove all but 1 object from the single non-empty pile, forcing the human player's hand
            if len(non_empty_pile_indexes) == 1:
                for pile_index in non_empty_pile_indexes:
                    reduction = piles[pile_index] - 1
                    # If the non-empty pile remaining contains more than 1 object...
                    if reduction != 0:
                        # Check for constrained/immediate-loss game states
                        temp_piles = piles.copy()
                        temp_piles[pile_index] -= reduction
                        temp_piles = [pile_size for pile_size in temp_piles if pile_size > 0]
                        if frozenset(Counter(temp_piles).items()) in blacklist:
                            flagged_state = temp_piles
                            break
                        else:
                            return(reduction, pile_index)
                    # ...else forfeit
                    else:
                        return(1, pile_index)
            # If the non-empty pile count is equal to 2...
            else:
                # ...and 1 of the 2 non-empty piles contains just 1 object, remove all of the objects from the OPPOSITE pile, forcing the human player's hand
                if any(piles[pile_index] == 1 for pile_index in non_empty_pile_indexes):
                    for pile_index in non_empty_pile_indexes:
                        if piles[pile_index] > 1:
                            reduction = piles[pile_index]
                            # Check for constrained/immediate-loss game states
                            temp_piles = piles.copy()
                            temp_piles[pile_index] -= reduction
                            temp_piles = [pile_size for pile_size in temp_piles if pile_size > 0]
                            if frozenset(Counter(temp_piles).items()) in blacklist:
                                flagged_state = temp_piles
                                break
                            else:
                                return(reduction, pile_index)
                else:
                    # ...and none of the 2 non-empty piles contains just 1 object, ensure the 2 non-empty piles have an equal number of objects
                    # In other words, ensure the NIM-sum is 0 at the end of the turn
                    smallest_pile_size = min(pile_size for pile_size in piles if pile_size > 0)
                    for pile_index in non_empty_pile_indexes:
                        if piles[pile_index] != smallest_pile_size:
                            reduction = piles[pile_index] - smallest_pile_size
                            # Check for constrained/immediate-loss game states
                            temp_piles = piles.copy()
                            temp_piles[pile_index] -= reduction
                            temp_piles = [pile_size for pile_size in temp_piles if pile_size > 0]
                            if frozenset(Counter(temp_piles).items()) in blacklist:
                                flagged_state = temp_piles
                                break
                            else:
                                return(reduction, pile_index)
    if flagged_state is not None:
        # Strategy for cases in which any and all moves that change the NIM-sum to 0 also put the CPU player into a constrained/immediate-loss game state
        # If possible, the move chosen should force the other player into the same situation on their next turn, if possible

        print("CPU: No move leading to a winning state found... Checking other possibilities.")
        best_move = None
        # High NIM-sums are more likely to make it difficult to reduce the NIM-sum to 0 on the next turn
        # e.g.: A high NIM-sum is more likely to mean > 1 pile must be reduced to get the NIM-sum to 0
        best_move_nim_sum = 0
        # High pile counts are more likely to make it difficult to reduce the NIM-sum to 0 on the next turn, for similar reasons
        best_move_non_empty_pile_count = 0

        future_sum = sum(flagged_state)
        current_sum = sum(piles)
        reduction = (current_sum - future_sum) - 1

        for pile_index in non_empty_pile_indexes:
            if piles[pile_index] >= reduction:
                # Check for constrained/immediate-loss game states
                temp_piles = piles.copy()
                temp_piles[pile_index] -= reduction
                temp_piles = [pile_size for pile_size in temp_piles if pile_size > 0]
                if frozenset(Counter(temp_piles).items()) not in blacklist:
                    temp_nim_sum = 0
                    temp_non_empty_pile_count = 0
                    for pile in temp_piles:
                        temp_nim_sum ^= pile
                        temp_non_empty_pile_count += 1
                    if best_move_nim_sum <= temp_nim_sum and best_move_non_empty_pile_count <= temp_non_empty_pile_count:
                        best_move = (reduction, pile_index)
                        best_move_nim_sum = temp_nim_sum
                        best_move_non_empty_pile_count = temp_non_empty_pile_count
        if best_move is not None:
            return(best_move)

    # If no strategy is found, perform some arbitrary move that doesn't lead to an immediate-loss game state
    for pile_index in non_empty_pile_indexes:
        for reduction in range(1, piles[pile_index] + 1):
            temp_piles = piles.copy()
            temp_piles[pile_index] -= reduction
            temp_piles = [pile_size for pile_size in temp_piles if pile_size > 0]
            if frozenset(Counter(temp_piles).items()) not in blacklist:
                return(reduction, pile_index)

    # Default return for safety (handled externally)
    return(None, None)

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
        print("Ignoring custom constraint (was this an accident?)...")

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
            # Get reduction/pile index:
            reduction, pile_index = cpu_plays(piles, non_empty_pile_indexes) # !!! If we don't have to pass any variables by adjusting scope, that would be ideal
            
            if reduction is None or pile_index is None:
                print("ERROR: CPU could not find move. Defaulting...")
                reduction = 1
                pile_index = non_empty_pile_indexes[0]

            print_reduction("CPU", reduction, pile_index)

        # Reduction logic:
        piles[pile_index] -= reduction
        if piles[pile_index] == 0:
            non_empty_pile_indexes.remove(pile_index) # !!! May have a hit on performance, could look into an alternative

        # Check if game is over:
        if not non_empty_pile_indexes: # Check if all piles are empty
            print("All piles are empty.")
            game_over = True
        elif frozenset(Counter([pile_size for pile_size in piles if pile_size > 0]).items()) in blacklist:
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