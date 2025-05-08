def player(prev_play, opponent_history=[], my_history=[], patterns={}):
    if not prev_play:
        opponent_history.clear()
        my_history.clear()
        patterns.clear()
    else:
        opponent_history.append(prev_play)

    counter = {'P': 'S', 'R': 'P', 'S': 'R'}
    
    # Strategy 1: Detect Quincy's pattern (R, R, P, P, S)
    if len(opponent_history) >= 5:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        is_quincy = all(
            opponent_history[i] == quincy_pattern[i % 5]
            for i in range(-5, 0)
        )
        if is_quincy:
            next_move = quincy_pattern[len(opponent_history) % 5]
            guess = counter[next_move]
            my_history.append(guess)
            return guess

    # Strategy 2: Specialized Abbey counter (Markov chain with 3-move memory)
    if len(opponent_history) >= 6:
        # Update pattern database
        last_three = "".join(opponent_history[-3:])
        if len(last_three) == 3:
            pattern_key = last_three[:2]
            next_move = last_three[2]
            if pattern_key not in patterns:
                patterns[pattern_key] = {'R': 0, 'P': 0, 'S': 0}
            patterns[pattern_key][next_move] += 1
        
        # Predict Abbey's move using last 2 moves
        if len(opponent_history) >= 2:
            last_two = "".join(opponent_history[-2:])
            if last_two in patterns:
                prediction = max(patterns[last_two], key=patterns[last_two].get)
                guess = counter[prediction]
                my_history.append(guess)
                return guess

    # Strategy 3: Counter Kris (who counters your last move)
    if len(my_history) >= 3:
        is_kris = all(
            opponent_history[i] == counter.get(my_history[i-1] if i > 0 else "R", "R")
            for i in range(-3, 0)
        )
        if is_kris:
            predicted_kris_move = counter[my_history[-1]]
            guess = counter[predicted_kris_move]
            my_history.append(guess)
            return guess

    # Strategy 4: Counter Mrugesh (counts your frequent moves)
    if len(my_history) >= 10:
        last_ten = my_history[-10:]
        freq = max(set(last_ten), key=last_ten.count)
        mrugesh_move = counter[freq]
        guess = counter[mrugesh_move]
        my_history.append(guess)
        return guess

    # Fallback: Rotate moves with occasional randomness
    if not my_history:
        guess = "P"
    else:
        rotate = ["R", "P", "S"]
        last_index = rotate.index(my_history[-1]) if my_history[-1] in rotate else 0
        guess = rotate[(last_index + 1) % 3]
    
    my_history.append(guess)
    return guess