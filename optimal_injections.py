# Creator: Zoey Samples
# Creation Date: Sept 3, 2025
# Updated: Sept 9, 2025
#
# This script runs a simulation of the usage of multi-dose injectable
# medication vials. The premise is that the medication is used safely by
# multiple people, and that they each take a constant, recurring dosage over
# time. If there is not enough medication left in the vial at the time of an
# injection, it is thrown away and considered wasted medication. Another vial
# is opened, and the simulation continues.
# 
# This simulation considers a range of possible doses and days between doses,
# determined by the user-specified parameters, for each person listed. It
# considers every possible permutation of doses, within these parameters, so
# as to minimize total medication waste. When the simulation is concluded, it
# displays the most optimal outcomes.

import numpy as np
import itertools
from simulator import InjectionSimulator

'''User-specified parameters:

num_vials (int): The number of medication vials to simulate per trial.
vial_volume (float): The volume (mL) of the medication vial.
step (float): The amount to increment daily dosage through different trials
of the simulation. The default is 0.001. More precision than this is unlikely
to show any additional unique results.
num_outcomes (int): How many outcomes to print at the conclusion of simulation.
people (list): This list becomes populated with the information for each
person.
person1, person2, ... (dicts): A dict that contains the person's:
    name (string),
    dose_unit (array of floats): a range of the amount of medication they 
    use on average (mL/day)
    dose_freq (array of ints): The interval (days) between injections.
'''

num_vials = 20
vial_volume = 5.0   # mL
step = 0.001
num_outcomes = 5

# Create a dict for each person and add them to the list of people.
people = []
person1 = {
    "name": "Alice",
    "dose_unit": np.arange(0.038, 0.042, step=step),
    "dose_freq": np.array([7,8])
}
people.append(person1)

person2 = {
    "name": "Bob",
    "dose_unit": np.arange(0.06, 0.063, step=step),
    "dose_freq": np.array([4,5])
}
people.append(person2)

person3 = {
    "name": "Charlie",
    "dose_unit": np.arange(0.049, 0.052, step=step),
    "dose_freq": np.array([5,6,7])
}
people.append(person3)

# Make a list of arrays, each containing every value of dose_unit and dose_freq
# per person, so that we can iterate our for loop over every permutation.
total_people = len(people)
iter_list = []
name_list = []
for idx in range(total_people):
    iter_list.append(people[idx]["dose_unit"])
    iter_list.append(people[idx]["dose_freq"])
    name_list.append(people[idx]["name"])

# Iterate over every dosage permutation.
result_list = []
early_terminations = 0
for dose_info in itertools.product(*iter_list):
    trial = InjectionSimulator(total_people, name_list, dose_info,
                            num_vials=num_vials, vial_volume=vial_volume)
    trial_result = trial.run_simulation()

    # Keep only unique outcomes.
    if (trial_result not in result_list) and (trial_result != None):
        result_list.append(trial_result)
    elif trial_result == None:
        early_terminations += 1

if early_terminations > 0:
    print("{} trials were aborted.".format(early_terminations))
    print("This is likely a result of having a dose larger than the vial",
           "volume or a negative dose.", "\n")

# If all trials were aborted, then end the program.
if result_list == []:
    raise ValueError("There is no trial data due to early terminations.")

# Do not print in scientific notation.
np.set_printoptions(suppress=True)

# Sort the results by the amount of medication wasted.
result_list = sorted(result_list, key=lambda x: x[0])

# Print the results.
print("The least wasteful dosage schedules are:")
for i in range(num_outcomes):
    print("Optimal outcome:", i+1)
    print("Total wasted medicine: ", f"{result_list[i][0]:.2f}", " mL")
    print("In {} days, you will have used {} vials".format(
        result_list[i][1], num_vials))
    
    # Print dosage info for each person in the original order
    print_info = result_list[i][2]
    for j in range(total_people):
        for k in range(total_people):
            # Find the index that matches the original order
            if print_info[k]["name"] == name_list[j]:
                idx = k
        print("{}'s dosage: {:.2f} mL every {} days".format(
            print_info[idx]["name"], print_info[idx]["dosage"],
            print_info[idx]["frequency"]))
    print("")