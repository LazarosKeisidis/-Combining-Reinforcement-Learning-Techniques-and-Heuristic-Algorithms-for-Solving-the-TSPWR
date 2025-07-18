import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import os

exchange_rate = 0.1631 
save_dir = "random save dir on ur pc"

# graph function
def graph(total_cost_plot , Iteration_plot, algorithm_name , best_solution) :
    fig, ax1 = plt.subplots(figsize=(21.9, 11.1))
    total_cost_plot.append(best_solution[0])
    Iteration_plot.append(best_solution[5])
    total_cost_plot_euros = [cost * exchange_rate for cost in total_cost_plot]
    # Initialize PLOT
    for i in range(len(total_cost_plot_euros)) :
        if i>0 and total_cost_plot_euros[i] != total_cost_plot_euros[i-1] and i != len(total_cost_plot_euros) - 1 :        
            ax1.scatter(Iteration_plot[i], total_cost_plot_euros[i], color='tab:blue', marker='o', s = 15, zorder = 1)
        if i == len(total_cost_plot_euros) - 1 :
            ax1.scatter(Iteration_plot[i], total_cost_plot_euros[i], color='red', marker='o', s = 15 , zorder = 2)          
    ax1.set_title(algorithm_name + ' training')
    ax1.set_xlabel('EPISODE NUMBER')
    ax1.set_ylabel('TOTAL COST')
    legend_elements = [Line2D([0], [0], color='tab:blue', lw=0,marker = 'o', label='Cost During Training'), 
                       Line2D([0], [0], color='red', lw=0, marker = 'o',label=f'Best Cost Found ({round(exchange_rate*best_solution[0],2)} €)')]
    # Create the legend
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=12)
    fig.savefig(os.path.join(save_dir, f'training_graph.png'), bbox_inches='tight')
    plt.close(fig)  # Close the figure to free up memory
    return