import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os
from matplotlib.patches import FancyArrowPatch
import re

save_dir = "random save dir on ur pc"

# MAP Functions
def map_no_route_Bahia30D(city_data , title1):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    # Create a figure with two subplots
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    ax1.scatter(x_coords, y_coords, marker='o', color='r', s=30, label='Cities')
    for city, y, x in city_data:
        if city == 4 :
            ax1.text(x, y+0.1, str(int(city)), fontsize=9, ha='center', va='center')
        else :
            ax1.text(x, y-0.12, str(int(city)), fontsize=9, ha='center', va='center')
    ax1.legend(loc='upper left', fontsize=12)
    
    # Customize plot (optional)
    ax1.set_title(title1)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

    return

def map_Bahia30D(city_data , cost_1 , distance_1 , cost_2 , distance_2 , route1 , refuel_states1 , exp_refuel_states1 , route2 , refuel_states2 , exp_refuel_states2 , title1 ,title2 , filename_suffix):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    #min distance for arrows
    min_distance = math.sqrt( (x_coords[12]-x_coords[27])*(x_coords[12]-x_coords[27]) + (y_coords[12]-y_coords[27])*(y_coords[12]-y_coords[27]) )

    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    axs[0].scatter(x_coords, y_coords, marker='o', color='r', s=30, label='No Refuel Cities' ,zorder=2)
    axs[0].scatter(x_coords[route1[0]], y_coords[route1[0]], marker='o', color='b', s=30, label='Starting City',zorder=2)
    counter = 0         #Το counter το έβαλα ως πατέντα για να μην εμφανίζεται στο legend πολλές φορές το refuel states symbol 
    for idx in refuel_states1:
        if counter < len(refuel_states1) - 1 :
            axs[0].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=30, zorder=2)
            counter += 1
        else :
            axs[0].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=30 , label='Refuel Cities',zorder=2)
    for i in range(len(route1) - 1):
        axs[0].plot([x_coords[route1[i]], x_coords[route1[i + 1]]], [y_coords[route1[i]], y_coords[route1[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route1[i]] + 0.5 * (x_coords[route1[i+1]] - x_coords[route1[i]])
        end_y = y_coords[route1[i]] + 0.5 * (y_coords[route1[i+1]] - y_coords[route1[i]])
        if math.sqrt((x_coords[route1[i]]-x_coords[route1[i+1]])**2+(y_coords[route1[i]]-y_coords[route1[i+1]])**2)  > min_distance:   
            arrow = FancyArrowPatch((x_coords[route1[i]], y_coords[route1[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            axs[0].add_patch(arrow)
    counter = 0
    for i in range(len(exp_refuel_states1)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states1[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            axs[0].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            axs[0].scatter(marker_x, marker_y, marker='x', color='orange', s=65, linewidths=4)   
    axs[0].set_title(title1)
    legend1_a = axs[0].legend(loc='lower left', fontsize=12)
    legend1_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_1,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_1,3)} km')]
    legend1_b = axs[0].legend(handles = legend1_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend1_b.legend_handles[0].set_visible(False)
    legend1_b.legend_handles[1].set_visible(False)
    axs[0].add_artist(legend1_a)
    
    # Scatter plot for episode Best
    axs[1].scatter(x_coords, y_coords, marker='o', color='r', s=30 , label='No Refuel Cities',zorder=2)
    axs[1].scatter(x_coords[route2[0]], y_coords[route2[0]], marker='o', color='b', s=30, label='Starting City',zorder=2)
    counter = 0
    for idx in refuel_states2:
        if counter < len(refuel_states2) - 1 :
            axs[1].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=30,zorder=2)
            counter += 1
        else:
            axs[1].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=30, label='Refuel Cities',zorder=2)
    for i in range(len(route2) - 1):
        axs[1].plot([x_coords[route2[i]], x_coords[route2[i + 1]]], [y_coords[route2[i]], y_coords[route2[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route2[i]] + 0.5 * (x_coords[route2[i+1]] - x_coords[route2[i]])
        end_y = y_coords[route2[i]] + 0.5 * (y_coords[route2[i+1]] - y_coords[route2[i]])
        if math.sqrt((x_coords[route2[i]]-x_coords[route2[i+1]])**2+(y_coords[route2[i]]-y_coords[route2[i+1]])**2)  > min_distance:    
            arrow = FancyArrowPatch((x_coords[route2[i]], y_coords[route2[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            axs[1].add_patch(arrow)      
    counter = 0
    for i in range(len(exp_refuel_states2)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states2[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            axs[1].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            axs[1].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4)
    axs[1].set_title(title2)
    legend2_a = axs[1].legend(loc='lower left', fontsize=12)
    legend2_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_2,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_2,3)} km')]
    legend2_b = axs[1].legend(handles = legend2_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend2_b.legend_handles[0].set_visible(False)
    legend2_b.legend_handles[1].set_visible(False)
    axs[1].add_artist(legend2_a)
    
    # Customize plot (optional)
    for ax in axs:
        #ax.set_aspect(4) ΕΔΏ ΑΛΛΆΖΩ ΤΟ ratio x/y ΤΟΥ ΚΑΘΕ subplot ΑΜΑ ΘΕΛΩ
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True)

    # Show the plot
    plt.tight_layout()
    fig.savefig(os.path.join(save_dir, f'map{filename_suffix}.png')) 
    plt.close(fig)  # Close the figure to free up memory
    return

def map_heuristic_Bahia30D(city_data , cost_1 , distance_1 , route1 , refuel_states1 , exp_refuel_states1 , title1 , filename_suffix):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    #min distance for arrows
    min_distance = math.sqrt( (x_coords[12]-x_coords[27])*(x_coords[12]-x_coords[27]) + (y_coords[12]-y_coords[27])*(y_coords[12]-y_coords[27]) )

    # Create a figure with two subplots
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    ax1.scatter(x_coords, y_coords, marker='o', color='r', s=30, label='No Refuel Cities' ,zorder=2)
    ax1.scatter(x_coords[route1[0]], y_coords[route1[0]], marker='o', color='b', s=30, label='Starting City',zorder=2)
    counter = 0         #Το counter το έβαλα ως πατέντα για να μην εμφανίζεται στο legend πολλές φορές το refuel states symbol 
    for idx in refuel_states1:
        if counter < len(refuel_states1) - 1 :
            ax1.scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=30, zorder=2)
            counter += 1
        else :
            ax1.scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=30 , label='Refuel Cities',zorder=2)
    for i in range(len(route1) - 1):
        ax1.plot([x_coords[route1[i]], x_coords[route1[i + 1]]], [y_coords[route1[i]], y_coords[route1[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route1[i]] + 0.5 * (x_coords[route1[i+1]] - x_coords[route1[i]])
        end_y = y_coords[route1[i]] + 0.5 * (y_coords[route1[i+1]] - y_coords[route1[i]])
        if math.sqrt((x_coords[route1[i]]-x_coords[route1[i+1]])**2+(y_coords[route1[i]]-y_coords[route1[i+1]])**2)  > min_distance:   
            arrow = FancyArrowPatch((x_coords[route1[i]], y_coords[route1[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            ax1.add_patch(arrow)
    counter = 0
    for i in range(len(exp_refuel_states1)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states1[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            ax1.scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            ax1.scatter(marker_x, marker_y, marker='x', color='orange', s=65, linewidths=4)   
    ax1.set_title(title1)
    legend1_a = ax1.legend(loc='lower left', fontsize=12)
    legend1_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_1,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_1,3)} km')]
    legend1_b = ax1.legend(handles = legend1_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend1_b.legend_handles[0].set_visible(False)
    legend1_b.legend_handles[1].set_visible(False)
    ax1.add_artist(legend1_a)
    
    # Customize plot (optional)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True)

    # Show the plot
    plt.tight_layout()
    fig.savefig(os.path.join(save_dir, f'map{filename_suffix}.png')) 
    plt.close(fig)  # Close the figure to free up memory
    return

def map_no_route_Minas24D(city_data , title1):
   
    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    # Create a figure with two subplots
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    ax1.scatter(x_coords, y_coords, marker='o', color='r', s=28, label='Cities')
    for city, y, x in city_data:
        ax1.text(x, y-0.1, str(int(city)), fontsize=9, ha='center', va='center')
    ax1.legend(loc='upper left', fontsize=12)
    
    # Customize plot (optional)
    ax1.set_title(title1)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

    return

def map_Minas24D(city_location , cost_1 , distance_1 , cost_2 , distance_2 , route1 , refuel_states1 , exp_refuel_states1 , route2 , refuel_states2 , exp_refuel_states2 , title1 ,title2 , filename_suffix):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_location]    #longitude
    y_coords = [coord[1] for coord in city_location]    #latitude

    #min distance for arrows
    min_distance = math.sqrt( (x_coords[2]-x_coords[1])*(x_coords[2]-x_coords[1]) + (y_coords[2]-y_coords[1])*(y_coords[2]-y_coords[1]) )
    
    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    axs[0].scatter(x_coords, y_coords, marker='o', color='r', s=28, label='No Refuel Cities' ,zorder=2)
    axs[0].scatter(x_coords[route1[0]], y_coords[route1[0]], marker='o', color='b', s=28, label='Starting City',zorder=2)
    counter = 0         #Το counter το έβαλα ως πατέντα για να μην εμφανίζεται στο legend πολλές φορές το refuel states symbol 
    for idx in refuel_states1:
        if counter < len(refuel_states1) - 1 :
            axs[0].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28, zorder=2)
            counter += 1
        else :
            axs[0].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28 , label='Refuel Cities',zorder=2)
    for i in range(len(route1) - 1):
        axs[0].plot([x_coords[route1[i]], x_coords[route1[i + 1]]], [y_coords[route1[i]], y_coords[route1[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route1[i]] + 0.5 * (x_coords[route1[i+1]] - x_coords[route1[i]])
        end_y = y_coords[route1[i]] + 0.5 * (y_coords[route1[i+1]] - y_coords[route1[i]])
        if math.sqrt((x_coords[route1[i]]-x_coords[route1[i+1]])**2+(y_coords[route1[i]]-y_coords[route1[i+1]])**2)  > min_distance:   
            arrow = FancyArrowPatch((x_coords[route1[i]], y_coords[route1[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            axs[0].add_patch(arrow)
    counter = 0
    for i in range(len(exp_refuel_states1)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states1[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            axs[0].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            axs[0].scatter(marker_x, marker_y, marker='x', color='orange', s=65, linewidths=4)   
    axs[0].set_title(title1)
    legend1_a = axs[0].legend(loc='lower left', fontsize=12)
    legend1_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_1,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_1,3)} km')]
    legend1_b = axs[0].legend(handles = legend1_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend1_b.legend_handles[0].set_visible(False)
    legend1_b.legend_handles[1].set_visible(False)
    axs[0].add_artist(legend1_a)
    
    # Scatter plot for episode Best
    axs[1].scatter(x_coords, y_coords, marker='o', color='r', s=28 , label='No Refuel Cities',zorder=2)
    axs[1].scatter(x_coords[route2[0]], y_coords[route2[0]], marker='o', color='b', s=28, label='Starting City',zorder=2)
    counter = 0
    for idx in refuel_states2:
        if counter < len(refuel_states2) - 1 :
            axs[1].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28,zorder=2)
            counter += 1
        else:
            axs[1].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28, label='Refuel Cities',zorder=2)
    for i in range(len(route2) - 1):
        axs[1].plot([x_coords[route2[i]], x_coords[route2[i + 1]]], [y_coords[route2[i]], y_coords[route2[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route2[i]] + 0.5 * (x_coords[route2[i+1]] - x_coords[route2[i]])
        end_y = y_coords[route2[i]] + 0.5 * (y_coords[route2[i+1]] - y_coords[route2[i]])
        if math.sqrt((x_coords[route2[i]]-x_coords[route2[i+1]])**2+(y_coords[route2[i]]-y_coords[route2[i+1]])**2)  > min_distance:    
            arrow = FancyArrowPatch((x_coords[route2[i]], y_coords[route2[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            axs[1].add_patch(arrow)      
    counter = 0
    for i in range(len(exp_refuel_states2)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states2[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            axs[1].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            axs[1].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4)
    axs[1].set_title(title2)
    legend2_a = axs[1].legend(loc='lower left', fontsize=12)
    legend2_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_2,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_2,3)} km')]
    legend2_b = axs[1].legend(handles = legend2_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend2_b.legend_handles[0].set_visible(False)
    legend2_b.legend_handles[1].set_visible(False)
    axs[1].add_artist(legend2_a)
    
    # Customize plot (optional)
    for ax in axs:
        #ax.set_aspect(4) ΕΔΏ ΑΛΛΆΖΩ ΤΟ ratio x/y ΤΟΥ ΚΑΘΕ subplot ΑΜΑ ΘΕΛΩ
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True)

    # Show the plot
    plt.tight_layout()
    fig.savefig(os.path.join(save_dir, f'map{filename_suffix}.png')) 
    plt.close(fig)  # Close the figure to free up memory
    return

def map_heuristic_Minas24D(city_data , cost_1 , distance_1 , route1 , refuel_states1 , exp_refuel_states1 , title1 , filename_suffix):

    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    #min distance for arrows
    min_distance = math.sqrt( (x_coords[2]-x_coords[1])*(x_coords[2]-x_coords[1]) + (y_coords[2]-y_coords[1])*(y_coords[2]-y_coords[1]) )
    
    # Create a figure with two subplots
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    ax1.scatter(x_coords, y_coords, marker='o', color='r', s=28, label='No Refuel Cities' ,zorder=2)
    ax1.scatter(x_coords[route1[0]], y_coords[route1[0]], marker='o', color='b', s=28, label='Starting City',zorder=2)
    counter = 0         #Το counter το έβαλα ως πατέντα για να μην εμφανίζεται στο legend πολλές φορές το refuel states symbol 
    for idx in refuel_states1:
        if counter < len(refuel_states1) - 1 :
            ax1.scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28, zorder=2)
            counter += 1
        else :
            ax1.scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28 , label='Refuel Cities',zorder=2)
    for i in range(len(route1) - 1):
        ax1.plot([x_coords[route1[i]], x_coords[route1[i + 1]]], [y_coords[route1[i]], y_coords[route1[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route1[i]] + 0.5 * (x_coords[route1[i+1]] - x_coords[route1[i]])
        end_y = y_coords[route1[i]] + 0.5 * (y_coords[route1[i+1]] - y_coords[route1[i]])
        if math.sqrt((x_coords[route1[i]]-x_coords[route1[i+1]])**2+(y_coords[route1[i]]-y_coords[route1[i+1]])**2)  > min_distance:   
            arrow = FancyArrowPatch((x_coords[route1[i]], y_coords[route1[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            ax1.add_patch(arrow)
    counter = 0
    for i in range(len(exp_refuel_states1)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states1[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            ax1.scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            ax1.scatter(marker_x, marker_y, marker='x', color='orange', s=65, linewidths=4)   
    ax1.set_title(title1)
    legend1_a = ax1.legend(loc='lower left', fontsize=12)
    legend1_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_1,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_1,3)} km')]
    legend1_b = ax1.legend(handles = legend1_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend1_b.legend_handles[0].set_visible(False)
    legend1_b.legend_handles[1].set_visible(False)
    ax1.add_artist(legend1_a)
    
    # Customize plot (optional)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True)

    # Show the plot
    plt.tight_layout()
    fig.savefig(os.path.join(save_dir, f'map{filename_suffix}.png')) 
    plt.close(fig)  # Close the figure to free up memory

    return

def map_no_route_Minas30D(city_data , title1):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    # Create a figure with two subplots
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    ax1.scatter(x_coords, y_coords, marker='o', color='r', s=28, label='Cities')
    for city, y, x in city_data:
        ax1.text(x, y-0.1, str(int(city)), fontsize=9, ha='center', va='center')
    ax1.legend(loc='upper left', fontsize=12)
    
    # Customize plot (optional)
    ax1.set_title(title1)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

    return

def map_Minas30D(city_location , cost_1 , distance_1 , cost_2 , distance_2 , route1 , refuel_states1 , exp_refuel_states1 , route2 , refuel_states2 , exp_refuel_states2 , title1 ,title2 , filename_suffix):
   
    # Extract coordinates
    x_coords = [coord[2] for coord in city_location]    #longitude
    y_coords = [coord[1] for coord in city_location]    #latitude

    #min distance for arrows
    min_distance = math.sqrt( (x_coords[2]-x_coords[1])*(x_coords[2]-x_coords[1]) + (y_coords[2]-y_coords[1])*(y_coords[2]-y_coords[1]) )
    
    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    axs[0].scatter(x_coords, y_coords, marker='o', color='r', s=28, label='No Refuel Cities' ,zorder=2)
    axs[0].scatter(x_coords[route1[0]], y_coords[route1[0]], marker='o', color='b', s=28, label='Starting City',zorder=2)
    counter = 0         #Το counter το έβαλα ως πατέντα για να μην εμφανίζεται στο legend πολλές φορές το refuel states symbol 
    for idx in refuel_states1:
        if counter < len(refuel_states1) - 1 :
            axs[0].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28, zorder=2)
            counter += 1
        else :
            axs[0].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28 , label='Refuel Cities',zorder=2)
    for i in range(len(route1) - 1):
        axs[0].plot([x_coords[route1[i]], x_coords[route1[i + 1]]], [y_coords[route1[i]], y_coords[route1[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route1[i]] + 0.5 * (x_coords[route1[i+1]] - x_coords[route1[i]])
        end_y = y_coords[route1[i]] + 0.5 * (y_coords[route1[i+1]] - y_coords[route1[i]])
        if math.sqrt((x_coords[route1[i]]-x_coords[route1[i+1]])**2+(y_coords[route1[i]]-y_coords[route1[i+1]])**2)  > min_distance:   
            arrow = FancyArrowPatch((x_coords[route1[i]], y_coords[route1[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            axs[0].add_patch(arrow)
    counter = 0
    for i in range(len(exp_refuel_states1)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states1[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            axs[0].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            axs[0].scatter(marker_x, marker_y, marker='x', color='orange', s=65, linewidths=4)   
    axs[0].set_title(title1)
    legend1_a = axs[0].legend(loc='lower left', fontsize=12)
    legend1_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_1,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_1,3)} km')]
    legend1_b = axs[0].legend(handles = legend1_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend1_b.legend_handles[0].set_visible(False)
    legend1_b.legend_handles[1].set_visible(False)
    axs[0].add_artist(legend1_a)
    
    # Scatter plot for episode Best
    axs[1].scatter(x_coords, y_coords, marker='o', color='r', s=28 , label='No Refuel Cities',zorder=2)
    axs[1].scatter(x_coords[route2[0]], y_coords[route2[0]], marker='o', color='b', s=28, label='Starting City',zorder=2)
    counter = 0
    for idx in refuel_states2:
        if counter < len(refuel_states2) - 1 :
            axs[1].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28,zorder=2)
            counter += 1
        else:
            axs[1].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28, label='Refuel Cities',zorder=2)
    for i in range(len(route2) - 1):
        axs[1].plot([x_coords[route2[i]], x_coords[route2[i + 1]]], [y_coords[route2[i]], y_coords[route2[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route2[i]] + 0.5 * (x_coords[route2[i+1]] - x_coords[route2[i]])
        end_y = y_coords[route2[i]] + 0.5 * (y_coords[route2[i+1]] - y_coords[route2[i]])
        if math.sqrt((x_coords[route2[i]]-x_coords[route2[i+1]])**2+(y_coords[route2[i]]-y_coords[route2[i+1]])**2)  > min_distance:    
            arrow = FancyArrowPatch((x_coords[route2[i]], y_coords[route2[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            axs[1].add_patch(arrow)      
    counter = 0
    for i in range(len(exp_refuel_states2)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states2[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            axs[1].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            axs[1].scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4)
    axs[1].set_title(title2)
    legend2_a = axs[1].legend(loc='lower left', fontsize=12)
    legend2_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_2,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_2,3)} km')]
    legend2_b = axs[1].legend(handles = legend2_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend2_b.legend_handles[0].set_visible(False)
    legend2_b.legend_handles[1].set_visible(False)
    axs[1].add_artist(legend2_a)
    
    # Customize plot (optional)
    for ax in axs:
        #ax.set_aspect(4) ΕΔΏ ΑΛΛΆΖΩ ΤΟ ratio x/y ΤΟΥ ΚΑΘΕ subplot ΑΜΑ ΘΕΛΩ
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True)

    # Show the plot
    plt.tight_layout()
    fig.savefig(os.path.join(save_dir, f'map{filename_suffix}.png')) 
    plt.close(fig)  # Close the figure to free up memory
    return

def map_heuristic_Minas30D(city_data , cost_1 , distance_1 , route1 , refuel_states1 , exp_refuel_states1 , title1 , filename_suffix):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    #min distance for arrows
    min_distance = math.sqrt( (x_coords[2]-x_coords[1])*(x_coords[2]-x_coords[1]) + (y_coords[2]-y_coords[1])*(y_coords[2]-y_coords[1]) )
    
    # Create a figure with two subplots
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    ax1.scatter(x_coords, y_coords, marker='o', color='r', s=28, label='No Refuel Cities' ,zorder=2)
    ax1.scatter(x_coords[route1[0]], y_coords[route1[0]], marker='o', color='b', s=28, label='Starting City',zorder=2)
    counter = 0         #Το counter το έβαλα ως πατέντα για να μην εμφανίζεται στο legend πολλές φορές το refuel states symbol 
    for idx in refuel_states1:
        if counter < len(refuel_states1) - 1 :
            ax1.scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28, zorder=2)
            counter += 1
        else :
            ax1.scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=28 , label='Refuel Cities',zorder=2)
    for i in range(len(route1) - 1):
        ax1.plot([x_coords[route1[i]], x_coords[route1[i + 1]]], [y_coords[route1[i]], y_coords[route1[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route1[i]] + 0.5 * (x_coords[route1[i+1]] - x_coords[route1[i]])
        end_y = y_coords[route1[i]] + 0.5 * (y_coords[route1[i+1]] - y_coords[route1[i]])
        if math.sqrt((x_coords[route1[i]]-x_coords[route1[i+1]])**2+(y_coords[route1[i]]-y_coords[route1[i+1]])**2)  > min_distance:   
            arrow = FancyArrowPatch((x_coords[route1[i]], y_coords[route1[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=17, fc='black', ec='none',zorder=2)
            ax1.add_patch(arrow)
    counter = 0
    for i in range(len(exp_refuel_states1)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states1[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            ax1.scatter(marker_x, marker_y , marker='x', color='orange', s=65, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            ax1.scatter(marker_x, marker_y, marker='x', color='orange', s=65, linewidths=4)   
    ax1.set_title(title1)
    legend1_a = ax1.legend(loc='lower left', fontsize=12)
    legend1_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_1,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_1,3)} km')]
    legend1_b = ax1.legend(handles = legend1_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend1_b.legend_handles[0].set_visible(False)
    legend1_b.legend_handles[1].set_visible(False)
    ax1.add_artist(legend1_a)
    
    # Customize plot (optional)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True)

    # Show the plot
    plt.tight_layout()
    fig.savefig(os.path.join(save_dir, f'map{filename_suffix}.png')) 
    plt.close(fig)  # Close the figure to free up memory

    return

def map_no_route_Minas57D(city_data , title1):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    # Create a figure with two subplots
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    ax1.scatter(x_coords, y_coords, marker='o', color='r', s=13, label='Cities')
    for city, y, x in city_data:
        if city == 35 or city == 52 :
            ax1.text(x, y+0.1, str(int(city)), fontsize=9, ha='center', va='center')
        elif city == 27 :
            ax1.text(x+0.07, y, str(int(city)), fontsize=9, ha='center', va='center')
        elif city == 4 :
            ax1.text(x-0.005, y+0.09, str(int(city)), fontsize=9, ha='center', va='center')
        else :
            ax1.text(x, y-0.12, str(int(city)), fontsize=9, ha='center', va='center')
    ax1.legend(loc='upper left', fontsize=12)
    
    # Customize plot (optional)
    ax1.set_title(title1)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

    return

def map_Minas57D(city_location , cost_1 , distance_1 , cost_2 , distance_2 , route1 , refuel_states1 , exp_refuel_states1 , route2 , refuel_states2 , exp_refuel_states2 , title1 ,title2 , filename_suffix):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_location]    #longitude
    y_coords = [coord[1] for coord in city_location]    #latitude

    #min distance for arrows
    min_distance = math.sqrt( (x_coords[54]-x_coords[29])*(x_coords[54]-x_coords[29]) + (y_coords[54]-y_coords[29])*(y_coords[54]-y_coords[29]) )

    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    axs[0].scatter(x_coords, y_coords, marker='o', color='r', s=13, label='No Refuel Cities' ,zorder=2)
    axs[0].scatter(x_coords[route1[0]], y_coords[route1[0]], marker='o', color='b', s=13, label='Starting City',zorder=2)
    counter = 0         #Το counter το έβαλα ως πατέντα για να μην εμφανίζεται στο legend πολλές φορές το refuel states symbol 
    for idx in refuel_states1:
        if counter < len(refuel_states1) - 1 :
            axs[0].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=13, zorder=2)
            counter += 1
        else :
            axs[0].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=13 , label='Refuel Cities',zorder=2)
    for i in range(len(route1) - 1):
        axs[0].plot([x_coords[route1[i]], x_coords[route1[i + 1]]], [y_coords[route1[i]], y_coords[route1[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route1[i]] + 0.5 * (x_coords[route1[i+1]] - x_coords[route1[i]])
        end_y = y_coords[route1[i]] + 0.5 * (y_coords[route1[i+1]] - y_coords[route1[i]])
        if math.sqrt((x_coords[route1[i]]-x_coords[route1[i+1]])**2+(y_coords[route1[i]]-y_coords[route1[i+1]])**2)  > min_distance:   
            arrow = FancyArrowPatch((x_coords[route1[i]], y_coords[route1[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=14, fc='black', ec='none',zorder=2)
            axs[0].add_patch(arrow)
    counter = 0
    for i in range(len(exp_refuel_states1)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states1[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            axs[0].scatter(marker_x, marker_y , marker='x', color='orange', s=53, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            axs[0].scatter(marker_x, marker_y, marker='x', color='orange', s=53, linewidths=4)   
    axs[0].set_title(title1)
    legend1_a = axs[0].legend(loc='lower left', fontsize=12)
    legend1_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_1,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_1,3)} km')]
    legend1_b = axs[0].legend(handles = legend1_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend1_b.legend_handles[0].set_visible(False)
    legend1_b.legend_handles[1].set_visible(False)
    axs[0].add_artist(legend1_a)
    
    # Scatter plot for episode Best
    axs[1].scatter(x_coords, y_coords, marker='o', color='r', s=13 , label='No Refuel Cities',zorder=2)
    axs[1].scatter(x_coords[route2[0]], y_coords[route2[0]], marker='o', color='b', s=13, label='Starting City',zorder=2)
    counter = 0
    for idx in refuel_states2:
        if counter < len(refuel_states2) - 1 :
            axs[1].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=13,zorder=2)
            counter += 1
        else:
            axs[1].scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=13, label='Refuel Cities',zorder=2)
    for i in range(len(route2) - 1):
        axs[1].plot([x_coords[route2[i]], x_coords[route2[i + 1]]], [y_coords[route2[i]], y_coords[route2[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route2[i]] + 0.5 * (x_coords[route2[i+1]] - x_coords[route2[i]])
        end_y = y_coords[route2[i]] + 0.5 * (y_coords[route2[i+1]] - y_coords[route2[i]])
        if math.sqrt((x_coords[route2[i]]-x_coords[route2[i+1]])**2+(y_coords[route2[i]]-y_coords[route2[i+1]])**2)  > min_distance:    
            arrow = FancyArrowPatch((x_coords[route2[i]], y_coords[route2[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=14, fc='black', ec='none',zorder=2)
            axs[1].add_patch(arrow)      
    counter = 0
    for i in range(len(exp_refuel_states2)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states2[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            axs[1].scatter(marker_x, marker_y , marker='x', color='orange', s=53, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            axs[1].scatter(marker_x, marker_y , marker='x', color='orange', s=53, linewidths=4)
    axs[1].set_title(title2)
    legend2_a = axs[1].legend(loc='lower left', fontsize=12)
    legend2_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_2,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_2,3)} km')]
    legend2_b = axs[1].legend(handles = legend2_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend2_b.legend_handles[0].set_visible(False)
    legend2_b.legend_handles[1].set_visible(False)
    axs[1].add_artist(legend2_a)
    
    # Customize plot (optional)
    for ax in axs:
        #ax.set_aspect(4) ΕΔΏ ΑΛΛΆΖΩ ΤΟ ratio x/y ΤΟΥ ΚΑΘΕ subplot ΑΜΑ ΘΕΛΩ
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.grid(True)

    # Show the plot
    plt.tight_layout()
    fig.savefig(os.path.join(save_dir, f'map{filename_suffix}.png')) 
    plt.close(fig)  # Close the figure to free up memory
    return

def map_heuristic_Minas57D(city_data , cost_1 , distance_1 , route1 , refuel_states1 , exp_refuel_states1 , title1 , filename_suffix):
    
    # Extract coordinates
    x_coords = [coord[2] for coord in city_data]    #longitude
    y_coords = [coord[1] for coord in city_data]    #latitude

    #min distance for arrows
    min_distance = math.sqrt( (x_coords[54]-x_coords[29])*(x_coords[54]-x_coords[29]) + (y_coords[54]-y_coords[29])*(y_coords[54]-y_coords[29]) )

    # Create a figure with two subplots
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))

    # Scatter plot for episode 1 
    ax1.scatter(x_coords, y_coords, marker='o', color='r', s=13, label='No Refuel Cities' ,zorder=2)
    ax1.scatter(x_coords[route1[0]], y_coords[route1[0]], marker='o', color='b', s=13, label='Starting City',zorder=2)
    counter = 0         #Το counter το έβαλα ως πατέντα για να μην εμφανίζεται στο legend πολλές φορές το refuel states symbol 
    for idx in refuel_states1:
        if counter < len(refuel_states1) - 1 :
            ax1.scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=13, zorder=2)
            counter += 1
        else :
            ax1.scatter(x_coords[idx], y_coords[idx], marker='o', color='limegreen', s=13 , label='Refuel Cities',zorder=2)
    for i in range(len(route1) - 1):
        ax1.plot([x_coords[route1[i]], x_coords[route1[i + 1]]], [y_coords[route1[i]], y_coords[route1[i + 1]]], color='grey', linestyle='--',zorder=1)
        end_x = x_coords[route1[i]] + 0.5 * (x_coords[route1[i+1]] - x_coords[route1[i]])
        end_y = y_coords[route1[i]] + 0.5 * (y_coords[route1[i+1]] - y_coords[route1[i]])
        if math.sqrt((x_coords[route1[i]]-x_coords[route1[i+1]])**2+(y_coords[route1[i]]-y_coords[route1[i+1]])**2)  > min_distance:   
            arrow = FancyArrowPatch((x_coords[route1[i]], y_coords[route1[i]]), (end_x,end_y), arrowstyle='-|>', mutation_scale=14, fc='black', ec='none',zorder=2)
            ax1.add_patch(arrow)
    counter = 0
    for i in range(len(exp_refuel_states1)) :
        integers_of_states = [int(s) for s in re.findall(r'\b\d+\b', exp_refuel_states1[i])]
        dx = -x_coords[integers_of_states[0]] + x_coords[integers_of_states[1]] 
        dy = -y_coords[integers_of_states[0]] + y_coords[integers_of_states[1]]
        marker_x = x_coords[integers_of_states[0]] + 0.6 * dx
        marker_y = y_coords[integers_of_states[0]] + 0.6 * dy
        if counter == 0 :
            ax1.scatter(marker_x, marker_y , marker='x', color='orange', s=53, linewidths=4 , label = 'Out of fuel')
            counter =+ 1
        else:
            ax1.scatter(marker_x, marker_y, marker='x', color='orange', s=53, linewidths=4)   
    ax1.set_title(title1)
    legend1_a = ax1.legend(loc='lower left', fontsize=12)
    legend1_b_elements = [Line2D([0], [0], color='r', lw=1, label = f'Cost = {round(cost_1,2)} R$') , Line2D([0], [0], color='r', lw=1, label = f'Distance = {round(distance_1,3)} km')]
    legend1_b = ax1.legend(handles = legend1_b_elements , loc = 'upper left' , handlelength=-1 , prop={'size': 12, 'style': 'italic'})
    legend1_b.legend_handles[0].set_visible(False)
    legend1_b.legend_handles[1].set_visible(False)
    ax1.add_artist(legend1_a)
    
    # Customize plot (optional)
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True)

    # Show the plot
    plt.tight_layout()
    fig.savefig(os.path.join(save_dir, f'map{filename_suffix}.png')) 
    plt.close(fig)  # Close the figure to free up memory

    return