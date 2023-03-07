import pygame, sys, random, time

from scripts.entity.entity import Entity
from scripts.entity.player import Player

player = Player((0, 0), (16, 32))
player.initialize()
print(player.images)