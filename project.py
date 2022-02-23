"""
TITLE:          project.py
DIRECTORY:      Reinforcement Racer project.
DESCRIPTION:    Main project file for the reinforcement
                racer project - one of two primary projects
                for DU's ACS 2500: Core Apps of AI course.
MUTABILITY:     This file contains challenges that must be
                resolved for full project completion. 
"""


import numpy as np
import matplotlib.pyplot as plt
import os, sys, math, random
import neat, pygame

from structures.structures import CarAgent


AGENT_PARAMETERS = {
    "X": 60, 
    "Y": 60
}

ENVIRONMENT_PARAMETERS = {
    "WIDTH":    1920,
    "HEIGHT":   1080
}

BORDER_COLOR = (255, 255, 255, 255)

current_generation = 0


def racecar_simulator(genomes, configurations):
    """ Custom function to conduct simulated reinforcement learning using naive self-driving car object. """
    models, agents = list(), list()

    pygame.init(); screen = pygame.display.set_mode((ENVIRONMENT_PARAMETERS["WIDTH"], ENVIRONMENT_PARAMETERS["HEIGHT"]), 
                                                     pygame.FULLSCREEN)
    
    for iteration, genome in genomes:
        model = neat.nn.FeedForwardNetwork.create(genome, configurations)
        models.append(model)
        genome.fitness = 0

        agents.append(CarAgent(agent_parameters=AGENT_PARAMETERS,
                               environment_parameters=ENVIRONMENT_PARAMETERS,
                               border_color=BORDER_COLOR))

    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    environment = pygame.image.load("assets/environments/map03.png").convert()

    global current_generation
    current_generation += 1

    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        for iteration, agent in enumerate(agents):
            output = models[iteration].activate(agent.get_actions())
            choice = output.index(max(output))
            if choice == 0:
                agent.angle += 10
            elif choice == 1:
                agent.angle -= 10
            elif choice == 2:
                if agent.speed - 2 >= 12:
                    agent.speed -= 2
            else:
                agent.speed += 2

        still_alive = 0
        for iteration, agent in enumerate(agents):
            if agent.is_alive():
                still_alive += 1
                agent.play_game(environment)
                genomes[iteration][1].fitness += agent.get_rewards()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40:
            break

        screen.blit(environment, (0, 0))
        for agent in agents:
            if agent.is_alive():
                agent.draw(screen)

        text = generation_font.render("Generation: {}".format(str(current_generation)),
                                      True,
                                      (0, 0, 0))
        text_rectangle = text.get_rect()
        text_rectangle.center = (900, 450)
        screen.blit(text, text_rectangle)

        text = alive_font.render("Still Alive: {}".format(str(still_alive)),
                                 True,
                                 (0, 0, 0))
        text_rectangle = text.get_rect()
        text_rectangle.center = (900, 490)
        screen.blit(text, text_rectangle)

        pygame.display.flip(); clock.tick(60)

if __name__ == "__main__":
    PATH_CONFIG = "./config.txt"
    configurations = neat.config.Config(neat.DefaultGenome,
                                        neat.DefaultReproduction,
                                        neat.DefaultSpeciesSet,
                                        neat.DefaultStagnation,
                                        PATH_CONFIG)
    
    population = neat.Population(configurations)
    population.add_reporter(neat.StdOutReporter(True))
    population_statistics = neat.StatisticsReporter()
    population.add_reporter(population_statistics)

    population.run(racecar_simulator, 1000)