import unittest
import pytest
import numpy as np
from commodity_matrix import *

class CalculatorTests(unittest.TestCase):

    #First, test to make sure the calculator is making matrices as expected:
    def test_instantiate_matrix_01(self) -> None:
        matrix = CommodityMatrix("../dat/subsistence_1.txt")
        test_matrix = np.array([[280.0, 12.0], [120.0,8.0]])
        solution_vector = np.array([400.0, 20.0])

        self.assertTrue(np.array_equal(matrix.commodity_matrix, test_matrix))
        self.assertTrue(np.array_equal(matrix.total_production_matrix, solution_vector))

    def test_instantiate_matrix_02(self) -> None:
        matrix = CommodityMatrix("../dat/subsistence_2.txt")
        test_matrix = np.array([[240.0, 12.0, 18.0], [90.0, 6.0, 12.0], [120.0, 3.0, 30.0]])
        solution_vector = np.array([450.0, 21.0, 60.0])

        self.assertTrue(np.array_equal(matrix.commodity_matrix, test_matrix))
        self.assertTrue(np.array_equal(matrix.total_production_matrix, solution_vector))

    #Now, test subsistence calculator functionality:
    def test_subsistence_calculator_01(self) -> None:
        matrix = CommodityMatrix("../dat/subsistence_1.txt")
        price_solution = np.array([1.0, 10.0])
        matrix.solve_subsistence_economy()

        self.assertTrue(np.allclose(matrix.price_weights, price_solution))
    def test_subsistence_calculator_02(self) -> None:
        matrix = CommodityMatrix("../dat/subsistence_2.txt")
        price_solution = np.array([1.0, 10.0, 5.0])
        matrix.solve_subsistence_economy()

        self.assertTrue(np.allclose(matrix.price_weights, price_solution))
        
    #Skeletons of a growth test suite are here. TODO: Finish implementing, double-check solutions by hand
    def test_growth_calculator_01(self) -> None:
        matrix = CommodityMatrix("../dat/surplus_1.txt")
        price_solution = np.array([1.0, 15.0])
        growth_rate: float = 1.25
        matrix.solve_growth_economy()

        self.assertTrue(np.allclose(matrix.price_weights, price_solution))
        self.assertAlmostEqual(matrix.growth_rate, growth_rate)

    def test_growth_calculator_02(self) -> None:
        matrix = CommodityMatrix(".../dat/surplus_2.txt")
        price_solution = np.array()
        growth_rate: float = 1.25
        matrix.solve_growth_economy()

        self.assertTrue(np.allclose(matrix.price_weights, price_solution))
        self.assertAlmostEqual(matrix.growth_rate, growth_rate)
    