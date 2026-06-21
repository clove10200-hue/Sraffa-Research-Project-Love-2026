import pathlib
from solve_prices import Economy

DAT_DIR = pathlib.Path(__file__).resolve().parent.parent / "dat"

trivial_matrix = Economy.from_file(DAT_DIR / "subsistence_2.txt")
matrix_10 = Economy.from_file(DAT_DIR / "test_economy_10.txt")
matrix_100 = Economy.from_file(DAT_DIR / "test_economy_100.txt")
matrix_100_alter = Economy.from_file(DAT_DIR / "test_economy_100_altered.txt")
matrix_1000 = Economy.from_file(DAT_DIR / "test_economy_1000.txt")
matrix_5000 = Economy.from_file(DAT_DIR / "test_economy_5000.txt")

#trivial_cond = trivial_matrix.condition_number()
#cond_10 = matrix_10.condition_number()
#cond_100 = matrix_100.condition_number()
#cond_1000 = matrix_1000.condition_number()
#cond_5000 = matrix_5000.condition_number()

#print (f"2-element matrix condition number:{trivial_cond} \n")
#print(f"10-element matrix condition number:{cond_10} \n")
#print(f"100-element matrix condition number:{cond_100} \n")
#print(f"1000-element matrix condition number:{cond_1000} \n")
#print(f"5000-element matrix condition number:{cond_5000} \n")

#r_100, p_100 = matrix_100.power_iteration(0.001)
#ra_100, pa_100 = matrix_100_alter.power_iteration(0.001)

#print(f"Unaltered 100-element matrix R: {r_100} \n")
#print(f"Altered 100-element matrix R: {ra_100} \n")

r_5000, p_5000 = matrix_5000.power_iteration(0.001)

error_r_list: list[float] = []
for x in range(50):
    error_5000 = matrix_5000.perturb(0.01)
    error_r, error_p = error_5000.power_iteration(0.001)
    error_r_list.append(error_r)
average = sum(error_r_list)/50
error_deviation_list: list[float] = []
for value in error_r_list:
    deviation = abs(value-average)**2
    error_deviation_list.append(deviation)
std_dev = (sum(error_deviation_list)/50)**0.5

print(f"The true r value is: {r_5000} \n")
print(f"The list of error r values are: {error_r_list} \n" )
print(f"The average error value for r is: {average} \n")
print(f"The standard deviation of the value r is: {std_dev}")