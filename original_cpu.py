from collections import Counter

# Our original CPU player, prior to creating a minimax-based CPU player (better_cpu.py)
def cpu_plays(piles, non_empty_pile_indexes, blacklist):
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
            # Special case strategy (with the exception of a single pile, all non-empty piles contain exactly 1 object)
            piles_of_size_one = 0
            flag = -1 # -1 is arbitrary/an identifiably invalid pile_index value
            for pile_index in non_empty_pile_indexes:
                if piles[pile_index] != 1:
                    if flag == -1:
                        flag = pile_index
                    else:
                        flag = -1
                        break
                else:
                    piles_of_size_one += 1
            if flag != -1:
                if piles_of_size_one % 2 == 0:
                    reduction = piles[flag] - 1
                else:
                    reduction = piles[flag]
                return(reduction, flag)
            else:
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
        if best_move is not None and reduction != 0:
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