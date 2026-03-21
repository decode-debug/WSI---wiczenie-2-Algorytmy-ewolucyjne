import numpy as np
import copy
import random


def calibration_error(x):
    """Fitness function to minimize."""
    return 5 * len(x) + sum(xi**2 - 5 * np.cos(2 * np.pi * xi) for xi in x)


class RealChromosome:
    """
    Class representing a chromosome with
    real-valued genes and self-adaptive sigma.



            !!! DANEGER !!!
    Class variables set before execution:
        RealChromosome.num_params = <int>
        RealChromosome.sigma_lower_bound = <int>
    """
    num_params = None
    sigma_lower_bound = None

    def __init__(self, genes, sigma):
        self.genes = np.array(genes, dtype=float)
        self.sigma = sigma
        self.fitness = calibration_error(self.genes)

    def mutate(self):
        """Gaussian mutation with sigma self-adaptation."""
        tau = 1.0 / np.sqrt(self.num_params)
        self.sigma = self.sigma * np.exp(np.random.normal(0, tau))
        self.sigma = max(self.sigma, self.sigma_lower_bound)

        noise = np.random.normal(0, self.sigma, size=self.num_params)
        self.genes += noise
        self.fitness = calibration_error(self.genes)


def arithmetic_crossover(parent1, parent2):
    """Performs arithmetic crossover between two parents."""
    alpha = random.random()
    child_genes = alpha * parent1.genes + (1 - alpha) * parent2.genes
    child_sigma = alpha * parent1.sigma + (1 - alpha) * parent2.sigma

    return RealChromosome(child_genes, child_sigma)


class EvolutionStrategy:
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

    def initialize_population(self):
        """Generates the initial population of size mu."""
        self.population = []
        for _ in range(self.mu):
            genes = np.random.uniform(
                self.min_gene_val, self.max_gene_val, self.num_params
            )
            sigma = np.random.uniform(self.min_sigma, self.max_sigma)
            self.population.append(RealChromosome(genes, sigma))

    def run(self):
        """Main loop of the (mu, lambda) algorithm."""
        self.initialize_population()

        best_global_chromosome = min(self.population, key=lambda x: x.fitness)
        history_best = []

        for _ in range(self.generations):
            offspring = []

            for _ in range(self.lambda_):
                p1, p2 = random.sample(self.population, 2)
                child = arithmetic_crossover(p1, p2)
                child.mutate()
                offspring.append(child)

            # (mu, lambda) selection: select best mu from offspring only
            offspring.sort(key=lambda x: x.fitness)
            self.population = offspring[: self.mu]

            current_best = self.population[0]
            if current_best.fitness < best_global_chromosome.fitness:
                best_global_chromosome = copy.deepcopy(current_best)

            history_best.append(best_global_chromosome.fitness)

        return best_global_chromosome, history_best
