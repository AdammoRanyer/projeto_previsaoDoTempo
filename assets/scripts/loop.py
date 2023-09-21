from config import d_config as c
import utils as u
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg
import time
import datetime
import random
from pygame.math import lerp

def load_scene(scene):
    """
    Carrega objetos da cena.
    
    Parâmetros:
        scene (str) - nome da cena
    
    Retorno:
        Objetos da cena criados
    """
    
    if scene == "load_screen":
        c["d_objects"].clear()
        #c["spriteGroup"] = pg.sprite.LayeredUpdates()
        
        c["background_color"] = (237, 186, 118)
        u.SpriteObject("loadingBar[_0", animation="main", position=[32, 460])
        u.SpriteObject("loadingBar=_0", animation="main", position=[42, 460], imageSize=(876, 38))
        u.SpriteObject("loadingBar]_0", animation="main", position=[918, 460])
        u.SpriteObject("loadingBarBar_0", position=[40, 467], zOrder=-1, imageSize=(0, 23))
        u.Text("txtLoading_0", size=48, text="Carregando...", position=[40, 410])
    
    if scene == "scene_0":
        l_cities = [
            "Jaboatão dos Guararapes",
            "Londres",
            "São Paulo",
            "Tokyo",
            "Nova York",
            "Moscou",
        ]
        random.shuffle(l_cities)
        t_tasks = (
            (u.weatherForecast_nowAndTomorrow, ({"city": l_cities[0]})), 
            (u.weatherForecast_nowAndTomorrow, ({"city": l_cities[1]})),
            (u.weatherForecast_nowAndTomorrow, ({"city": l_cities[2]})), 
            (u.weatherForecast_nowAndTomorrow, ({"city": l_cities[3]})),
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
            if u.event_checkInput(event, c["key_r"]) and len(c["d_objects"]["txtLoading_0"].text) > 13:
                load_scene(c["scene"][0])
                c["load_target"] = 0
                c["l_threadsResults"] = []
                c["load_scene"] = False

        c["d_objects"]["loadingBarBar_0"].set_imageFill((239, 239, 239))
        if len(c["l_threadsResults"]) > 0:
            if c["d_objects"]["loadingBarBar_0"].image.get_width() < (len(c["l_threadsResults"]) * (880 / c["load_target"])):
                if c["d_objects"]["loadingBarBar_0"].image.get_width() + ((880 / c["load_target"]) / 10) > 880:
                    x = 880
                else:
                    x = c["d_objects"]["loadingBarBar_0"].image.get_width() + ((880 / c["load_target"]) / 10)
                c["d_objects"]["loadingBarBar_0"].set_imageSize(
                    x,
                    c["d_objects"]["loadingBarBar_0"].image.get_height(),
                )
        else:
            c["d_objects"]["loadingBarBar_0"].set_imageSize(
                c["d_objects"]["loadingBarBar_0"].image.get_width() + 1,
                c["d_objects"]["loadingBarBar_0"].image.get_height(),
            )
        
        u.draw_objects(main_surface)

        if c["load_scene"] == False:
            load_scene(c["scene"][1])
            c["load_scene"] = True
        elif len(c["l_threadsResults"]) == c["load_target"] and c["d_objects"]["loadingBarBar_0"].image.get_width() == 880:
            success = True
            for i in c["l_threadsResults"]:
                if i == "Falha ao executar requisão em Open Weather" \
                or i == "Falha ao executar requisão em Googletrans":
                    success = False
                    c["d_objects"]["txtLoading_0"].set_size(24)
                    c["d_objects"]["txtLoading_0"].text = i + "\nPressione a tecla [R] para tentar novamente"
                    break
            if success == True:
                c["scene"][0] = c["scene"][1]
                c["scene"][1] = ""
                c["load_target"] = 0
                c["l_forecasts"] = []
                c["l_forecasts"] = c["l_threadsResults"]
                #print(c["l_threadsResults"])
                c["l_threadsResults"] = []
                c["load_scene"] = False
                
                #print(c["l_forecasts"])
                c["d_objects"].clear()
                #c["spriteGroup"] = pg.sprite.LayeredUpdates()
                u.SpriteObject("bg_0", animation="bg_0")
                u.SpriteObject("forecastIcon_0", position=[850, 30], animation=c["l_forecasts"][0]["icon"], zOrder=1)
                u.Text("txt_0", size=32, color=(239, 239, 239), text=c["l_forecasts"][0]["temperature_0"][0], position=[894, 32], zOrder=1)
                u.Text("txt_1", size=24, color=(239, 239, 239), text="00:00", position=[843, 66], zOrder=1)
                u.Text("txt_2", size=48, text=c["l_forecasts"][0]["city"], position=[300, 70], zOrder=1)
                u.SpriteObject("liveBox_0", imageSize=(100, 42), color=(145, 114, 103), position=[0, 480], zOrder=5)
                u.SpriteObject("infoBox_0", imageSize=(860, 42), color=(137, 154, 142), position=[100, 480], zOrder=3)
                u.Text("txt_3", size=30, color=(239, 239, 239), text="AO VIVO", position=[7, 493], zOrder=6)
                u.Text("txt_4", size=30, color=(239, 239, 239), text="AGORA A TEMPERATURA MÁXIMA PARA AMANHÃ", position=[0, 489], zOrder=4)
                u.Text("txt_5", size=30, color=(239, 239, 239), text="AGORA A TEMPERATURA MÁXIMA PARA AMANHÃ", position=[600, 489], zOrder=4)
                u.Text("txt_6", size=30, color=(239, 239, 239), text="AGORA A TEMPERATURA MÁXIMA PARA AMANHÃ", position=[1200, 489], zOrder=4)
                u.Text("txt_7", size=48, color=(237, 186, 118), text="°C", position=[275, 110], zOrder=1)
                u.Text("txt_8", size=48, text="", position=[275, 110], zOrder=1)
                u.Text("txt_9", size=26, text="00h     03h     06h     09h     12h     15h     18h     21h     00h", position=[79, 355], zOrder=1)
                spacing, l_graphData = u.load_graphData(0)
                d_control["graph_target"][0] = (max(l_graphData))[0]
                d_control["graph_target"][1].clear()
                for i in range(len(l_graphData)):
                    if max(l_graphData) == l_graphData[i]:
                        d_control["graph_target"][1].append("txt_"+str(i+10))
                #color = (239, 239, 239)
                u.Text("txt_10", size=26, text=str(l_graphData[0][0])+"°", position=[79, 336-(spacing*l_graphData[0][1])], zOrder=2, visible=False)
                u.Text("txt_11", size=26, text=str(l_graphData[1][0])+"°", position=[79+(54*1), 336-(spacing*l_graphData[1][1])], zOrder=2, visible=False)
                u.Text("txt_12", size=26, text=str(l_graphData[2][0])+"°", position=[79+(54*2), 336-(spacing*l_graphData[2][1])], zOrder=2, visible=False)
                u.Text("txt_13", size=26, text=str(l_graphData[3][0])+"°", position=[79+(54*3), 336-(spacing*l_graphData[3][1])], zOrder=2, visible=False)
                u.Text("txt_14", size=26, text=str(l_graphData[4][0])+"°", position=[79+(54*4), 336-(spacing*l_graphData[4][1])], zOrder=2, visible=False)
                u.Text("txt_15", size=26, text=str(l_graphData[5][0])+"°", position=[79+(54*5), 336-(spacing*l_graphData[5][1])], zOrder=2, visible=False)
                u.Text("txt_16", size=26, text=str(l_graphData[6][0])+"°", position=[79+(54*6), 336-(spacing*l_graphData[6][1])], zOrder=2, visible=False)
                u.Text("txt_17", size=26, text=str(l_graphData[7][0])+"°", position=[79+(54*7), 336-(spacing*l_graphData[7][1])], zOrder=2, visible=False)
                u.Text("txt_18", size=26, text=str(l_graphData[8][0])+"°", position=[79+(54*8), 336-(spacing*l_graphData[8][1])], zOrder=2, visible=False)
                u.Text("txt_19", size=26, text="ma", position=[50, 155], zOrder=1)
                u.Text("txt_20", size=26, text="mi", position=[50, 330], zOrder=1)
                u.SpriteObject("pipe_0", imageSize=(2, 30), position=[273, 109], zOrder=2)
                u.Canvas("lineHorizontal_0", width=2, zOrder=1, lineCoordinates=[77, 350, 545, 350])
                u.Canvas("lineVertical_0", width=2, zOrder=1, lineCoordinates=[77, 155, 77, 350])
                u.Canvas("line_0", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_10"].position[0],
                    c["d_objects"]["txt_10"].position[1]+12,
                    c["d_objects"]["txt_10"].position[0],
                    c["d_objects"]["txt_10"].position[1]+12,
                ])
                u.Canvas("line_1", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_11"].position[0],
                    c["d_objects"]["txt_11"].position[1]+12,
                    c["d_objects"]["txt_11"].position[0],
                    c["d_objects"]["txt_11"].position[1]+12,
                ])
                u.Canvas("line_2", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_12"].position[0],
                    c["d_objects"]["txt_12"].position[1]+12,
                    c["d_objects"]["txt_12"].position[0],
                    c["d_objects"]["txt_12"].position[1]+12,
                ])
                u.Canvas("line_3", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_13"].position[0],
                    c["d_objects"]["txt_13"].position[1]+12,
                    c["d_objects"]["txt_13"].position[0],
                    c["d_objects"]["txt_13"].position[1]+12,
                ])
                u.Canvas("line_4", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_14"].position[0],
                    c["d_objects"]["txt_14"].position[1]+12,
                    c["d_objects"]["txt_14"].position[0],
                    c["d_objects"]["txt_14"].position[1]+12,
                ])
                u.Canvas("line_5", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_15"].position[0],
                    c["d_objects"]["txt_15"].position[1]+12,
                    c["d_objects"]["txt_15"].position[0],
                    c["d_objects"]["txt_15"].position[1]+12,
                ])
                u.Canvas("line_6", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_16"].position[0],
                    c["d_objects"]["txt_16"].position[1]+12,
                    c["d_objects"]["txt_16"].position[0],
                    c["d_objects"]["txt_16"].position[1]+12,
                ])
                u.Canvas("line_7", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_17"].position[0],
                    c["d_objects"]["txt_17"].position[1]+12,
                    c["d_objects"]["txt_17"].position[0],
                    c["d_objects"]["txt_17"].position[1]+12,
                ])
                u.Canvas("line_8", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_18"].position[0],
                    c["d_objects"]["txt_18"].position[1]+12,
                    c["d_objects"]["txt_18"].position[0],
                    c["d_objects"]["txt_18"].position[1]+12,
                ])
                d_control["graph_path"] = 0
                d_control["lerp_path"] = 0
                c["scene_state"] = "choose_temperature"
    
    elif scene == "scene_0":
        for event in pg.event.get():
            u.event_exitPygame(event)
            if u.event_checkInput(event, c["key_f"]): 
                if c["window_resolution"] != 1: u.set_resolution(window_surface, 1)
                else: u.set_resolution(window_surface, 0)
            if u.event_checkInput(event, c["key_r"]):
                load_scene("load_screen")
                c["scene"] = ["load_screen", "scene_0"]
                return None
            if c["scene_state"] == "choose_temperature":
                if u.event_checkInput(event, c["key_-"]) and len(c["d_objects"]["txt_8"].text) == 0:
                    c["d_objects"]["txt_8"].text += "-"
                if (u.event_checkInput(event, c["key_0"]) or u.event_checkInput(event, c["key_keypad0"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "0"
                if (u.event_checkInput(event, c["key_1"]) or u.event_checkInput(event, c["key_keypad1"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "1"
                if (u.event_checkInput(event, c["key_2"]) or u.event_checkInput(event, c["key_keypad2"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "2"
                if (u.event_checkInput(event, c["key_3"]) or u.event_checkInput(event, c["key_keypad3"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "3"
                if (u.event_checkInput(event, c["key_4"]) or u.event_checkInput(event, c["key_keypad4"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "4"
                if (u.event_checkInput(event, c["key_5"]) or u.event_checkInput(event, c["key_keypad5"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "5"
                if (u.event_checkInput(event, c["key_6"]) or u.event_checkInput(event, c["key_keypad6"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "6"
                if (u.event_checkInput(event, c["key_7"]) or u.event_checkInput(event, c["key_keypad7"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "7"
                if (u.event_checkInput(event, c["key_8"]) or u.event_checkInput(event, c["key_keypad8"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "8"
                if (u.event_checkInput(event, c["key_9"]) or u.event_checkInput(event, c["key_keypad9"])) and len(c["d_objects"]["txt_8"].text) < 3:
                    c["d_objects"]["txt_8"].text += "9"
                if u.event_checkInput(event, c["key_backspace"]) and len(c["d_objects"]["txt_8"].text) > 0:
                    c["d_objects"]["txt_8"].text = c["d_objects"]["txt_8"].text[:-1]
                if u.event_checkInput(event, c["key_return"]) and len(c["d_objects"]["txt_8"].text) > 0:
                    c["scene_state"] = "draw_graph"
                    c["d_objects"]["pipe_0"].switch_visible(False)
                    c["d_objects"]["txt_10"].visible = True
            elif c["scene_state"] == "result":
                if u.event_checkInput(event, c["key_return"]):
                    d_control["city"] += 1
                    spacing, l_graphData = u.load_graphData(d_control["city"])
                    d_control["graph_target"][0] = (max(l_graphData))[0]
                    d_control["graph_target"][1].clear()
                    for i in range(len(l_graphData)):
                        if max(l_graphData) == l_graphData[i]:
                            d_control["graph_target"][1].append("txt_"+str(i+10))
                    c["d_objects"]["txt_2"].text = c["l_forecasts"][d_control["city"]]["city"]
                    c["d_objects"]["txt_8"].text = ""
                    c["d_objects"]["txt_10"].visible = False
                    c["d_objects"]["txt_11"].visible = False
                    c["d_objects"]["txt_12"].visible = False
                    c["d_objects"]["txt_13"].visible = False
                    c["d_objects"]["txt_14"].visible = False
                    c["d_objects"]["txt_15"].visible = False
                    c["d_objects"]["txt_16"].visible = False
                    c["d_objects"]["txt_17"].visible = False
                    c["d_objects"]["txt_18"].visible = False
                    c["d_objects"]["txt_10"].background = None
                    c["d_objects"]["txt_11"].background = None
                    c["d_objects"]["txt_12"].background = None
                    c["d_objects"]["txt_13"].background = None
                    c["d_objects"]["txt_14"].background = None
                    c["d_objects"]["txt_15"].background = None
                    c["d_objects"]["txt_16"].background = None
                    c["d_objects"]["txt_17"].background = None
                    c["d_objects"]["txt_18"].background = None
                    c["d_objects"]["txt_10"].timer_0 = 0
                    c["d_objects"]["txt_11"].timer_0 = 0
                    c["d_objects"]["txt_12"].timer_0 = 0
                    c["d_objects"]["txt_13"].timer_0 = 0
                    c["d_objects"]["txt_14"].timer_0 = 0
                    c["d_objects"]["txt_15"].timer_0 = 0
                    c["d_objects"]["txt_16"].timer_0 = 0
                    c["d_objects"]["txt_17"].timer_0 = 0
                    c["d_objects"]["txt_18"].timer_0 = 0
                    c["d_objects"]["txt_10"].text = str(l_graphData[0][0])+"°"
                    c["d_objects"]["txt_11"].text = str(l_graphData[1][0])+"°"
                    c["d_objects"]["txt_12"].text = str(l_graphData[2][0])+"°"
                    c["d_objects"]["txt_13"].text = str(l_graphData[3][0])+"°"
                    c["d_objects"]["txt_14"].text = str(l_graphData[4][0])+"°"
                    c["d_objects"]["txt_15"].text = str(l_graphData[5][0])+"°"
                    c["d_objects"]["txt_16"].text = str(l_graphData[6][0])+"°"
                    c["d_objects"]["txt_17"].text = str(l_graphData[7][0])+"°"
                    c["d_objects"]["txt_18"].text = str(l_graphData[8][0])+"°"
                    c["d_objects"]["txt_10"].position = [79, 336-(spacing*l_graphData[0][1])]
                    c["d_objects"]["txt_11"].position = [79+(54*1), 336-(spacing*l_graphData[1][1])]
                    c["d_objects"]["txt_12"].position = [79+(54*2), 336-(spacing*l_graphData[2][1])]
                    c["d_objects"]["txt_13"].position = [79+(54*3), 336-(spacing*l_graphData[3][1])]
                    c["d_objects"]["txt_14"].position = [79+(54*4), 336-(spacing*l_graphData[4][1])]
                    c["d_objects"]["txt_15"].position = [79+(54*5), 336-(spacing*l_graphData[5][1])]
                    c["d_objects"]["txt_16"].position = [79+(54*6), 336-(spacing*l_graphData[6][1])]
                    c["d_objects"]["txt_17"].position = [79+(54*7), 336-(spacing*l_graphData[7][1])]
                    c["d_objects"]["txt_18"].position = [79+(54*8), 336-(spacing*l_graphData[8][1])]
                    u.Canvas("line_0", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_10"].position[0],
                        c["d_objects"]["txt_10"].position[1]+12,
                        c["d_objects"]["txt_10"].position[0],
                        c["d_objects"]["txt_10"].position[1]+12,
                    ])
                    u.Canvas("line_1", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_11"].position[0],
                        c["d_objects"]["txt_11"].position[1]+12,
                        c["d_objects"]["txt_11"].position[0],
                        c["d_objects"]["txt_11"].position[1]+12,
                    ])
                    u.Canvas("line_2", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_12"].position[0],
                        c["d_objects"]["txt_12"].position[1]+12,
                        c["d_objects"]["txt_12"].position[0],
                        c["d_objects"]["txt_12"].position[1]+12,
                    ])
                    u.Canvas("line_3", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_13"].position[0],
                        c["d_objects"]["txt_13"].position[1]+12,
                        c["d_objects"]["txt_13"].position[0],
                        c["d_objects"]["txt_13"].position[1]+12,
                    ])
                    u.Canvas("line_4", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_14"].position[0],
                        c["d_objects"]["txt_14"].position[1]+12,
                        c["d_objects"]["txt_14"].position[0],
                        c["d_objects"]["txt_14"].position[1]+12,
                    ])
                    u.Canvas("line_5", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_15"].position[0],
                        c["d_objects"]["txt_15"].position[1]+12,
                        c["d_objects"]["txt_15"].position[0],
                        c["d_objects"]["txt_15"].position[1]+12,
                    ])
                    u.Canvas("line_6", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_16"].position[0],
                        c["d_objects"]["txt_16"].position[1]+12,
                        c["d_objects"]["txt_16"].position[0],
                        c["d_objects"]["txt_16"].position[1]+12,
                    ])
                    u.Canvas("line_7", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_17"].position[0],
                        c["d_objects"]["txt_17"].position[1]+12,
                        c["d_objects"]["txt_17"].position[0],
                        c["d_objects"]["txt_17"].position[1]+12,
                    ])
                    u.Canvas("line_8", color=(213, 90, 50), width=0, zOrder=1, lineCoordinates=[
                        c["d_objects"]["txt_18"].position[0],
                        c["d_objects"]["txt_18"].position[1]+12,
                        c["d_objects"]["txt_18"].position[0],
                        c["d_objects"]["txt_18"].position[1]+12,
                    ])
                    d_control["graph_path"] = 0
                    d_control["lerp_path"] = 0
                    c["scene_state"] = "choose_temperature"
        
        c["d_objects"]["txt_1"].text = "  "+str(datetime.date.today())[8:]+"/"+str(datetime.date.today())[5:7]+"    "+str(datetime.datetime.now())[11:16]
        amount_char = len(c["d_objects"]["txt_2"].text)
        c["d_objects"]["txt_2"].set_position(300 - (amount_char * 9), 70)
        c["d_objects"]["txt_4"].set_position(c["d_objects"]["txt_4"].position[0] - 1, 489)
        c["d_objects"]["txt_5"].set_position(c["d_objects"]["txt_5"].position[0] - 1, 489)
        c["d_objects"]["txt_6"].set_position(c["d_objects"]["txt_6"].position[0] - 1, 489)
        if c["d_objects"]["txt_4"].position[0] <= -600: c["d_objects"]["txt_4"].set_position(1200, 489)
        if c["d_objects"]["txt_5"].position[0] <= -600: c["d_objects"]["txt_5"].set_position(1200, 489)
        if c["d_objects"]["txt_6"].position[0] <= -600: c["d_objects"]["txt_6"].set_position(1200, 489)
        if c["scene_state"] == "choose_temperature":
            c["d_objects"]["pipe_0"].flickering(36)
            c["d_objects"]["pipe_0"].rect.x = 273 + (len(c["d_objects"]["txt_8"].text) * 19)
        c["d_objects"]["txt_7"].position[0] = 275 + (len(c["d_objects"]["txt_8"].text) * 19)
        
        if c["scene_state"] == "draw_graph":
            if d_control["lerp_path"] < 1: 
                d_control["lerp_path"] += 0.05
            if d_control["lerp_path"] > 1:
                d_control["lerp_path"] = 1
            
            if d_control["graph_path"] == 0:
                u.Canvas("line_0", color=(213, 90, 50), width=4, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_10"].position[0],
                    c["d_objects"]["txt_10"].position[1]+12,
                    lerp(c["d_objects"]["txt_10"].position[0], c["d_objects"]["txt_11"].position[0], d_control["lerp_path"]),
                    lerp(c["d_objects"]["txt_10"].position[1]+12, c["d_objects"]["txt_11"].position[1]+12, d_control["lerp_path"]),
                ]) 
                if d_control["lerp_path"] == 1: 
                    d_control["graph_path"] += 1
                    d_control["lerp_path"] = 0
                    c["d_objects"]["txt_11"].visible = True
            if d_control["graph_path"] == 1:
                u.Canvas("line_1", color=(213, 90, 50), width=4, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_11"].position[0],
                    c["d_objects"]["txt_11"].position[1]+12,
                    lerp(c["d_objects"]["txt_11"].position[0], c["d_objects"]["txt_12"].position[0], d_control["lerp_path"]),
                    lerp(c["d_objects"]["txt_11"].position[1]+12, c["d_objects"]["txt_12"].position[1]+12, d_control["lerp_path"]),
                ]) 
                if d_control["lerp_path"] == 1: 
                    d_control["graph_path"] += 1
                    d_control["lerp_path"] = 0
                    c["d_objects"]["txt_12"].visible = True
            if d_control["graph_path"] == 2:
                u.Canvas("line_2", color=(213, 90, 50), width=4, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_12"].position[0],
                    c["d_objects"]["txt_12"].position[1]+12,
                    lerp(c["d_objects"]["txt_12"].position[0], c["d_objects"]["txt_13"].position[0], d_control["lerp_path"]),
                    lerp(c["d_objects"]["txt_12"].position[1]+12, c["d_objects"]["txt_13"].position[1]+12, d_control["lerp_path"]),
                ]) 
                if d_control["lerp_path"] == 1: 
                    d_control["graph_path"] += 1
                    d_control["lerp_path"] = 0
                    c["d_objects"]["txt_13"].visible = True
            if d_control["graph_path"] == 3:
                u.Canvas("line_3", color=(213, 90, 50), width=4, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_13"].position[0],
                    c["d_objects"]["txt_13"].position[1]+12,
                    lerp(c["d_objects"]["txt_13"].position[0], c["d_objects"]["txt_14"].position[0], d_control["lerp_path"]),
                    lerp(c["d_objects"]["txt_13"].position[1]+12, c["d_objects"]["txt_14"].position[1]+12, d_control["lerp_path"]),
                ]) 
                if d_control["lerp_path"] == 1: 
                    d_control["graph_path"] += 1
                    d_control["lerp_path"] = 0
                    c["d_objects"]["txt_14"].visible = True
            if d_control["graph_path"] == 4:
                u.Canvas("line_4", color=(213, 90, 50), width=4, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_14"].position[0],
                    c["d_objects"]["txt_14"].position[1]+12,
                    lerp(c["d_objects"]["txt_14"].position[0], c["d_objects"]["txt_15"].position[0], d_control["lerp_path"]),
                    lerp(c["d_objects"]["txt_14"].position[1]+12, c["d_objects"]["txt_15"].position[1]+12, d_control["lerp_path"]),
                ]) 
                if d_control["lerp_path"] == 1: 
                    d_control["graph_path"] += 1
                    d_control["lerp_path"] = 0
                    c["d_objects"]["txt_15"].visible = True
            if d_control["graph_path"] == 5:
                u.Canvas("line_5", color=(213, 90, 50), width=4, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_15"].position[0],
                    c["d_objects"]["txt_15"].position[1]+12,
                    lerp(c["d_objects"]["txt_15"].position[0], c["d_objects"]["txt_16"].position[0], d_control["lerp_path"]),
                    lerp(c["d_objects"]["txt_15"].position[1]+12, c["d_objects"]["txt_16"].position[1]+12, d_control["lerp_path"]),
                ]) 
                if d_control["lerp_path"] == 1: 
                    d_control["graph_path"] += 1
                    d_control["lerp_path"] = 0
                    c["d_objects"]["txt_16"].visible = True
            if d_control["graph_path"] == 6:
                u.Canvas("line_6", color=(213, 90, 50), width=4, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_16"].position[0],
                    c["d_objects"]["txt_16"].position[1]+12,
                    lerp(c["d_objects"]["txt_16"].position[0], c["d_objects"]["txt_17"].position[0], d_control["lerp_path"]),
                    lerp(c["d_objects"]["txt_16"].position[1]+12, c["d_objects"]["txt_17"].position[1]+12, d_control["lerp_path"]),
                ]) 
                if d_control["lerp_path"] == 1: 
                    d_control["graph_path"] += 1
                    d_control["lerp_path"] = 0
                    c["d_objects"]["txt_17"].visible = True
            if d_control["graph_path"] == 7:
                u.Canvas("line_7", color=(213, 90, 50), width=4, zOrder=1, lineCoordinates=[
                    c["d_objects"]["txt_17"].position[0],
                    c["d_objects"]["txt_17"].position[1]+12,
                    lerp(c["d_objects"]["txt_17"].position[0], c["d_objects"]["txt_18"].position[0], d_control["lerp_path"]),
                    lerp(c["d_objects"]["txt_17"].position[1]+12, c["d_objects"]["txt_18"].position[1]+12, d_control["lerp_path"]),
                ]) 
                if d_control["lerp_path"] == 1: 
                    d_control["graph_path"] += 1
                    #d_control["lerp_path"] = 0
                    c["d_objects"]["txt_18"].visible = True
        if d_control["graph_path"] == 8:
            #c["d_objects"]["txt_18"].background = (57, 213, 216)
            for i in d_control["graph_target"][1]:
                c["d_objects"][i].flickering_background(18, (57, 213, 216), None)
            c["scene_state"] = "result"
        
        u.draw_objects(main_surface)

window_surface, main_surface = u.start_pygame()
#clock = pg.time.Clock()
frame = 1 / c["FPS"]
ticks = 0
lastTime = time.perf_counter()
load_scene(c["scene"][0])

d_control={
    "lerp_path": 0,
    "graph_path": 0,
    "graph_target": [0, []],
    "city": 0,
}

while 1:
    #clock.tick(c["FPS"])
    ticks += time.perf_counter() - lastTime
    lastTime = time.perf_counter()
    
    if ticks >= frame:
        main_surface.fill(c["background_color"])
        play_scene(c["scene"][0])
        u.adjust_resolution(window_surface, main_surface)
        ticks = 0
    
    pg.display.update((c["window_position"][0], 0, c["window_originalSize"][0] * c["window_resolution"], c["window_originalSize"][1] * c["window_resolution"]))

exit(0)