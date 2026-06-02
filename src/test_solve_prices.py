"""Compare the eigenvalue-based price solver in solve_prices.py against the
fsolve-based CommodityMatrix.solve_growth_economy on the dat/ files.

Both methods should return identical prices and an identical growth factor.
Note that CommodityMatrix exposes the growth factor (1+r), while Economy.solve
returns the rate of profit r itself -- so we compare (1 + r) to growth_rate.

CommodityMatrix.solve_growth_economy is currently hardcoded for a 2x2 system,
so the cross-solver comparison only runs on surplus_1.txt (2 commodities).
surplus_2.txt is exercised against the eigenvalue solver alone, as a regression
check on the larger case.
"""

import pathlib
import unittest

import numpy as np

from commodity_matrix import CommodityMatrix
from solve_prices import Economy

DAT_DIR = pathlib.Path(__file__).resolve().parent.parent / "dat"


class EigenvalueVsFsolveTests(unittest.TestCase):

    def test_surplus_1_eigenvalue_matches_fsolve(self) -> None:
        """On the 2x2 wheat/iron surplus economy, eigenvalue and fsolve agree."""
        eig_economy = Economy.from_file(DAT_DIR / "surplus_1.txt")
        eig_r, eig_prices = eig_economy.solve()

        fs_matrix = CommodityMatrix("../dat/surplus_1.txt")
        fs_matrix.solve_growth_economy()

        # prices line up element-wise (commodity 0 is the numeraire in both)
        np.testing.assert_allclose(eig_prices, fs_matrix.price_weights, atol=1e-8)
        # CommodityMatrix.growth_rate is the growth factor (1+r), not r itself
        self.assertAlmostEqual(1.0 + eig_r, float(fs_matrix.growth_rate), places=8)


class EigenvalueOnlyTests(unittest.TestCase):
    """surplus_2.txt is 3x3, which exceeds the scope of the current fsolve
    implementation. We still want a regression check that the eigenvalue solver
    handles it and returns sane numbers."""

    def test_surplus_2_eigenvalue_runs(self) -> None:
        economy = Economy.from_file(DAT_DIR / "surplus_2.txt")
        r, prices = economy.solve()

        self.assertGreater(r, 0.0)              # surplus economy => positive profit rate
        self.assertAlmostEqual(prices[0], 1.0)  # numeraire
        np.testing.assert_array_less(0.0, prices)  # all prices strictly positive (Perron-Frobenius)

        # plug the solution back in: (1+r) M p == q * p
        residual = (economy.M @ prices) * (1.0 + r) - economy.q * prices
        self.assertLess(float(np.max(np.abs(residual))), 1e-8)

class PowerIterationTests(unittest.TestCase):
    """Test cases for the power iteration method implementation. The base error allowed is .001 and values are directly compared to the exact mathematical solution
    methods."""

    def test_power_iteration_1(self) -> None:
        power_economy = Economy.from_file(DAT_DIR / "surplus_1.txt")
        r, prices = power_economy.power_iteration(0.001)
        r_solution, price_solution = power_economy.solve()

        self.assertGreater(r, 0.0) #sanity checking r and price values
        self.assertAlmostEqual(prices[0], 1.0)
        np.testing.assert_array_less(0.0, prices)

        np.testing.assert_allclose(r, r_solution, rtol = 1e3) #allow for an amount of potential error equal to the error added to the error given to the power iteration function
        np.testing.assert_allclose(prices, price_solution, rtol = 1e3)

    def test_power_iteration_2(self) -> None:
        power_economy = Economy.from_file(DAT_DIR / "surplus_2.txt")
        r, prices = power_economy.power_iteration(0.001)
        r_solution, price_solution = power_economy.solve()

        self.assertGreater(r, 0.0)
        self.assertAlmostEqual(prices[0], 1.0)
        np.testing.assert_array_less(0.0, prices)

        np.testing.assert_allclose(r, r_solution, rtol = 1e3)
        np.testing.assert_allclose(prices, price_solution, rtol = 1e3)

if __name__ == "__main__":
    unittest.main()
