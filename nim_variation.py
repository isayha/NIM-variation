# Team Project (NIM Variation)
# Python Source Code
# CPSC 482
# Derik Dreher, Sofia Jones, Isayha Raposo

from custom_io import *

# Main function:
def main():
    # Game setup:
    # Get pile count:
    valid_pile_count = False
    while not valid_pile_count:
        pile_count = get_user_int("Please enter the desired number of piles (> 1): ")
        if pile_count is None or pile_count < 2:
            print("ERROR: Invalid input.")
        else:
            valid_pile_count = True

    piles = []
    non_empty_pile_count = pile_count

    # Get pile sizes:
    for selected_pile in range(pile_count):
        valid_pile_size = False
        while not valid_pile_size:
            pile_size = get_user_int("Please enter the desired size of pile " + str(selected_pile) + ": ")
            if pile_size is None or pile_size < 1:
                print("ERROR: Invalid input.")
            else:
                piles.append(pile_size)
                valid_pile_size = True

    print(piles) # TEST ONLY REMOVE LATER

    # Get turn order:
    valid_selection = False
    while not valid_selection:
        turn_order = get_user_int("Please enter the desired turn order (0 for human-first, 1 for cpu-first): ")
        if turn_order is None or (turn_order != 0 and turn_order != 1):
            print("ERROR: Invalid input.")
        else:
            valid_selection = True

    # Game logic:
    game_over = False
    while not game_over:
        print("Piles: " + str(piles))
        print("Index: " + str(list(index for index in range(len(piles)))))

        if turn_order == 0: # human's turn

            # Get selected pile:
            valid_selection = False
            while not valid_selection:
                selected_pile = get_user_int("Please enter the index of the pile you would like to take from: ")
                if selected_pile is None or selected_pile < 0 or selected_pile >= pile_count:
                    print("ERROR: Invalid input.")
                elif piles[selected_pile] == 0:
                    print("ERROR: Pile " + str(selected_pile) + "is empty.")
                else:
                    valid_selection = True

            # Get reduction:
            valid_selection = False
            while not valid_selection:
                reduction = get_user_int("Please enter the number of objects you would like to remove from pile " + str(selected_pile) + ": ")
                if reduction is None or reduction < 1:
                    print("ERROR: Invalid input.")
                elif reduction > piles[selected_pile]:
                    print("ERROR: Pile " + str(selected_pile) + "currently only contains " + str(piles(selected_pile)) + " objects.")
                else:
                    valid_selection = True

            piles[selected_pile] -= reduction
            if piles[selected_pile] == 0:
                non_empty_pile_count -= 1
        
        if turn_order == 1: # cpu's turn
            nim_sum = 0
            for pile_size in piles:
                nim_sum ^= pile_size
            if nim_sum == 0:
                print("CPU is losing.") # TEST ONLY REMOVE LASTER
                for pile in range(len(piles)):
                    if piles[pile] != 0:
                        print("CPU removes 1 object(s) from pile " + str(pile) + ".")
                        piles[pile] -= 1
                        if piles[pile] == 0:
                            non_empty_pile_count -= 1
                        break
            else:
                if non_empty_pile_count > 2:
                    move_found = False
                    while not move_found:
                        for pile in range(len(piles)):
                            nim_sum_xor_pile_size = nim_sum ^ piles[pile]
                            if piles[pile] >= nim_sum_xor_pile_size:
                                print("CPU removes " + str(piles[pile] - nim_sum_xor_pile_size) + " object(s) from pile " + str(pile) + ".")
                                piles[pile] -= piles[pile] - nim_sum_xor_pile_size
                                if piles[pile] == 0:
                                    non_empty_pile_count -= 1
                                move_found = True
                                break
                        nim_sum -= 1
                        
                else:
                    if non_empty_pile_count == 1:
                        for pile in range(len(piles)):
                            if piles[pile] > 0:
                                print("CPU removes " + str(piles[pile] - 1) + " objects from pile " + str(pile) + ".")
                                piles[pile] = 1
                                break
                    else:
                        if any(pile_size == 1 for pile, pile_size in enumerate(piles)):
                            for pile in range(len(piles)):
                                if piles[pile] > 1:
                                    print("CPU removes " + str(piles[pile]) + " object(s) from pile " + str(pile) + ".")
                                    piles[pile] = 0
                                    non_empty_pile_count += 1
                                    break
                        else:
                            smallest_pile = min(pile for pile in piles if pile > 0)
                            for pile in range(len(piles)):
                                if piles[pile] != smallest_pile:
                                    print("CPU removes " + str(piles[pile] - smallest_pile) + " object(s) from pile " + str(pile) + ".")
                                    piles[pile] = smallest_pile
                                    break


                    
        
        # Check if game is over:
        if all(pile_size == 0 for pile_size in piles): # Check if all piles are empty
            print("All piles are empty.")
            game_over = True
        # Add logic for Chen's constraints HERE as an ELIF
        else:
            turn_order = not(turn_order) # Rotate turns

    if turn_order == 0:
        print("CPU wins!")
    else:
        print("Human wins!")

# Driver:
if __name__ == "__main__":
    main()