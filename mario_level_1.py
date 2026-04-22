#!/usr/bin/env python
__author__ = 'justinarmstrong'

"""
This is an attempt to recreate the first level of
Super Mario Bros for the NES.
"""

import sys
import pygame as pg
from data.marioMain import mainMario
import cProfile


if __name__=='__main__':
    # Chromosome vazio para jogo manual (controle do jogador)
    chromosome = []
    distance, time = mainMario(chromosome, redraw=True)
    pg.quit()
    sys.exit()
























