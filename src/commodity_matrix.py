import numpy as np
from scipy.linalg import solve
import os

class CommodityMatrix:
    '''
    Workhorse class for parsing and storing commodity coefficient data. It is assumed that the data input is a .txt file that contains the commodity coefficients for each industry
    with the final entry for each line being the coefficient of the solution vector. 
    '''
    def __init__(self, data_path: str) -> None:
        script_dir: str = os.path.dirname(__file__)
        file_path: str = os.path.join(script_dir, data_path)
        data_list: list[list[float]] = []
        solution_list: list[float] = []
        with open(file_path, "r") as file:
            for line in file:
                text_data: list[str] = line.split()
                num_data: list[float] = []
                for data in text_data[:-1]:  ##read all but the last value into the list that will become the coefficient matrix
                    num_data.append(float(data))
                solution_list.append(float(text_data[-1]))  ##read the last value into the list that will become the solution vector
                data_list.append(num_data)
        self.commodity_matrix = np.array(data_list)
        self.total_production_matrix = np.array(solution_list)
        self.price_weights = np.empty(self.total_production_matrix.size)

    def solve_subsistence_economy(self)-> None:
        '''
        Method for solving the given commodity matrix for a strict subsistence economy, where the total commodity inputs for the economy for each industry are exactly the
        same as commodity outputs for each industry. The first commodity in the economy is selected as a numeraire and its price weight set to 1; the rest of the commodity matrix is solved
        with this in mind. 
        '''
        prod_matrix_index: int = 0
        start_matrix = self.commodity_matrix.copy() 
        for value in self.total_production_matrix:
            start_matrix[prod_matrix_index, prod_matrix_index] = self.commodity_matrix[prod_matrix_index, prod_matrix_index] - value
            prod_matrix_index += 1
        simplified_matrix = start_matrix[1:, 1:].copy() #get an array that consists of the simplified commodity matrix - drop the first equation and the first commodity from each other equation
        solution_vector = self.commodity_matrix[1:, 0].copy() #get a solution vector that consists of the coefficients of the numeraire commodity, as its price is defined as 1
        solution_index: int = 0
        for solution in solution_vector:
            solution_vector[solution_index] = solution_vector[solution_index]*-1 #remember that we're subtracting to get these constants!
            solution_index += 1 
        solutions = solve(simplified_matrix, solution_vector) #solve the simplified matrix
        solution_index = 1
        self.price_weights[0] = 1
        for solution in solutions:
            self.price_weights[solution_index] = solution
            solution_index += 1
        
    def solve_growth_economy()-> None:
        '''
        Method for solving the given commodity matrix for an economy with a rate of profit. The first commodity in the economy is selected as a numeraire and its solution set to 1; the rest of the commodity matrix is solved
        with this in mind. Will also calculate a rate of profit in addition to the price weights.
        '''
