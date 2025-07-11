#Q learning agent version 4.0 /  Πλέον σκέφτεται το refuel(uniform), μένουν κάποιες μικροδιορθώσεις σε αυτό το version + κάποια τεστ
import itertools #Για όλα τα δυνατά compinations i->j
import numpy as np
import math
import random
import time
start_time = time.time()

#Παράμετροι προβλήματος
maximum_fuel_tank_capacity = 150 #litre
average_diesel_consumption = 7  #km/l
reference_level = 0.25 * maximum_fuel_tank_capacity #litre
fuel_cost = 2 #euros/litre
epsilon= 0.05 #ε-greedy 
alpha= 0.4 #learning rate
gamma= 0.7 #discount factor
starting_state = 0 #state_0

# Ορίζω τα States / data input
# city  x-coordinate  y-coordinate
city_location = [[0, 565.0 , 575.0, fuel_cost],
                 [1, 25.0  , 185.0, fuel_cost],
                 [2, 345.0 , 750.0, fuel_cost],           #data by trelo kokori
                 [3, 945.0 , 685.0, fuel_cost],
                 [4, 845.0 , 655.0, fuel_cost],
                 [5, 880.0 , 660.0, fuel_cost],
                 [6, 25.0  , 230.0, fuel_cost],
                 [7, 525.0 , 1000.0, fuel_cost],
                 [8, 580.0 , 1175.0, fuel_cost],
                 [9, 650.0 , 1130.0, fuel_cost]]  

#Δημιουργία Q value Πίνακα
first_column = [row[0] for row in city_location] #Η πρώτη στήλη του πίνακα με τις πόλεις
number_of_nodes=max(first_column) + 1              #10 πόλεις στο παράδειγμα / βάζω το +1 γιατί παίρνω το max της πρώτης στήλης, άλλα ξεκινάει αυτή η στήλη από 0 και όχι από 1
q_values = np.zeros((number_of_nodes,number_of_nodes,2)) #Ο πίνακας με την αξία κάθε πιθανού action / 10x10x2 οταν βαλω και το refueling σαν option 


#Δημιουργία πίνακα available states
available_states_constant = [0]
for i in range(1,number_of_nodes):                  #ορίζω το available states = All states - starting state
    available_states_constant.append(i)                      #Το available_states_constant και avaulable_states είναι σε ολο τον κώδικο python lists.
available_states_constant.remove(starting_state)    

#Rewards
def get_distance(city_location_A,city_location_B) : 
    x_1 = city_location_A[1]
    x_2 = city_location_B[1]
    y_1 = city_location_A[2]                                            #Πρέπει να βρω την κλίμακα των αποστάσεων 
    y_2 = city_location_B[2]
    distance=math.sqrt( (x_1-x_2)*(x_1-x_2) + (y_1-y_2)*(y_1-y_2) )
    return distance

def get_cost_of_refueling(current_fuel) :
    cost_of_refueling = (maximum_fuel_tank_capacity - current_fuel)*fuel_cost
    return cost_of_refueling

def get_fuel_consumption(distance) :
    fuel_consumption = distance / average_diesel_consumption
    return fuel_consumption

def get_reward_function_6(distance , cost_of_refueling , fuel_consumption) :
    reward = - (distance + cost_of_refueling + fuel_consumption)
    return reward

def get_reward_function_3(distance) :
     reward = -distance
     return reward

def get_reward_function_2(cost_of_refueling):
    reward = -cost_of_refueling
    return reward

def get_reward_function_1(distance , cost_of_refueling):
    reward = - (distance + cost_of_refueling)
    return reward

#Important functions
def get_next_action (q_values,current_state,available_states : list,current_fuel) :          #*ΔΕΝ ΕΧΩ ΚΑΤΑΛΑΒΕΙ ΓΙΑΤΙ ΧΡΕΙΑΖΕΤΑΙ ΔΙΕΥΚΡΙΝΙΣΗ list ΣΤΟ ΟΡΙΣΜΑ ???????? 
    if current_fuel == maximum_fuel_tank_capacity :
        action_space = 1
        refuel_boolean = 0 
    else:                                                   #Αυτό το κομμάτι κώδικα αφαιρεί την όραση των action που περιλαμβάνουν refuel από τον agent όταν η βενζίνη είναι γεμάτη
        action_space = 2
        refuel_boolean = random.choice([0,1])  #Όπως διαλέγει τυχαία next state σύμφωνα με το ε-greedy, το ίδιο κάνει και για το refueling  

    if len(available_states) == 0 :
        next_state = starting_state
        available_states = []
        if current_fuel == maximum_fuel_tank_capacity :     #Αυτό το if το έβαλα γιατί αν είναι γεμάτο ούτε εδώ θέλω να τσεκάρει καν την επιλογή refuel
            refuel_boolean = 0
        else:
            if q_values[current_state][next_state][1] > q_values[current_state][next_state][0] :
                refuel_boolean = 1
            else :
                refuel_boolean = 0              #Το αν θα κάνει refuel ή όχι στο τελευταίο δρομολόγιο είναι δικιά του επιλιγή, άμα κρίνει ότι έχει μεγαλύτερη αξία το refuel θα το κάνει, αλλιώς όχι

    else :
        next_state = random.choice(available_states)               
        max_q_value = q_values[current_state][next_state][refuel_boolean]
        if random.random() > epsilon:
            for i in available_states :
                for j in range(0,action_space):         #Άμα το action_space είναι 1 σήμαινει ότι το ντεπόζιτο είναι γεμάτο και δεν τσεκάρει καν τις τιμές για refuel
                    if q_values[current_state][i][j] > max_q_value:               
                        max_q_value = q_values[current_state][i][j]                    
                        next_state = i                                              #Το function αυτό κάνει και την δουλειά της αφαίρεσης μίας πόλης που έχει ήδη επισκεφτεί ο agent από την λίστα προορισμών
                        refuel_boolean = j
        available_states.remove(next_state)                                    
    return next_state,available_states,refuel_boolean       

