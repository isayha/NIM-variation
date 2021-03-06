import math
from collections import Counter

# Our best and brightest CPU player, based on the minimax algorithm (a game/search tree) with alpha-beta pruning and memoization (a hash table/dictionary)

# Generate (immediate) child nodes of parent node
def generate_children(parent):
    children = []
    for pile_index in range(len(parent)):
        for reduction in range(1, parent[pile_index] + 1):
            temp_parent = parent.copy()
            temp_parent[pile_index] -= reduction
            children.append(temp_parent)
    return children if len(children) > 0 else None

# Check if state is a game over state
def game_over(state, blacklist):
    # Check if state is a blacklisted state
    non_zero_state = state.copy()
    non_zero_state = [pile_size for pile_size in state if pile_size > 0]
    if frozenset(Counter(non_zero_state).items()) in blacklist:
        return True
    # Check if all piles in state are empty
    if not any(pile_size != 0 for pile_size in state):
        return True
    return False

cache = {}
choices = []
# Yields optimal moves (if they exist) for the computer player using the minimax algorithm with alpha-beta pruning and memoization
def minimax(state, iteration, cpus_turn, blacklist, alpha, beta):
    if game_over(state, blacklist):
        if cpus_turn:
            return 1
        else:
            return -1
    if cpus_turn:
        children = generate_children(state)
        max_eval = -math.inf
        for child in children:
            non_zero_copy = child.copy()
            non_zero_copy = [pile_size for pile_size in non_zero_copy if pile_size > 0]
            if (frozenset(Counter(non_zero_copy).items()), cpus_turn) in cache:
                eval = cache.get((frozenset(Counter(non_zero_copy).items()), cpus_turn))
            else:
                eval = minimax(child.copy(), iteration + 1, False, blacklist, alpha, beta)
                cache.update({(frozenset(Counter(non_zero_copy).items()), cpus_turn) : eval})
            max_eval = max(max_eval, eval)
            alpha = max(alpha, max_eval)
            if alpha >= beta:
                break
            if iteration == 0 and eval == 1:
                choices.append(child)
        return max_eval
    else:
        children = generate_children(state)
        min_eval = math.inf
        for child in children:
            non_zero_copy = child.copy()
            non_zero_copy = [pile_size for pile_size in non_zero_copy if pile_size > 0]
            if (frozenset(Counter(non_zero_copy).items()), cpus_turn) in cache:
                eval = cache.get((frozenset(Counter(non_zero_copy).items()), cpus_turn))
            else:
                eval = minimax(child.copy(), iteration + 1, True, blacklist, alpha, beta)
                cache.update({(frozenset(Counter(non_zero_copy).items()), cpus_turn) : eval})
            min_eval = min(min_eval, eval)
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
            if iteration == 0 and eval == 1:
                choices.append(child)
        return min_eval

# Handles interfacing between the driver logic and the minimax function above
def better_cpu_plays(piles, blacklist):
    minimax(piles, 0, True, blacklist, -math.inf, math.inf)
    if len(choices) > 0:
        choice = choices[0]
        for pile_index in range (0, len(choice)):
            if piles[pile_index] > choice[pile_index]:
                reduction = piles[pile_index] - choice[pile_index]
                return(reduction, pile_index)
    return(None, None)