maximum_fuel_tank_capacity = 150 
average_diesel_consumption = 7  
fuel_cost = 2

# refueling functions
def get_cost_of_refueling(current_fuel , current_state , city_data) :
    cost_of_refueling = (maximum_fuel_tank_capacity - current_fuel)*city_data[current_state][3] 
    return cost_of_refueling

def get_fuel_consumption(distance) :
    fuel_consumption = distance / average_diesel_consumption
    return fuel_consumption

def get_cost_of_refueling_punishment (current_fuel) :
    cost_of_refueling = - current_fuel * fuel_cost * 10
    return cost_of_refueling

def get_cost_of_punishment_2() :
    cost_of_punishment = 200
    return cost_of_punishment