def get_best_solution () :                  #δοκιμή για best solution το ε = 0 και επανάληψη του loop με το οποίο έκανε train ο agent
    global epsilon          
    epsilon = -1
    current_state = starting_state
    current_fuel = maximum_fuel_tank_capacity
    total_distance = 0
    available_states = available_states_constant.copy()
    optimal_route = [starting_state]
    total_cost = 0 
    
    for i in range(1 , number_of_nodes + 1 ) :                       #Και εδώ μπήκε το +1 γιατί τρέχει μία ακόμα φορά εξαιτίας της επιστροφής στο starting state
        next_state , available_states , refuel_boolean = get_next_action(q_values , current_state , available_states , current_fuel) 
        distance = get_distance(city_location[current_state] , city_location[next_state])
        cost_of_refueling = 0                               #Γιατί για κάθε δρομολόγιο είναι διαφορετικό 

        if refuel_boolean == 1 :
                    cost_of_refueling = get_cost_of_refueling(current_fuel)
                    current_fuel = maximum_fuel_tank_capacity
                    optimal_route.append("refuel")
                    
        fuel_consumption = get_fuel_consumption(distance)
        current_fuel = current_fuel - fuel_consumption

        if current_fuel < 0 :
            cost_of_refueling = get_cost_of_refueling_punishment(current_fuel) 
            current_fuel = 0
            optimal_route.append("expensive refuel")
            cost_of_refueling = cost_of_refueling + get_cost_of_refueling(current_fuel) ######## ΑΠΟ ΕΔΩ ΚΑΙ ΚΑΤΩ 3 ΓΡΑΜΜΕΣ ΕΙΝΑΙ ΓΙΑ ΜΕΤΑ ΠΟΥ ΦΤΑΣΩ ΣΤΟ NEXT STATE
            current_fuel = maximum_fuel_tank_capacity ####
            optimal_route.append("refuel") ############### ΑΥΤΑ ΝΑ ΤΑ ΦΤΙΑΞΩ ΣΩΣΤΑ
            
        total_cost = total_cost + cost_of_refueling  
        total_distance = total_distance + distance
        optimal_route.append(next_state)                          #Για να έχω μία "εικόνα" για την διαδρομή που ακολουθεί
        current_state = next_state
    return total_distance, optimal_route, total_cost

def get_epsilon_linear_decay (episode_number , initial_epsilon , decay_rate , min_epsilon) :          #decay_rate = (initial_epsilon-min_epsilon)/episode_number
    global epsilon
    epsilon = max(min_epsilon, initial_epsilon - decay_rate * episode_number)                     #min_epsilon = 0, episode_number δίνεται αυτόματα από το loop
    decimal_places = len(str(1/total_episodes).split('.')[0])   #υπολογίζω πόσα δεκαδικά ψηφία θα χρειαστώ βάση τον συνολικό αριθμό επισοδείων / Να το βγάλω απέξω για να μην υπολογίζεται συνέχεια...
    epsilon = round(epsilon,decimal_places)                                                                          #και initial το επιλέγω εγώ, πχ 1
    return epsilon  

def get_epsilon_glie (initial_epsilon , episode_number) :
    global epsilon
    epsilon = initial_epsilon / episode_number                          #ΑΝΤΙ ΓΙΑ ΤΟ GLOBAL ΜΠΟΡΩ ΙΣΩΣ ΝΑ ΤΟ ΑΠΟΦΥΓΩ ΜΕ ΕΝΑ ΑΠΛΟ epsilon = get_epsilon_glie ΜΕΣΑ ΣΤΟ training
    return epsilon

def get_epsilon_logarithmic_decay (episode_number , total_episodes , initial_epsilon ) :               
    global epsilon
    decay_factor = math.log(total_episodes) / total_episodes
    epsilon = initial_epsilon * math.exp(-decay_factor * episode_number)
    return max(epsilon,0.0)

