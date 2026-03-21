"""Genetic algorithm implementation for optimization problems."""

import random
import numpy as np
import uuid
import copy


def calibration_error(x):
    """Function to minimize."""
    return 5 * len(x) + sum(xi**2 - 5 * np.cos(2 * np.pi * xi) for xi in x)


class chromosome:
    """Class representing a chromosome."""

    def __init__(self, genes):
        self.genes = genes
        self.fitness = calibration_error(genes)
        self.number = uuid.uuid4()  # Unique identifier for the chromosome

    def mutate(self, mutation_rate):
        """Mutates a chromosome based on the mutation rate."""
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                self.genes[i] = 1 - self.genes[i]  # Flip the bit

    def __add__(self, other):
        """
        Performs two-point crossover between two parents to produce offspring.
        Usage: child1, child2 = parent1 + parent2
        """
        if not isinstance(other, chromosome):
            raise TypeError(
                "Można dodawać do siebie tylko obiekty klasy chromosome."
            )

        genes1 = self.genes
        genes2 = other.genes
        length = len(genes1)

        # random points of cut
        p1, p2 = sorted(random.sample(range(1, length), 2))

        child1_genes = genes1[:p1] + genes2[p1:p2] + genes1[p2:]
        child2_genes = genes2[:p1] + genes1[p1:p2] + genes2[p2:]

        return chromosome(child1_genes), chromosome(child2_genes)


class genetic_evoution:
    """Class representing the genetic algorithm."""

    def __init__(
        self,
        population_size,
        chromosome_length,
        mutation_rate,
        crossover_rate,
        num_generations,
        selection_method,
        tournament_size,
        generations,
    ):
        self.population_size = population_size
        self.chromosome_length = chromosome_length
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.num_generations = num_generations
        self.selection_method = selection_method
        self.tournament_size = tournament_size
        self.generations = generations
        self.population = []

    def generate_population(self):
        """Generates a random population of binary chromosomes."""
        return [
            chromosome(
                [random.randint(0, 1) for _ in range(self.chromosome_length)]
            )
            for _ in range(self.population_size)
        ]

    def tournament_selection(self):
        """Selects a parent using tournament selection."""
        selected_fighters = random.sample(
            self.population, self.tournament_size
        )
        best_fighter = min(selected_fighters, key=lambda x: x.fitness)
        return best_fighter

    def hybridize(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            child1, child2 = parent1 + parent2
        else:
            # if crossover not possible copy parents
            child1 = chromosome(parent1.genes.copy())
            child2 = chromosome(parent2.genes.copy())
        return child1, child2

    def genetic_algorithm(self):
        """Main function to run the genetic algorithm."""
        self.population = self.generate_population()

        # find best one
        best_global_chromosome = min(self.population, key=lambda x: x.fitness)
        best_global_fitness = best_global_chromosome.fitness

        for generation in range(self.generations):

            new_population = []

            while len(new_population) < self.population_size:
                # parents selection
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()

                # hybridization
                child1, child2 = self.hybridize(parent1, parent2)

                # mutation
                child1.mutate(self.mutation_rate)
                child2.mutate(self.mutation_rate)

                # add children to population
                new_population.extend([child1, child2])

            # double check population length and define new population
            self.population = new_population[: self.population_size]

            # find best one
            best_local_chromosome = min(
                self.population, key=lambda x: x.fitness
            )
            best_local_fitness = best_local_chromosome.fitness

            # find best child
            if best_local_fitness < best_global_fitness:
                best_global_fitness = best_local_fitness
                best_global_chromosome = copy.deepcopy(best_local_chromosome)

            # log evoultion
            if generation % 1 == 0 or generation == self.generations - 1:
                print(
                    f"Pokolenie {generation:3d} "
                    f"| Najlepszy dotychczasowy wynik (błąd):"
                    f" {best_global_fitness:.4f}"
                )

        # Koniec pętli (t <- t + 1 robi się automatycznie w pętli for)
        return best_global_chromosome, best_global_fitness
