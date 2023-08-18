from config import d_config as c
import utils as u
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg
import time

def load_scene(scene):
    """
    Carrega objetos da cena.
    
    Parâmetros:
        scene (str) - nome da cena
    
    Retorno:
        Objetos da cena criados
    """
    
    if scene == "scene_0":    
        c["l_threadsResults"] = []
        t_tasks = (
            (u.weatherForecast, ({"city": "Jaboatão dos Guararapes"})), 
            (u.weatherForecast, ({"city": "Londres"})), 
            (u.weatherForecast, ({"city": "São Paulo"})), 
            (u.weatherForecast, ({"city": "Tokyo"})),
        )
        c["load_target"] = len(t_tasks)
        u.threads(t_tasks, c["l_threadsResults"])

def play_scene(scene):
    """
    Toca a cena.
    
    Parâmetros:
        scene (str) - nome da cena
    
    Retorno:
        Retorna o desfecho da cena
    """
    
    if scene == "load_screen":
        for event in pg.event.get():
            u.event_exitPygame(event)
            if u.event_checkInput(event, c["key_f"]): 
                if c["window_resolution"] != 1: u.set_resolution(window_surface, 1)
                else: u.set_resolution(window_surface, 0)

        u.draw_spriteGroup(window_surface)

        if c["load_scene"] == False:
            load_scene(c["scene"][1])
            c["load_scene"] = True
        """
        elif len(c["l_threadsResults"]) == c["load_target"]:
            for i in c["l_threadsResults"]:
                if i == "Falha ao executar requisão em Open Weather" \
                or i == "Falha ao executar requisão em Googletrans":
                    print(i)
                    exit(1)
            c["scene"][0] = c["scene"][1]
            c["scene"][1] = ""
            c["load_scene"] = False
            
            c["background_color"] = (128, 128, 128)
            c["d_objects"].clear()
            c["spriteGroup"] = pg.sprite.LayeredUpdates()
            u.SpriteObject("p1")
        """
    
    elif scene == "scene_0":
        for event in pg.event.get():
            u.event_exitPygame(event)
            if u.event_checkInput(event, c["key_f"]): 
                if c["window_resolution"] != 1: u.set_resolution(window_surface, 1)
                else: u.set_resolution(window_surface, 0)
            if u.event_checkInput(event, c["key_r"]):
                c["scene"] = ["load_screen", "scene_0"]
                
        c["d_objects"]["p1"].rect.x += 1
        
        u.draw_spriteGroup(window_surface)

window_surface = u.start_pygame()

#clock = pg.time.Clock()
frame = 1 / c["FPS"]
ticks = 0
lastTime = time.perf_counter()

c["background_color"] = (237, 186, 118)
u.SpriteObject("loadingBar_[", d_sprites=True, position=[32, 460])
c["d_objects"]["loadingBar_["].image = c["d_objects"]["loadingBar_["].d_sprites["main"][0]
u.SpriteObject("loadingBar_=", d_sprites=True, position=[42, 460])
c["d_objects"]["loadingBar_="].image = c["d_objects"]["loadingBar_="].d_sprites["main"][0]
c["d_objects"]["loadingBar_="].set_imageSize(876, 38)
u.SpriteObject("loadingBar_]", d_sprites=True, position=[918, 460])
c["d_objects"]["loadingBar_]"].image = c["d_objects"]["loadingBar_]"].d_sprites["main"][0]
u.SpriteObject("loadingBar_bar", position=[40, 467], zOrder=-1)
c["d_objects"]["loadingBar_bar"].set_imageFill((239, 239, 239))
c["d_objects"]["loadingBar_bar"].set_imageSize(0, 23)

while 1:
    #clock.tick(c["FPS"])
    ticks += time.perf_counter() - lastTime
    lastTime = time.perf_counter()
    
    if ticks >= frame:
        window_surface.fill(c["background_color"])
        play_scene(c["scene"][0])
        ticks = 0
    
    pg.display.update((c["window_position"][0], 0, c["window_originalSize"][0] * c["window_resolution"], c["window_originalSize"][1] * c["window_resolution"]))

exit(0)