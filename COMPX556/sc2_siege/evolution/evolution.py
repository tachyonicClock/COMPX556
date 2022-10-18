from dataclasses import dataclass
import random
from loguru import logger as log
import typing as t
import ray
import gp
from gp.fitness import Fitness, SquashFitness
from sc2_evaluator.evaluate import evaluate as sc2_evaluate

@dataclass
class Individual():
    chromosome: gp.Gene
    fitness: t.Optional[gp.Fitness] = None

    def __str__(self):
        return f'Individual(chromosome={self.chromosome}, fitness={self.fitness})'


class Population():
    _population: t.List[Individual]

    def __init__(self, 
            population: t.List[Individual], 
            to_fitness_score: SquashFitness):
        self._population = population
        self.to_fitness_score = to_fitness_score


    @staticmethod
    def initialize(
                 population_size: int,
                 chromosome_depth: int,
                 to_fitness_score: SquashFitness
                 ) -> 'Population':
        return Population([Individual(gp.initialise_chromosome(chromosome_depth))
                            for _ in range(population_size)], to_fitness_score)

    def select(self, selection_size: int) -> 'Population':
        """Select a subset of the population based on fitness"""
        sorted_population = sorted(
            self._population, 
            key=lambda x: self.to_fitness_score(x.fitness), reverse=True)
        return Population(sorted_population[:selection_size], self.to_fitness_score)

    def sample(self, sample_size: int) -> 'Population':
        """Sample a subset of the population with replacement"""
        return Population(random.choices(self._population, k=sample_size), self.to_fitness_score)

    def stochastic_mutate(self, func: t.Callable[[gp.Gene], gp.Gene], probability: float) -> 'Population':
        """Apply a function to a random subset of the population"""
        new_population = []
        for individual in self._population:
            if random.random() < probability:
                try:
                    individual = Individual(func(individual.chromosome))
                except gp.BadChromosome:
                    # Skip failed cross over attempts
                    pass
            new_population.append(individual)
        return Population(new_population, self.to_fitness_score)

    def stochastic_sex(self, func: t.Callable[[gp.Gene, gp.Gene], gp.Gene], probability: float) -> 'Population':
        """Apply a function to a random subset of the population"""
        new_population = []
        for individual in self._population:
            if random.random() < probability:
                parent_a = individual.chromosome
                parent_b = random.choice(self._population).chromosome
                try:
                    individual = Individual(func(parent_a, parent_b))
                except gp.BadChromosome:
                    # Skip failed cross over attempts
                    pass
        
            new_population.append(individual)
        return Population(new_population, self.to_fitness_score)

    def __iter__(self) -> t.Iterator[Individual]:
        return self._population.__iter__()

    def __len__(self) -> int:
        return len(self._population)

    def sum_fitness(self) -> float:
        return sum([self.to_fitness_score(x.fitness) for x in self._population])

    def average_fitness_score(self) -> float:
        return  self.sum_fitness() / len(self)

    def best_fitness_score(self) -> float:
        return max([self.to_fitness_score(x.fitness) for x in self._population])

    def average_minerals(self) -> float:
        return sum([x.fitness.minerals for x in self._population])/len(self)
    
    def average_gas(self) -> float:
        return sum([x.fitness.gas for x in self._population])/len(self)
    
    def average_time(self) -> float:
        return sum([x.fitness.time for x in self._population])/len(self)

    def best_individual(self) -> Individual:
        best_fitness: float = None
        best: Individual = None
        for individual in self._population:
            fitness = self.to_fitness_score(individual.fitness)
            if best_fitness == None or fitness > best_fitness:
                best_fitness = fitness
                best = individual
        return best


class PopulationEvaluator():

    def __init__(self,
        win_timeout: float,
        ready_time_limit: float
    ) -> None:
        self.win_timeout = win_timeout
        self.ready_time_limit = ready_time_limit

    @ray.remote
    def evaluate_chromosome(self, chromosome: gp.Gene) -> gp.Fitness:
        return sc2_evaluate(chromosome, realtime=False, win_timeout=self.win_timeout, ready_time_limit=self.ready_time_limit)

    def evaluate(self, population: Population) -> Population:
        """Evaluate the fitness of all chromosomes in the population"""
        fitness_ref = []

        log.info("Launching evaluation of population")
        for individual in population._population:
            if individual.fitness is None:
                fitness_ref.append(
                    self.evaluate_chromosome.remote(self, individual.chromosome))
            else:
                fitness_ref.append(ray.put(individual.fitness))

        log.info("Waiting for evaluation to complete")
        for i, ref in enumerate(fitness_ref):
            population._population[i].fitness = ray.get(ref)

        log.info("Evaluation complete")
        return population


    # def save(self, f: pickle._WritableFileobj):
    #     """Write the population to a file"""
    #     pickle.dump(self._population, f)

