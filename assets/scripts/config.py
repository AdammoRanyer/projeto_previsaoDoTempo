import screeninfo
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg

d_config = {
	"OpenWeather_key": "1fae0386a4d15ee5dd547562f9d0dd5c",
    "l_threadsResults": [],
    "label_name": "O Cara do Tempo",
    "window_originalSize": (960, 540),
    "window_resolution": 1,
    "monitor_size": (screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height),
    "window_position": (0, 0),
    "FPS": 60,
    "background_color": (128, 128, 128),
    "scene": ["load_screen", "scene_0"],
    "load_scene": False,
    "load_target": 0,
    "d_objects": {},
    "spriteGroup": pg.sprite.LayeredUpdates(),
    "sprites_colorKey": ((253, 77, 211)),
    "dir_root": os.getcwd()[:-8],
    "spriteSheet_0": None,
    "key_f": pg.K_f,
    "key_r": pg.K_r,
}