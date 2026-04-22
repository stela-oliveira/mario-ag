__author__ = 'justinarmstrong'

"""
Inicializa o display do pygame e carrega recursos.
MODIFICADO: SDL_VIDEODRIVER padrão = 'dummy' para rodar sem janela
            (necessário para Docker sem servidor X11).
            Quando DRAW_FRAMES=True, use SDL_VIDEODRIVER=x11 manualmente.
"""

import os
import pygame as pg

# ── Configurar drivers SDL ANTES de inicializar pygame ─────────────
# Audio: sempre dummy dentro do container
if 'SDL_AUDIODRIVER' not in os.environ:
    os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Para assistir o Mario jogar: defina SDL_VIDEODRIVER=x11 no ambiente
if 'SDL_VIDEODRIVER' not in os.environ:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'

# Renderização por software (sem GPU)
if 'SDL_RENDER_DRIVER' not in os.environ:
    os.environ['SDL_RENDER_DRIVER'] = 'software'

from . import tools
from . import constants as c

ORIGINAL_CAPTION = c.ORIGINAL_CAPTION

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(c.ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(c.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
