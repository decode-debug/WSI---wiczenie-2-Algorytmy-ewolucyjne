import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from evolution_algorythym.evolution_algorytym import (  # noqa: E402
    evolution_strategy,
    chromosome,
)


def return_evolutionary_strategy_parameters():
    """Return parameters for the evolutionary strategy algorithm (mu, 100)."""
    evaluations_limit = 9000
    lambda_ = 100
    num_params = 10

    return {
        "num_params": num_params,
        "lambda_": lambda_,
        "mu_values": [5, 15, 30],
        "generations": evaluations_limit // lambda_,
        "min_gene_val": -5.0,
        "max_gene_val": 5.0,
        "min_sigma": 0.5,
        "max_sigma": 2.0,
        "sigma_lower_bound": 1e-5,
    }


def main():
    # Load configuration
    config = return_evolutionary_strategy_parameters()

    # Inject class variables required by chromosome
    chromosome.num_params = config["num_params"]
    chromosome.sigma_lower_bound = config["sigma_lower_bound"]

    results = {}

    # Test for different values of mu
    for mu in config["mu_values"]:
        print(f"Running Evolution Strategy for mu = {mu}...")
        es = evolution_strategy(mu=mu, config=config)
        best_ind, best_fitness, history = es.evolution_algorithm()
        results[mu] = history
        print(f"Best fitness found (error): {best_ind.fitness:.4f}\n")


if __name__ == "__main__":
    main()