def get_cost_of_refueling_punishment (current_fuel) :
    cost_of_refueling = - current_fuel * fuel_cost * 5
    return cost_of_refueling



#Agent training / Q-Learing
total_episodes = 10000 * number_of_nodes
for episode_number in range(1 , total_episodes + 1):
    current_fuel = maximum_fuel_tank_capacity                           #ξεκινάω με φουλ ντεποζιτο χωρις να το πληρώσω
    current_state = starting_state
    total_distance = 0
    available_states = available_states_constant.copy() #Το βάζω αυτό εδώ γιατί διαφορετικά μετά το πρώτο επισόδειο δε θα ξαναγεμίσει η λίστα, μετά από κάθε επισόδειο θέλω να επανέρχεται       
    total_cost = 0
    #ΕΔΩ ΜΠΑΊΝΕΙ ΤΟ get_epsilon
    get_epsilon_logarithmic_decay (episode_number,total_episodes,1)
    for city_index in range(1 , number_of_nodes + 1) :               #Αυτό ίσως το αλλάξω σε for i in available_states / το +1 μπήκε γιατί πλέον τρέχει μία επιπλέον φορά για την επιστροφή στο starting state
        next_state , available_states , refuel_boolean = get_next_action(q_values , current_state , available_states , current_fuel)  #εδώ το get_next_action επιστρέφει tuple καθώς γυρνάει δύο τιμές, για αυτό τις αποθηκεύω αναλόγως
        distance = get_distance(city_location[current_state] , city_location[next_state])        
        cost_of_refueling = 0               #Γιατί σε κάθε δρομολόγιο είναι διαφορετικό, για αυτό αρχικοποιείται κάθε φορά 0

        if refuel_boolean == 1 :
            cost_of_refueling = get_cost_of_refueling(current_fuel)
            current_fuel = maximum_fuel_tank_capacity
        
        fuel_consumption = get_fuel_consumption(distance)
        current_fuel = current_fuel - fuel_consumption
        
        if current_fuel <= 0 :          #Βαζω και το ίσον μέσα γιατί δίνει expensive cost 0 και θέλω ΑΝ τύχει και φτάσει με ακριβώς 0 βενζίνη σε πόλη να φουλάρει φυσικά, ΚΑΘΟΔΗΓΩ κάπως τον agent
            cost_of_refueling = cost_of_refueling + get_cost_of_refueling_punishment(current_fuel) 
            current_fuel = 0 #Δηλαδή αν ήταν -30 το current το έχει και καλά συμπληρώσει πιο ακριβά ίσα ίσα για να φτάσει με 0 ως τον προορισμό
            cost_of_refueling = cost_of_refueling + get_cost_of_refueling(current_fuel) #επειδή θα φουλάρει αναγκαστικά εκεί που φτάνει με 0 βενζίνη
            current_fuel = maximum_fuel_tank_capacity
        
        total_distance = total_distance + distance
        total_cost = total_cost + cost_of_refueling
        q_values_of_available_states = []                     #αρχικοποιώ μια άδεια λίστα για να την γεμίζω με τα διαθεσιμα qvalues κάθε φορά,την βάζω εδώ μέσα για να ξανααδειάζει.
        
        for i in (available_states) :
           q_values_of_available_states.append(q_values[next_state][i][0])  #Αφού το state είναι available θα βάλω στον πίνακα την τιμή του Q και με refuel και χωρίς
           q_values_of_available_states.append(q_values[next_state][i][1])                                  
        
        if len(available_states) == 0 :                         #Αυτό το κομμάτι το βάζω γιατί όταν επιστρέφει από το τελευταίο state στο αρχικό ο πίνακας available states είναι άδειος και δε δουλευει το max()
            q_values_of_available_states = [0,0]                #στον τύπο του update. Το βάζω 0,0 γιατί ούτως ή άλλως η επιστροφή στο starting δεν έχει κάποιο μελλοντικό value. Αμα το βάλω 0 σκέτο δε δουλεύει το max()                                     
                                                                                                    
        #ΕΔΩ ΜΠΑΙΝΕΙ ΤΟ reward function 
        reward = get_reward_function_1(distance , cost_of_refueling)
        q_values[current_state][next_state][refuel_boolean] = (1 - alpha) * q_values[current_state][next_state][refuel_boolean] + alpha * (reward + gamma * max(q_values_of_available_states))
        current_state = next_state
    print(total_distance)
    



total_distance_of_bs , optimal_route , total_cost_of_bs= get_best_solution()

print("The best cost (min) is =", total_cost_of_bs, "TOTAL COST")                                                
print("The best solution is =" , total_distance_of_bs, "TOTAL DISTANCE" )
print("And the path followed to achieve this :" , optimal_route)
print("The algorithm runned for", time.time() - start_time, "seconds.")

