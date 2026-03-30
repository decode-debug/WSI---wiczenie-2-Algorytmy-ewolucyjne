"""Evolution Strategy implementation for optimization problems."""

import numpy as np
import copy
import random
import uuid


def calibration_error(x):
    """Fitness function to minimize."""
    return 5 * len(x) + sum(xi**2 - 5 * np.cos(2 * np.pi * xi) for xi in x)


class chromosome:
    """
    Class representing a chromosome with
    real-valued genes and self-adaptive sigma.

            !!! DANGER !!!
    Before execution set Class variables:
        chromosome.num_params = <int>
        chromosome.sigma_lower_bound = <float>
    """

    num_params = None
    sigma_lower_bound = None
    min_gene_val = None
    max_gene_val = None

    def __init__(self, genes, sigma):
        self.genes = np.array(genes, dtype=float)
        self.sigma = sigma
        self.fitness = calibration_error(self.genes)
        self.number = uuid.uuid4()  # Unique identifier for the chromosome

    def mutate(self):
        """Gaussian mutation with sigma self-adaptation (always occurs)."""
        # generate a random scalar using tag for sigma adaptation
        tau = 1.0 / np.sqrt(self.num_params)
        self.sigma = self.sigma * np.exp(np.random.normal(0, tau))

        # Ensure sigma does not go below the specified lower bound
        self.sigma = max(self.sigma, self.sigma_lower_bound)

        # Mutate genes with Gaussian noise and clip to valid range
        noise = np.random.normal(0, self.sigma, size=self.num_params)
        self.genes += noise
        self.genes = np.clip(self.genes, self.min_gene_val, self.max_gene_val)

        # Recalculate fitness after mutation
        self.fitness = calibration_error(self.genes)

    def __add__(self, other):
        """
        Performs arithmetic crossover between two parents to produce offspring.
        Usage: child1, child2 = parent1 + parent2
        """
        if not isinstance(other, chromosome):
            raise TypeError(
                "Operands must be instances of the chromosome class."
            )

        # Generate two random alphas to create two distinct children
        alpha1 = random.random()
        alpha2 = random.random()

        child1_genes = alpha1 * self.genes + (1 - alpha1) * other.genes
        child1_sigma = alpha1 * self.sigma + (1 - alpha1) * other.sigma

        child2_genes = alpha2 * self.genes + (1 - alpha2) * other.genes
        child2_sigma = alpha2 * self.sigma + (1 - alpha2) * other.sigma

        return (
            chromosome(child1_genes, child1_sigma),
            chromosome(child2_genes, child2_sigma),
        )


class evolution_strategy:
    """Class representing the (mu, lambda) evolutionary strategy."""

    def __init__(self, mu, config):
        self.mu = mu
        self.lambda_ = config["lambda_"]
        self.num_params = config["num_params"]
        self.generations = config["generations"]
        self.min_gene_val = config["min_gene_val"]
        self.max_gene_val = config["max_gene_val"]
        self.min_sigma = config["min_sigma"]
        self.max_sigma = config["max_sigma"]
        self.population = []

    def generate_population(self):
        """Generates the initial population of size mu."""
        population = []
        for _ in range(self.mu):
            genes = np.random.uniform(
                self.min_gene_val, self.max_gene_val, self.num_params
            )
            sigma = np.random.uniform(self.min_sigma, self.max_sigma)
            population.append(chromosome(genes, sigma))
        return population

    def evolution_algorithm(self):
        """Main loop of the (mu, lambda) algorithm."""
        self.population = self.generate_population()

        best_global_chromosome = min(self.population, key=lambda x: x.fitness)
        best_global_fitness = best_global_chromosome.fitness
        history_best = []

        for _ in range(self.generations):
            offspring = []

            # Generate lambda offspring
            while len(offspring) < self.lambda_:
                p1, p2 = random.sample(self.population, 2)

                child1, child2 = p1 + p2

                child1.mutate()
                child2.mutate()

                offspring.extend([child1, child2])

            # Ensure we strictly have lambda_ offspring if odd numbers are used
            offspring = offspring[: self.lambda_]

            # (mu, lambda) selection: select best mu from offspring only
            offspring.sort(key=lambda x: x.fitness)
            self.population = offspring[: self.mu]

            # find best one
            current_best = self.population[0]
            current_best_fitness = current_best.fitness

            if current_best_fitness < best_global_fitness:
                best_global_fitness = current_best_fitness
                best_global_chromosome = copy.deepcopy(current_best)

            history_best.append(best_global_fitness)

        return best_global_chromosome, best_global_fitness, history_best
