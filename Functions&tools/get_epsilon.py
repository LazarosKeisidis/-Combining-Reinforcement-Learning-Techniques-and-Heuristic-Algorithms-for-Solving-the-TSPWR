import math

# ε-greedy με decay
def get_epsilon_linear_decay (episode_number , initial_epsilon , decay_rate , min_epsilon , total_episodes) :         
    epsilon = max(min_epsilon, initial_epsilon - decay_rate * episode_number)                    
    decimal_places = len(str(1/total_episodes).split('.')[0])   
    epsilon = round(epsilon,decimal_places)                                                                          
    return epsilon  

def get_epsilon_glie (initial_epsilon , episode_number) :
    epsilon = initial_epsilon / episode_number                          
    return epsilon

def get_epsilon_logarithmic_decay (episode_number , total_episodes , initial_epsilon ) :               
    decay_factor = math.log(total_episodes) / total_episodes
    epsilon = initial_epsilon * math.exp(-decay_factor * episode_number)
    return max(epsilon,0.0)

def get_epsilon_logarithmic_decay2 (episode_number , total_episodes , initial_epsilon ) :               
    decay_factor = math.log(total_episodes) / total_episodes
    epsilon = initial_epsilon * math.exp(-decay_factor * episode_number)
    return max(epsilon,0.05)