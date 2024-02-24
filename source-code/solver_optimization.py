#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Filename: solver_optimization.py
# Description: this python script applies solver optimization on data
# Author: Oleksandr Karpenko, karpen04@ads.uni-passau.de
# SPDX-License-Identifier: MIT
# Version: 1.1
#
# This code was based on tutorial: 
# https://ychung38.medium.com/how-to-use-solver-excel-in-python-458336408c7f


from pulp import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

bathing_friends_unlimited_path = '/home/duckies/data/bathing_friends_unlimited.xls'
result_graph_path = '/home/duckies/report/figures/result_plot.png'

# Constraints
ducks_time_constraint = 400
fish_time_constraint = 300
ducks_sale_forecast_constraint = 150
fish_sale_forecast_constraint = 50


# Function loads data from .xls file
def read_file(path_to_file):
    return pd.read_excel(path_to_file)

# Function to solve do optimization problem
def solve_problem(variable1_name, variable2_name, all_pellet_count, duck_pellet_count, fish_pellet_count, duck_unit_cost, fish_unit_cost,
 ducks_time_constraint, fish_time_constraint, ducks_sale_forecast_constraint, fish_sale_forecast_constraint):

    variables = list([variable1_name, variable2_name])
    unit_costs = dict(zip(variables, [duck_unit_cost, fish_unit_cost]))
    pellets = dict(zip(variables, [duck_pellet_count, fish_pellet_count]))

    # Define problem
    prob = LpProblem('Profit', LpMaximize)

    # Define variables to optimize
    inv_vars = LpVariable.dicts('Variable', variables, lowBound=0, cat='Integar')

    # Define an objective function
    prob += lpSum([inv_vars[i] * unit_costs[i] for i in variables])


    # Define constraints
    prob += lpSum([pellets[i] * inv_vars[i] for i in variables]) <= all_pellet_count 
    prob += inv_vars[variables[0]] <= ducks_time_constraint 
    prob += inv_vars[variables[1]] <= fish_time_constraint
    prob += inv_vars[variables[0]] <= ducks_sale_forecast_constraint
    prob += inv_vars[variables[1]] <= fish_sale_forecast_constraint

    # Execute solver
    prob.solve()

    return prob

def generate_answer(problem):
    # Answer
    value(problem.objective)
    # Variables' values
    print('The optimal answer\n'+'-'*70)
    for v in problem.variables():
        if v.varValue > 0:
            print(v.name, '=', v.varValue)

    return problem.variables()        

# Function generates result graph
def generate_result_graph(ducks_time_constraint, fish_time_constraint, ducks_sale_forecast_constraint, fish_sale_forecast_constraint, duck_unit_cost, fish_unit_cost,
duck_amount, fish_amount):

    # Data points
    amount_fishes = np.arange(0, fish_amount+1, 1)  
    amount_ducks = np.arange(0, duck_amount+1, 1)   

    # Calculate profit and total amount for each combination
    profits = []
    total_amounts = []

    for amount_fish in amount_fishes:
        for amount_duck in amount_ducks:
            profit = fish_unit_cost * amount_fish + duck_unit_cost * amount_duck
            total_amount = amount_fish + amount_duck
            profits.append(profit)
            total_amounts.append(total_amount)

    # Set the figure size
    plt.figure(figsize=(6, 6))  

    # Plot the data points
    plt.plot(profits, total_amounts, label='Profit vs Total Amount', marker='o')

    # Add a constraint line
    constraint_value = duck_amount + fish_amount
    constraint_profit = fish_unit_cost * fish_amount + duck_unit_cost * duck_amount
    plt.axhline(y=constraint_value, color='orange', linestyle='--', label='Best fish and ducks Count')

    # Add a line along the x-axis
    plt.axvline(x=constraint_profit, color='red', linestyle='--', label='Best profit')

    # Label the axes
    plt.xlabel('Profit')
    plt.ylabel('Total Amount (Fish + Ducks)')

    # Set x-axis ticks with a step of 50
    plt.xticks(np.arange(0, max(profits) + 1, 150))

    # Add a title
    plt.title('Profit vs Total Amount')

    # Add a legend
    plt.legend()

    # Save the plot as an image
    plt.savefig(result_graph_path)

    # Close the plot
    plt.close()

def main():

    data = read_file(bathing_friends_unlimited_path)

    # Get necessary information from .xls file
    all_pellet_count = data.iloc[12, 1]
    duck_pellet_count = data.iloc[8, 1]
    fish_pellet_count = data.iloc[9, 1]
    duck_unit_cost = data.iloc[15, 1]
    fish_unit_cost = data.iloc[16, 1]
    variable1_name = data.iloc[3,0]
    variable2_name = data.iloc[4,0]

    problem = solve_problem(variable1_name, variable2_name, all_pellet_count, duck_pellet_count, fish_pellet_count, duck_unit_cost, fish_unit_cost,
    ducks_time_constraint, fish_time_constraint, ducks_sale_forecast_constraint, fish_sale_forecast_constraint)

    problem_variables = generate_answer(problem)

    generate_result_graph(ducks_time_constraint, fish_time_constraint, ducks_sale_forecast_constraint, fish_sale_forecast_constraint,
     duck_unit_cost, fish_unit_cost, problem_variables[0].varValue, problem_variables[1].varValue)

if __name__ == "__main__":
    main()
