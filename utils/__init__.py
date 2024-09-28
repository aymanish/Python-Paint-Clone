#naming .py folder with __init__ treats the folder as a python package that can be imported
#import constants and functions from settings.py
#.settings: the . allows relative import to allow import a module within same package as init
from .settings import*
from .button import*
import pygame
pygame.init
pygame.font.init()