
from evolution.evolution import Population
from tensorboard.summary import Writer
import pickle

import gp

class LogCallback():

    def after_pop_eval(self, population: Population):
        pass 



class Tensorboard(LogCallback):

    def __init__(self, log_dir: str):
        self.writer = Writer(log_dir)

    def after_pop_eval(self, generation: int, population: Population):        
        best = population.best_individual()
        self.writer.add_scalar('fitness/average', population.average_fitness_score(), generation)
        self.writer.add_scalar('fitness/best', population.best_fitness_score(), generation)

        self.writer.add_scalar('gas/average', population.average_gas(), generation)
        self.writer.add_scalar('gas/best', best.fitness.gas, generation)

        self.writer.add_scalar('time/average', population.average_time(), generation)
        self.writer.add_scalar('time/best', best.fitness.time, generation)

        self.writer.add_scalar('minerals/average', population.average_minerals(), generation)
        self.writer.add_scalar('minerals/best', best.fitness.minerals, generation)
        # self.writer.image('best_individual', gp.plot_gene(best.chromosome), generation)



class SaveGeneration(LogCallback):
    
    def __init__(self, save_dir: str):
        self.save_dir = save_dir

    def after_pop_eval(self, generation: int, population: Population):
        with open(f'{self.save_dir}/generation_{generation:04d}.pkl', 'wb') as f:
            pickle.dump(population, f)