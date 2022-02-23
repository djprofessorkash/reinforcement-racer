"""
TITLE:          structures.py
DIRECTORY:      Reinforcement Racer project.
DESCRIPTION:    Supplemental file containing necessary 
                data structures for the completion of 
                ACS 4511's Reinforcement Racer project.
MUTABILITY:     This file contains challenges that must be
                resolved for full project completion. (NOTE:
                You may answer relevant TODOs by creating
                additional docstrings and commented segments
                that contain your respective answers.)
"""

# Relative Imports and Instantiations
import os, sys, math, random
import neat, pygame


# TODO: Minimal comments are provided for this code in order to
#       assess your capabilities in reverse-engineering and 
#       understanding complex AI scripting. Write additional
#       comments throughout this data structure file as needed
#       to clarify both your and others' understandings.

class CarAgent:
    """ Custom self-driving car object for reinforcement learning. """
    def __init__(self, agent_parameters, environment_parameters, border_color):
        """ Initialization method to configure setup parameters for agent and environment. """
        # Set State Info and Border Colors for Racetrack
        self.border_color =             border_color
        self.agent_parameters =         agent_parameters
        self.environment_parameters =   environment_parameters

        # Set Racecar Sprites
        self.sprite = pygame.image.load("assets/agents/car01.png").convert()
        self.sprite = pygame.transform.scale(self.sprite, (self.agent_parameters["X"],
                                                           self.agent_parameters["Y"]))
        self.rotated_sprite = self.sprite

        # Initialize Racecar Position on Track
        self.position = [830, 920]
        self.angle, self.speed = 0, 0

        # Disable Racecar Training Until Needed
        self.speed_set = False

        # Initialize Center of Racecar Sprite Object
        self.center = [self.position[0] + self.agent_parameters["X"] / 2,
                       self.position[1] + self.agent_parameters["Y"] / 2]

        # Setup Path Detection Algorithms for "Looking" In Front of the Racecar
        self.radars, self.drawing_radars = list(), list()

        # Set Car Survivability Variable
        self.alive = True

        # Set Distance/Time Metrics
        self.distance, self.time = 0, 0

    def __draw_radar__(self, screen):
        """ Helper method to draw sensors/radars for improved navigability. """
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def draw(self, screen):
        """ Major method to impose sprite across simulated environment screen. """
        screen.blit(self.rotated_sprite, self.position)
        self.__draw_radar__(screen)

    def detect_collision(self, environment):
        """ Major method to perform collision detection for agent across environment space. """
        self.alive = True
        for corner in self.corners:
            if environment.get_at((int(corner[0]), int(corner[1]))) == self.border_color:
                self.alive = False; break

    def __update_coordinates__(self, degree, length):
        """ Helper method to calculate updated coordinates with deltas in X and Y. """
        # TODO: Explain what the following three lines of code are doing.
        #       What values are we trying to calculate and what impact does
        #       that data have on our overall project?
        dX = math.cos(math.radians(360 - (self.angle + degree))) * length
        dY = math.sin(math.radians(360 - (self.angle + degree))) * length
        return int(self.center[0] + dX), int(self.center[1] + dY)

    def __calculate_distance__(self, X, Y):
        """ Helper method to calculate Euclidean distance between original and updated coordinates. """
        ΔX, ΔY = X - self.center[0], Y - self.center[1]
        # TODO: Utilize the `math` repository and your understanding
        #       of basic algebra to complete the Euclidean distance
        #       function algorithm below. (HINT: It's the basic 
        #       distance function you learn in algebra!)
        return None

    def check_radar(self, degree, environment):
        """ Major method to check and validate positions of car respective to track-path borders. """
        length = 0

        X, Y = self.__update_coordinates__(degree, length)
      
        while not environment.get_at((X, Y)) == self.border_color and length < 300:
            length += 1

            X, Y = self.__update_coordinates__(degree, length)
        
        distance = self.__calculate_distance__(X, Y)
        self.radars.append([(X, Y), distance])

    def __get_state__(self, length):
        """ Helper method to retrieve environment state data using simulation timesteps. """
        # TODO: This is a deceptively complex algorithm at play. Explain
        #       what information is being created and iterated across and 
        #       why this matters for our reinforcement learning algorithm.
        TOP_LEFT_OFFSET, TOP_RIGHT_OFFSET, BOTTOM_LEFT_OFFSET, BOTTOM_RIGHT_OFFSET = 30, 150, 210, 330
        corners = list()
        for offset in [TOP_LEFT_OFFSET, TOP_RIGHT_OFFSET, BOTTOM_LEFT_OFFSET, BOTTOM_RIGHT_OFFSET]:
            X, Y = self.__update_coordinates__(offset, length)
            corners.append([X, Y])
        return corners

    def play_game(self, environment):
        """ Major method to update car-environment positions with respective state data. """
        if not self.speed_set:
            self.speed, self.speed_set = 20, True
        
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], self.environment_parameters["WIDTH"] - 120)

        self.distance += self.speed; self.time += 1

        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], self.environment_parameters["WIDTH"] - 120)

        self.center = [int(self.position[0]) + self.agent_parameters["X"] / 2,
                       int(self.position[1]) + self.agent_parameters["Y"] / 2]
        
        length = 0.5 * self.agent_parameters["X"]
        self.corners = self.__get_state__(length)

        self.detect_collision(environment); self.radars.clear()

        for window in range(-90, 120, 45):
            self.check_radar(window, environment)

    def get_actions(self):
        """ Major method to obtain state action data for playing racecar simulation. """
        # TODO: Our `actions` object is a deceptively important data
        #       structures. Explain what this object represents and 
        #       how this data is interpreted/used by our learning algorithm.
        radars, actions = self.radars, [0, 0, 0, 0, 0]
        for iteration, radar in enumerate(radars):
            actions[iteration] = int(radar[1] / 30)
        return actions
    
    def is_alive(self):
        """ Major method to manually check car survival status. """
        return self.alive

    def get_rewards(self):
        """ Major method to calculate reward schema. """
        # TODO: Explain how our rewarding schema is expressly calculated.
        # TODO: Are there any other/better ways of selecting rewards for
        #       our reinforcement algorithm?
        return self.distance / (self.agent_parameters["X"] / 2)

    def rotate_center(self, image, angle):
        """ Major method to rotate environmental image. """
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image
