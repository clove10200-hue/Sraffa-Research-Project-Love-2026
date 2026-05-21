import numpy as np
from scipy import linalg
import os

class CommodityMatrix:
    '''
    Workhorse class for parsing and storing commodity coefficient data.
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
                for data in text_data[:-1]:
                    num_data.append(float(data))
                solution_list.append(float(text_data[-1]))
                data_list.append(num_data)
        self.commodity_matrix = np.array(data_list)
        self.total_production_matrix = np.array(solution_list)
        self.price_weights = np.empty(self.total_production_matrix.size)
    def solve_subsistence_economy()-> None:
        '''
        Method for solving the given commodity matrix for a strict subsistence economy, where the total commodity inputs for the economy for each industry are exactly the
        same as commodity outputs for each industry. The first commodity in the economy is selected as a numeraire and its price weight set to 1; the rest of the commodity matrix is solved
        with this in mind. 
        '''
    def solve_growth_economy()-> None:
        '''
        Method for solving the given commodity matrix for an economy with a rate of profit. The first commodity in the economy is selected as a numeraire and its solution set to 1; the rest of the commodity matrix is solved
        with this in mind. 
        '''
