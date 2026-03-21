from genetic_algorythym import genetic_evoution


def return_genetic_algorithm_parameters():
    """Return parameters for the genetic algorithm."""
    chrom_length = 10
    return {
        "population_size": 100,
        "chromosome_length": chrom_length,
        "mutation_rate": 1 / chrom_length,
        "crossover_rate": 0.7,
        "num_generations": 50,
        "selection_method": "tournament",
        "tournament_size": 5,
        "generations": 10,
    }


def main():
    """Main function to execute the genetic algorithm."""
    params = return_genetic_algorithm_parameters()
    ga = genetic_evoution(**params)
    result = ga.genetic_algorithm()
    print("Best chromosome:", result[0].genes)
    print("Best fitness:", result[1])


if __name__ == "__main__":
    main()
