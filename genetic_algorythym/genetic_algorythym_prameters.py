import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from genetic_algorythym.genetic_algorythym import (  # noqa: E402
    genetic_evolution,
)


def return_genetic_algorithm_parameters():
    """Return parameters for the genetic algorithm."""
    bits_per_param = 8
    num_params = 10
    chrom_length = num_params * bits_per_param

    return {
        "num_params": num_params,  # Dodane
        "bits_per_param": bits_per_param,  # Dodane
        "population_size": 100,
        "chromosome_length": chrom_length,
        "mutation_rate": 1 / chrom_length,
        "crossover_rate": 0.7,
        "num_generations": 50,
        "selection_method": "tournament",
        "tournament_size": 5,
        "generations": 100,
    }


def clear_screen():
    """Clears the terminal screen for a clean UI."""
    os.system("cls" if os.name == "nt" else "clear")


def wait_for_double_enter():
    """Waits for the user to press the Enter key twice consecutively."""
    enters = 0
    while enters < 2:
        user_input = input()
        if user_input == "":
            enters += 1
        else:
            enters = 0


def main():
    """Main function to execute the genetic algorithm with a CLI interface."""
    clear_screen()

    # --- 1. Welcome Screen ---
    print("=" * 60)
    print(" " * 15 + "GENETIC ALGORITHM ENGINE")
    print("=" * 60)
    print("\nWelcome! The environment parameters are loaded and ready.")
    print("The system is prepared to begin the evolutionary process.\n")

    print("Press [ENTER] twice to start...")
    wait_for_double_enter()

    # --- 2. Transition ---
    clear_screen()
    print("Initializing population and starting evolution...\n")
    time.sleep(0.5)

    # --- 3. Execute Core Logic ---
    try:
        params = return_genetic_algorithm_parameters()
        ga = genetic_evolution(**params)

        result = ga.genetic_algorithm()

        # --- 4. Display Results ---
        print("\nEVOLUTION COMPLETE")
        print("-" * 60)
        print(f"Best chromosome: {result[0].genes}")
        print(f"Best fitness:    {result[1]}")
        print("-" * 60)

        print("\nPress [ENTER] to exit the program.")
        input()

    except NameError as e:
        print(f"\nError: {e}")
        print(
            "Make sure your genetic algorithm functions"
            " and classes are defined above main()."
        )
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
