from config import d_config as c
import requests
from googletrans import Translator
from threading import Thread
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg

def translate(text, languages=("en", "pt")):
    """
    Traduz palavras, frases.
    
    Parâmetros:
        languages (tuple) - idioma de origem e destino
    
    Retorno:
        text traduzido
    """
    
    try:
        translator = Translator()
        x = translator.translate(text, src=languages[0], dest=languages[1])
        
        return x.text
    except:
        return "Falha ao executar requisão em Googletrans"

def kelvin_to_celsius(kelvin):
    """
    Converte temperatura de kelvin para celsius.
    
    Parâmetros:
        kelvin (float) - temperatura
    
    Retorno:
        Temperatura convertida
    """
    
    celsius = f"{(kelvin - 273.15):.0f}°C"
    
    return celsius

def weatherForecast(city):
    """
    Previsão do tempo.
    
    Parâmetros:
        city (str) - cidade
    
    Retorno:
        Texto com a previsão do tempo atual
    """
    
    try:
        link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={c['OpenWeather_key']}"
        request = requests.get(link)
        d_request = request.json()
        temperature = kelvin_to_celsius(d_request["main"]["temp"])
        description = translate(d_request["weather"][0]["description"])
        forecast = f"{city}: {temperature}, {description}"
        
        return forecast
    except:
        return "Falha ao executar requisão em Open Weather"
    
def threads(t_tasks, l_results):
    """
    Realiza execução de funções em paralelo.
    
    Parâmetros:
        t_tasks (tuple) - tupla com funções e parâmetros
        l_results (list) - lista com o resultado das threads
    
    Retorno:
        l_results preenchido com resultado das threads
    """
    
    def save_thredResult(function, kwargs):
        l_results.append(function(**kwargs))
    
    l_threads = []
    for i in range(len(t_tasks)):
        l_threads.append(Thread(target=save_thredResult, args=[t_tasks[i][0], t_tasks[i][1]]))
    
    for thread in l_threads:
        thread.start()

def start_pygame():
    """
    Inicia pygame e suas configurações.
    
    Parâmetros:
        Nenhum
    
    Retorno:
        window_surface
    """
    
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pg.init()
    pg.display.set_caption(c["label_name"])
    window_surface = pg.display.set_mode((c["window_originalSize"][0] * c["window_resolution"], c["window_originalSize"][1] * c["window_resolution"]))
    icon = pg.image.load(c["dir_root"] + r"\sprites\icon_0.png").convert()
    pg.display.set_icon(icon)
    set_resolution(window_surface, c["window_resolution"])
    
    return window_surface
    
def event_exitPygame(event):
    """
    Encerra o programa.
    
    Parâmetros:
        event (pygame.event.Event) - evento do pygame
    
    Retorno:
        exit(0)
    """

    if event.type == pg.QUIT:
        exit(0)

def event_checkInput(event, key, type=True):
    """
    Checa se um input do tipo pygame event é verdadeiro.
    
    Parâmetros:
        event (pygame.event.Event) - evento do pygame
        key (int) - número da tecla (formato ASCII)
        type (bool) - True = tecla foi precissonada, False = tecla foi despressionada
    
    Retorno:
        bool
    """
    
    input = False  
    if type == True and event.type == pg.KEYDOWN:
        if event.key == key:
            input = True
    elif type == False and event.type == pg.KEYUP:
        if event.key == key:
            input = True
       
    return input

def checkInput(key, type=True):
    """
    Checa se um input é verdadeiro.
    
    Parâmetros:
        key (int) - número da tecla (formato ASCII)
        type (bool) - True = tecla está precissonada, False = tecla não está pressionada
    
    Retorno:
        bool
    """
    
    input = False
    k = pg.key.get_pressed()
    if type == True and k[key]:
        input = True
    elif type == False and k[key] == False:
        input = True
        
    return input

def set_resolution(window_surface, resolution):
    """
    Atualiza resolução da tela.
    
    Parâmetros:
        window_surface (pygame.surface.Surface) - tela do pygame
        resolution (int) - escala da resolução
    
    Retorno:
        Resolução da tela atualizada
    """
    
    c["window_resolution"] = resolution
    if c["window_resolution"] == 0:
        c["window_resolution"] = float(c["monitor_size"][1] / c["window_originalSize"][1])
        x = (c["window_originalSize"][0] * c["window_resolution"], c["window_originalSize"][1] * c["window_resolution"])
        c["window_position"] = ((c["monitor_size"][0] - (c["window_originalSize"][0] * c["window_resolution"])) / 2, 0)
        
        window_surface = pg.display.set_mode(x, pg.FULLSCREEN)
    else:
        x = (c["window_originalSize"][0] * c["window_resolution"], c["window_originalSize"][1] * c["window_resolution"])
        c["window_position"] = (0, 0)
        
        window_surface = pg.display.set_mode(x)

def draw_spriteGroup(window_surface):
    """
    Desenha spriteGroup na tela.
    
    Parâmetros:
        window_surface (pygame.surface.Surface) - tela do pygame
    
    Return:
        Objetos renderizados na tela
    """
    
    surface=pg.Surface(c["window_originalSize"])
    surface.fill(c["background_color"])
    c["spriteGroup"].draw(surface)
    window_surface.blit(pg.transform.scale(surface, (c["window_originalSize"][0] * c["window_resolution"], c["window_originalSize"][1] * c["window_resolution"])), c["window_position"])

class SpriteObject(pg.sprite.Sprite):
    """
    Classe para criação de objetos do tipo SpriteObject.
    """
    def __init__(self, name, save=True, position=[0, 0], image=pg.Surface((16, 16)), d_sprites={}, visible=True, zOrder=0):
        """
        Constrói objeto SpriteObject.
        
        Parâmetros:
            self (utils.SpriteObject) - objeto da classe SpriteObject
            name (str) - nome do objeto
            save (bool) - adiciona objeto em d_objects
            rect (pygame.rect.Rect) - objeto pygame para armazenar coordenadas retangulares
            image (pygame.surface.Surface) - objeto pygame para representar imagens
            d_sprites (dict) - dicionário com todas as sprites/animações
            visible (bool) - visibilidade do objeto
            zOrder (int) - ordenação na janela
        
        Retorno:
            SpriteObject     
        """    

        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.rect = pg.Rect((position[0], position[1], 16, 16))
        self.image = image
        self.image.set_colorkey(c["sprites_colorKey"])
        self.d_sprites = d_sprites
        self.visible = visible
        self.zOrder = zOrder
        
        if save:
            c["d_objects"][self.name] = self
            c["spriteGroup"].add(self, layer=self.zOrder)