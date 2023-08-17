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
    
    print("carregando cena...")
    
    c["d_objects"].clear()
    c["spriteGroup"] = pg.sprite.LayeredUpdates()
    def load_sprites(spriteSheet, order):
        d_sprites = {}
        #if order == x:
        
        return d_sprites
    
    if scene == "main":
        c["l_threadsResults"] = []
        t_tasks = (
            (u.weatherForecast, ({"city": "Jaboatão dos Guararapes"})), 
            (u.weatherForecast, ({"city": "Londres"})), 
            (u.weatherForecast, ({"city": "São Paulo"})), 
            (u.weatherForecast, ({"city": "Tokyo"})),
            (u.SpriteObject, ({"name": "p1"})),
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
    
    if scene == "load screen":
        for event in pg.event.get():
            u.event_exitPygame(event)
            if u.event_checkInput(event, c["key_f"]): 
                if c["window_resolution"] != 1: u.set_resolution(window_surface, 1)
                else: u.set_resolution(window_surface, 0)

        if c["load_scene"] == False:
            load_scene(c["scene"][1])
            c["load_scene"] = True
        
        elif len(c["l_threadsResults"]) == c["load_target"]:
            for i in c["l_threadsResults"]:
                if i == "Falha ao executar requisão em Open Weather" \
                or i == "Falha ao executar requisão em Googletrans":
                    print(i)
                    exit(1)
            c["scene"][0] = c["scene"][1]
            c["load_scene"] = False            
            print("cena carregada")
    
    elif scene == "main":
        for event in pg.event.get():
            u.event_exitPygame(event)
            if u.event_checkInput(event, c["key_f"]): 
                if c["window_resolution"] != 1: u.set_resolution(window_surface, 1)
                else: u.set_resolution(window_surface, 0)
            if u.event_checkInput(event, c["key_r"]):
                c["scene"] = ["load screen", "main"]
                
        c["d_objects"]["p1"].rect.x += 1
        
        u.draw_spriteGroup(window_surface)

window_surface = u.start_pygame()

#clock = pg.time.Clock()
frame = 1 / c["FPS"]
ticks = 0
lastTime = time.perf_counter()

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