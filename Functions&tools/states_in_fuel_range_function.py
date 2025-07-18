maximum_fuel_tank_capacity = 150
average_diesel_consumption = 7

def get_states_in_fuel_range (current_state, route , distance_matrix) :
        max_distance = maximum_fuel_tank_capacity * average_diesel_consumption
        states_in_fuel_range = []
        next_state = route[route.index(current_state)+1]
        total_distance = distance_matrix[current_state][next_state]
        while total_distance < max_distance :
            states_in_fuel_range.append(next_state)
            current_state = next_state
            if current_state == route[0] :
                break
            else:
                next_state = route[route.index(current_state)+1]
                total_distance += distance_matrix[current_state][next_state]
        return states_in_fuel_range