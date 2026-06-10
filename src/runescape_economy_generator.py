## TODO: The economy generator
import pathlib
import random

def write_pvm_matrix(filename: str, size: int) -> None:
    thisdir = pathlib.Path(__file__).parent.resolve()
    DAT_DIR = thisdir.parent / "dat"
    current_path = DAT_DIR / filename
    with open(current_path, "a") as file:
        potion_string = str(size*500)                       #first element in every file will be the overload potion equation. the ingredients to make potions are often dropped by bosses, so potions go into their own production.
        potion_string = potion_string+" "+str(size*300)     #bosses drop potion ingredients and food is used to kill bosses, hence they are used in production in practice.
        potion_string = add_zeroes(potion_string, size-2)   #boss drops don't go into production of potions, so they're zero.
        potion_string = potion_string +" "+str(size*2000)   #not chosen arbitrarily - this ensures that the total number of potions produced is larger than the amount consumed by the rest of the economy
        file.write(potion_string + "\n")
        food_string = str(size*100)                         #second line is the food equation. potions are used to kill bosses and bosses often drop food ingredients, so they're used in production.
        food_string = food_string +" "+str(size*750)        #similarly, the ingredients to make food items are often dropped by bosses, so they go into their own production.
        food_string = add_zeroes(food_string, size-2)       
        food_string = food_string +" "+str(size*3000)
        file.write(food_string + "\n")
        for _ in range(size-2):                             #this writes the rest of the matrix.
            multiplier: int = random.randint(100, 500)      #sets a random 'multiplier' of how many of these boss drops were produced in the pvm economy.
            potion_use: int = random.uniform(1, 3)          #sets a random number of potion doses used per boss kill.
            food_use: int = random.uniform(0, 4)            #ditto for food.
            file_string = str(multiplier*potion_use)
            file_string = file_string + " " + str(multiplier*food_use)
            file_string = add_zeroes(file_string, size-2)
            file_string = file_string + " " + str(multiplier)
            file.write(file_string + "\n")

def add_zeroes(string:str, num_zeroes:int) -> str:
    """
    Helper function that appends zeroes to the end of a string. Takes in a string and the number
    of zeroes to append, returns that string with the zeroes appened.
    """
    for _ in range(num_zeroes):
        string = string + " 0" 
    return string

write_pvm_matrix("test_economy_10.txt", 10)
write_pvm_matrix("test_economy_100.txt", 100)
write_pvm_matrix("test_economy_1000.txt", 1000)
write_pvm_matrix("test_economy_5000.txt", 5000)