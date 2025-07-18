# Reward functions
def get_reward_function_1(distance , cost_of_refueling):
    reward = - (distance + cost_of_refueling)
    return reward

def get_reward_function_2(cost_of_refueling):
    reward = -cost_of_refueling
    return reward

def get_reward_function_3(distance) :
     reward = -distance
     return reward

def get_reward_function_6(distance , cost_of_refueling , fuel_consumption) :
    reward = - (distance + cost_of_refueling + fuel_consumption)
    return reward