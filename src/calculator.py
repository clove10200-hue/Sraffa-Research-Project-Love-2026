import time
import pathlib
from solve_prices import Economy

DAT_DIR = pathlib.Path(__file__).resolve().parent.parent / "dat"

matrix_100 = Economy.from_file(DAT_DIR / "test_economy_100.txt")
matrix_1000 = Economy.from_file(DAT_DIR / "test_economy_1000.txt")
matrix_5000 = Economy.from_file(DAT_DIR / "test_economy_5000.txt")

precise_start_time_100 = time.perf_counter()
precise_100_rate, precise_100_prices = matrix_100.solve()
precise_end_time_100 = time.perf_counter()

iterative_start_time_100 = time.perf_counter()
iterative_100_rate, iterative_100_prices = matrix_100.power_iteration(.001)
iterative_end_time_100 = time.perf_counter()

precise_execution_time_100 = precise_end_time_100 - precise_start_time_100
iterative_execution_time_100 = iterative_end_time_100 - iterative_start_time_100

print(f"Precise runtime for 100 element economy: {precise_execution_time_100:.6f} seconds \n")
print(f"Iterative runtime for 100 element economy: {iterative_execution_time_100:.6f} seconds \n")

precise_start_time_1000 = time.perf_counter()
precise_1000_rate, precise_1000_prices = matrix_1000.solve()
precise_end_time_1000 = time.perf_counter()

iterative_start_time_1000 = time.perf_counter()
iterative_1000_rate, iterative_1000_prices = matrix_1000.power_iteration(.001)
iterative_end_time_1000 = time.perf_counter()

precise_execution_time_1000 = precise_end_time_1000 - precise_start_time_1000
iterative_execution_time_1000 = iterative_end_time_1000 - iterative_start_time_1000

print(f"Precise runtime for 1000 element economy: {precise_execution_time_1000:.6f} seconds \n")
print(f"Iterative runtime for 1000 element economy: {iterative_execution_time_1000:.6f} seconds \n")

precise_start_time_5000 = time.perf_counter()
precise_5000_rate, precise_5000_prices = matrix_5000.solve()
precise_end_time_5000 = time.perf_counter()

iterative_start_time_5000 = time.perf_counter()
iterative_5000_rate, iterative_5000_prices = matrix_5000.power_iteration(.001)
iterative_end_time_5000 = time.perf_counter()

precise_execution_time_5000 = precise_end_time_5000 - precise_start_time_5000
iterative_execution_time_5000 = iterative_end_time_5000 - iterative_start_time_5000

print(f"Precise runtime for 5000 element economy: {precise_execution_time_5000:.6f} seconds \n")
print(f"Iterative runtime for 5000 element economy: {iterative_execution_time_5000:.6f} seconds \n")
