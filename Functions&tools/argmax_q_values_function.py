import random
# returns max q value of given array

def argmax_q_values (q_values , available_states , next_state , starting_state) :        
    if len(available_states) == 0 :
        max_q_value = max(q_values[next_state][starting_state][0],q_values[next_state][starting_state][1])
    else :    
        i = random.choice(available_states)
        j = random.choice([0, 1])
        max_q_value = q_values[next_state][i][j]
            
        for i in available_states :
            for j in range(0,2) :
                if q_values[next_state][i][j] > max_q_value :
                    max_q_value = q_values[next_state][i][j]
    
    if next_state == starting_state :
        max_q_value = 0                     
    
    return max_q_value