import pygame
import random
from random import random, randint, choice
from pygame.locals import KEYDOWN, QUIT
import matplotlib.pyplot as plt
import numpy as np
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

all_agents = pygame.sprite.Group()
all_players = []

class Disease():
    def __init__(self, name, transmissivity, deathrate, duration, pop):
        self.name = name
        self.transmissivity = transmissivity
        self.duration = duration*50*(100/pop)
        self.deathrate = deathrate
        self.pop = pop

class Environment():
    def __init__(self, population, socialdistancing):
        self.population = population
        self.agent_names = ['a' + str(i) for i in range(self.population)]
        self.agents = self.agent_names
        self.socialdistancing = socialdistancing
    
    def populate(self):
        for i in range(len(self.agents)):
            self.agents[i] = Agent('S', self.socialdistancing)
            all_players.append(self.agents[i])
            all_agents.add(self.agents[i])
        self.agents[0] = Agent('I', 0)

class Agent(pygame.sprite.Sprite):
    def __init__(self, condition, sd):
        super(Agent, self).__init__()
        self.condition = condition
        self.update_condition()
        self.rect = self.surf.get_rect()
        self.position = self.x, self.y = (randint(0, SCREEN_WIDTH - 20), randint(0, SCREEN_HEIGHT - 20))
        self.velocity = [1, 1]
        self.radius = (self.surf.get_width()) / 2
        self.life = 0
        self.sd = sd
        if randint(1, 100) <= self.sd and not self.condition == 'I':
            self.sd == True
            self.velocity = [0, 0]

    def update_condition(self):
        if self.condition == 'S':
            self.surf = pygame.image.load(r'assets\smiler.png')
        elif self.condition == 'R':
            self.surf = pygame.image.load(r'assets\sunglass2.png')
        elif self.condition == 'I':
            self.surf = pygame.image.load(r'assets\sicker.png')
        elif self.condition == 'D':
            self.surf = pygame.image.load(r'assets\coffin2.png')

    def bounce(self):
        if not self.condition == 'D':
            self.velocity[0] = -self.velocity[0]
            self.velocity[1] = randint(-1, 1)
    
    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def age(self):
        self.life += 1

    def move(self, env, corona):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        #self.update_condition()
        if self.sd == True:
            self.velocity = [0, 0]
        if self.x >= SCREEN_WIDTH - 10:
            self.velocity[0] = -self.velocity[0]
        if self.x <= 0:
            self.velocity[0] = -self.velocity[0]
        if self.y >= SCREEN_HEIGHT - 10:
            self.velocity[1] = -self.velocity[1]
        if self.y <= 0:
            self.velocity[1] = -self.velocity[1]
        for agent in env.agents:
            if not agent is self and self.distance(self.x, self.y, agent.x, agent.y) <= self.radius + agent.radius and not agent.condition == 'D':
                if agent.condition == 'I' and self.condition == 'S':
                    if randint(1, 100) < corona.transmissivity:
                        self.condition = 'I'
                        self.life = 0
                        self.update_condition()
                if not self.sd == True:
                    self.bounce()
        if self.life < corona.duration:
            self.age()
        if self.life >= corona.duration and self.condition == 'I':
            if randint(0, 100) <= corona.deathrate:
                self.condition = 'D'
                self.velocity = [0, 0]
            else:
                self.condition = 'R'
            self.update_condition()
        self.position = self.x, self.y

def main(corona, env):
    icon = pygame.image.load(r'assets\virus_icon.png')
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Simulating Infectious Disease')
    pygame.init()
    clock = pygame.time.Clock()
    myfont = pygame.font.SysFont('Comic Sans MS', 18)
    

    #corona = Disease('SARS-CoV-2', 90, 4, 500)
    #env = Environment(60)
    env.populate()
    #player = Agent('R')

    epidemic = True

    infected = []
    susceptible = []
    recovered = []
    died = []
    days = 0
    day = 0
    xi = []
    while epidemic:

        for event in pygame.event.get():
            if event.type == QUIT:
                epidemic = False

        screen.fill((255, 255, 255))

        for i in range(len(env.agents)):
            infecteds = len([agent for agent in env.agents if agent.condition == 'I'])
            susceptibles = len([agent for agent in env.agents if agent.condition == 'S'])
            recovereds = len([agent for agent in env.agents if agent.condition == 'R'])
            deads = len([agent for agent in env.agents if agent.condition == 'D'])
            susceptible.append(susceptibles)
            infected.append(infecteds)
            recovered.append(recovereds)
            died.append(deads)

            s_text = myfont.render(str(('Susceptible: ' + str(susceptibles))), False, (0, 0, 0))
            d_text = myfont.render(str(('Deaths: '+ str(deads))), False, (0, 0, 0))
            r_text = myfont.render(str(('Recovered: '+ str(recovereds))), False, (0, 0, 0))
            i_text = myfont.render(str(('Infected: '+ str(infecteds))), False, (0, 0, 0))
            days_elapsed = myfont.render(str(('Days Elapsed: '+ str(day))), False, (0, 0, 0))
            if infecteds == 0:
                epidemic = False

            screen.blit(env.agents[i].surf, env.agents[i].position)
            env.agents[i].move(env, corona)
            screen.blit(s_text,(0,0))
            screen.blit(d_text,(0,30))
            screen.blit(r_text,(0,60))
            screen.blit(i_text,(0,90))
            screen.blit(days_elapsed,(645,0))

            clock.tick(1100)
            days += 1
            d = days/5000
            day = round(days/5000)
            xi.append(d)
            


        pygame.display.flip()

    plt.figure(num='Results')
    plt.title(corona.name)
    plt.plot(xi,infected, '-r', label='Infected', color='red')
    plt.plot(xi,susceptible, '-b', label='Susceptible', color='blue')
    plt.plot(xi,recovered, '-g', label='Recovered', color='green')
    plt.plot(xi,died, color='black', label='Deaths')
    plt.ylabel('Number of Agents (People)')
    plt.xlabel('Days Elapsed')
    plt.legend()

    plt.show()

if __name__ == '__main__':
    main(Disease('MERS', 80, 10, 6, 30), Environment(30, 50))
