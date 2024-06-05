# run_simulation.py

import sys
from simulation_manager import SimulationManager

def main():
    new_recursion_limit = 3000  # Set the new recursion limit

    # Check if the new recursion limit is within the allowable range
    if new_recursion_limit > sys.getrecursionlimit():
        print("Warning: New recursion limit is higher than the default limit of ", sys.getrecursionlimit(), ".")

    sys.setrecursionlimit(new_recursion_limit)  # Set the new recursion limit

    print("New recursion limit:", sys.getrecursionlimit())  # Print the updated recursion limit

    manager = SimulationManager()
    print("Running: ", manager.STAGE[0])
    manager.simulate(manager.STAGE[0])
    manager.reset_simulation_data()

    print("Running: ", manager.STAGE[1])
    manager.optimize_resources(manager.STAGE[1])
    manager.reset_simulation_data()

    print("Running: ", manager.STAGE[2])
    manager.simulate(manager.STAGE[2])
    manager.reset_simulation_data()

    manager.report()

if __name__ == "__main__":
    main()
