## TODO: The economy generator
import pathlib
import random

def write_pvm_matrix(filename: str, size: int) -> None:
    thisdir = pathlib.Path(__file__).parent.resolve()
    DAT_DIR = thisdir.parent / "dat"
    current_path = DAT_DIR / filename
    with open(current_path, "a") as file:
        potion_string = str(size*500)
        potion_string = add_zeroes(potion_string, size-2)
        potion_string = potion_string +" "+str(size*1500)
        file.write(potion_string + "\n")
        food_string = "0"
        food_string = food_string +" "+str(size*750)
        food_string = add_zeroes(food_string, size-3)
        food_string = food_string +" "+str(size*2000)
        file.write(food_string + "\n")
        for _ in range(size-2):
            multiplier: int = random.randint(100, 500)
            potion_use: int = random.uniform(1, 3)
            food_use: int = random.uniform(0, 4)
            file_string = str(multiplier*potion_use)
            file_string = file_string + " " + str(multiplier*food_use)
            file_string = add_zeroes(file_string, size-3)
            file_string = file_string + " " + str(multiplier)
            file.write(file_string + "\n")

def add_zeroes(string:str, num_zeroes:int) -> str:
    for _ in range(num_zeroes):
        string = string + " 0" 
    return string

write_pvm_matrix("test_economy_100.txt", 100)
write_pvm_matrix("test_economy_1000.txt", 1000)
write_pvm_matrix("test_economy_5000.txt", 5000)