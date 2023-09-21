from config import d_config as c
import requests
from googletrans import Translator
from threading import Thread
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg
import datetime

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

def translate_main(text):
    """
    Traduz texto exclusivo.
    
    Parâmetros:
        text (str) - texto
    
    Retorno:
        Texto traduzido
    """
    
    if text == "Thunderstorm": return "Tempestade"
    if text == "Drizzle": return "Garoa"
    if text == "Rain": return "Chuva"
    if text == "Snow": return "Neve"
    if text == "Atmosphere": return "Atmosfera"
    if text == "Clear": return "Limpo"
    if text == "Clouds": return "Nuvens"

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

def weatherForecast_now(city):
    """
    Previsão do tempo atual.
    
    Parâmetros:
        city (str) - cidade
    
    Retorno:
        Dicionário com informações da previsão do tempo atual
    """

    try:
        link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=pt_br&appid={c['OpenWeather_key']}"
        request = requests.get(link, verify=False)
        d_request = request.json()
        temperature = kelvin_to_celsius(d_request["main"]["temp"])
        main = translate_main(d_request["weather"][0]["main"])
        description = d_request["weather"][0]["description"]
        dateTime = str(datetime.datetime.now())[:19]
        icon = d_request["weather"][0]["icon"]

        d_forecast = {
            "type": "now",
            "city": city,
            "temperature": [temperature, main, description, dateTime],
            "icon": icon,
        }
        
        return d_forecast
    except:
        return "Falha ao executar requisão em Open Weather"

def weatherForecast_5days3hours(city):
    """
    Previsão do tempo para amanhã.
    
    Parâmetros:
        city (str) - cidade
    
    Retorno:
        Dicionário com informações da previsão do tempo do próximo dia
    """

    try:
        link = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&lang=pt_br&appid={c['OpenWeather_key']}"
        request = requests.get(link, verify=False)
        d_request = request.json()
        tomorrow = (datetime.datetime.now() + datetime.timedelta(1)).strftime('%Y-%m-%d')
        index = 0
        
        d_forecasts = {
            "type": "5days3hours",
            "city": city,
        }
        for _ in range(9):
            if d_request["list"][index]["dt_txt"][:10] == tomorrow:
                break
            index += 1
        for i in range(9):
            d_forecasts["temperature_"+str(i)] = [
                kelvin_to_celsius(d_request["list"][index]["main"]["temp"]), 
                translate_main(d_request["list"][index]["weather"][0]["main"]),
                d_request["list"][index]["weather"][0]["description"],
                d_request["list"][index]["dt_txt"],
            ]
            index += 1
        
        return d_forecasts
    except:
        return "Falha ao executar requisão em Open Weather"

def weatherForecast_nowAndTomorrow(city):
    """
    Previsão do tempo para hoje e amanhã.
    
    Parâmetros:
        city (str) - cidade
    
    Retorno:
        Dicionário com informações da previsão do tempo de hoje e amanhã
    """
    
    d_now = weatherForecast_now(city)
    d_tomorrow = weatherForecast_5days3hours(city)
    if str(type(d_now)) and str(type(d_tomorrow)) != "<class 'dict'>":
        return "Falha ao executar requisão em Open Weather"
    d_nowAndTomorrow = {
        "type": "nowAndTomorrow",
        "city": city,
        "icon": d_now["icon"],
        "temperature_0": [
            d_now["temperature"][0],
            d_now["temperature"][1],
            d_now["temperature"][2],
            d_now["temperature"][3],
        ],
        "temperature_1": [
            d_tomorrow["temperature_0"][0],
            d_tomorrow["temperature_0"][1],
            d_tomorrow["temperature_0"][2],
            d_tomorrow["temperature_0"][3],
        ],
        "temperature_2": [
            d_tomorrow["temperature_1"][0],
            d_tomorrow["temperature_1"][1],
            d_tomorrow["temperature_1"][2],
            d_tomorrow["temperature_1"][3],
        ],
        "temperature_3": [
            d_tomorrow["temperature_2"][0],
            d_tomorrow["temperature_2"][1],
            d_tomorrow["temperature_2"][2],
            d_tomorrow["temperature_2"][3],
        ],
        "temperature_4": [
            d_tomorrow["temperature_3"][0],
            d_tomorrow["temperature_3"][1],
            d_tomorrow["temperature_3"][2],
            d_tomorrow["temperature_3"][3],
        ],
        "temperature_5": [
            d_tomorrow["temperature_4"][0],
            d_tomorrow["temperature_4"][1],
            d_tomorrow["temperature_4"][2],
            d_tomorrow["temperature_4"][3],
        ],
        "temperature_6": [
            d_tomorrow["temperature_5"][0],
            d_tomorrow["temperature_5"][1],
            d_tomorrow["temperature_5"][2],
            d_tomorrow["temperature_5"][3],
        ],
        "temperature_7": [
            d_tomorrow["temperature_6"][0],
            d_tomorrow["temperature_6"][1],
            d_tomorrow["temperature_6"][2],
            d_tomorrow["temperature_6"][3],
        ],
        "temperature_8": [
            d_tomorrow["temperature_7"][0],
            d_tomorrow["temperature_7"][1],
            d_tomorrow["temperature_7"][2],
            d_tomorrow["temperature_7"][3],
        ],
        "temperature_9": [
            d_tomorrow["temperature_8"][0],
            d_tomorrow["temperature_8"][1],
            d_tomorrow["temperature_8"][2],
            d_tomorrow["temperature_8"][3],
        ],
    }
    
    return d_nowAndTomorrow

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
    
    c["window_icon"] = pg.image.load(c["dir_root"] + r"\sprites\icon_0.png").convert()
    c["spriteSheet_0"] = pg.image.load(c["dir_root"] + r"\sprites\spriteSheet_0.png").convert()
    c["spriteSheet_0"].set_colorkey(c["sprites_colorKey"])
    
    set_resolution(window_surface, c["window_resolution"])
    main_surface = pg.Surface(c["window_originalSize"])    
    
    return window_surface, main_surface
    
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
    Defini resolução da tela.
    
    Parâmetros:
        window_surface (pygame.surface.Surface) - tela do pygame
        resolution (int) - escala da resolução
    
    Retorno:
        Modo de resolução da tela atualizado
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
        
        pg.display.set_icon(c["window_icon"])
        window_surface = pg.display.set_mode(x)

def adjust_resolution(window_surface, main_surface):
    """
    Atualiza tamanho de superfície para tamanho de resolução da tela.
    
    Parâmetros:
        window_surface (pygame.surface.Surface) - tela do pygame de exibição
        main_surface (pygame.surface.Surface) - tela do pygame para renderização de objetos
    
    Retorno:
        Tamanho da tela atualizado
    """
    
    window_surface.blit(
        pg.transform.scale(main_surface, (c["window_originalSize"][0] * c["window_resolution"], c["window_originalSize"][1] * c["window_resolution"])), 
        c["window_position"]
    )

def draw_spriteGroup(surface):
    """
    Desenha spriteGroup na tela.
    
    Parâmetros:
        surface (pygame.surface.Surface) - tela do pygame
    
    Return:
        Objetos renderizados na tela
    """
    
    c["spriteGroup"].draw(surface)

def draw_objects(surface):
    """
    Desenha objetos na tela na ordem definida.
    
    Parâmetros:
        surface (pygame.surface.Surface) - tela do pygame
    
    Return:
        Objetos renderizados na tela
    """
    
    for objectName in sorted(c["d_objects"], key=lambda x: c["d_objects"][x].zOrder):
        c["d_objects"][objectName].draw_object(surface)

def load_sprites(objectName):
    """
    Carrega sprites de um SpriteObject.
    
    Parâmetros:
        objectName (str) - nome do objeto
    
    Retorno:
        Dicionário com todas as sprites/animações
    """
    
    if objectName[:12] == "loadingBar[_":
        d_sprites = {
            "main": [c["spriteSheet_0"].subsurface(0, 0, 10, 38)],
        }
        return d_sprites
        
    if objectName[:12] == "loadingBar=_":
        d_sprites = {
            "main": [c["spriteSheet_0"].subsurface(10, 0, 1, 38)],
        }
        return d_sprites
        
    if objectName[:12] == "loadingBar]_":
        d_sprites = {
            "main": [c["spriteSheet_0"].subsurface(11, 0, 10, 38)],
        }
        return d_sprites
    
    if objectName[:3] == "bg_":
        d_sprites = {
            "bg_0": [c["spriteSheet_0"].subsurface(0, 38, 960, 540)],
        }
        return d_sprites
        
    if objectName[:13] == "forecastIcon_":
        d_sprites = {
            "01d": [c["spriteSheet_0"].subsurface(36, 0, 36, 27)],
            "01n": [c["spriteSheet_0"].subsurface(36*2, 0, 36, 27)],
            "02d": [c["spriteSheet_0"].subsurface(36*3, 0, 36, 27)],
            "02n": [c["spriteSheet_0"].subsurface(36*4, 0, 36, 27)],
            "03d": [c["spriteSheet_0"].subsurface(36*5, 0, 36, 27)],
            "03n": [c["spriteSheet_0"].subsurface(36*5, 0, 36, 27)],
            "04d": [c["spriteSheet_0"].subsurface(36*6, 0, 36, 27)],
            "04n": [c["spriteSheet_0"].subsurface(36*6, 0, 36, 27)],
            "09d": [c["spriteSheet_0"].subsurface(36*7, 0, 36, 27)],
            "09n": [c["spriteSheet_0"].subsurface(36*7, 0, 36, 27)],
            "10d": [c["spriteSheet_0"].subsurface(36*8, 0, 36, 27)],
            "10n": [c["spriteSheet_0"].subsurface(36*9, 0, 36, 27)],
            "11d": [c["spriteSheet_0"].subsurface(36*10, 0, 36, 27)],
            "11n": [c["spriteSheet_0"].subsurface(36*10, 0, 36, 27)],
            "13d": [c["spriteSheet_0"].subsurface(36*11, 0, 36, 27)],
            "13n": [c["spriteSheet_0"].subsurface(36*11, 0, 36, 27)],
            "50d": [c["spriteSheet_0"].subsurface(36*12, 0, 36, 27)],
            "50n": [c["spriteSheet_0"].subsurface(36*12, 0, 36, 27)],
        }
        return d_sprites
        
    if objectName[:] == "":
        d_sprites = {
            
        }
        return d_sprites
    
    return None

def load_graphData(order):
    """
    """
    
    l_temperatures = []
    for i in range(1, 10):
        temperature = c["l_forecasts"][order]["temperature_"+str(i)][0]
        treatment = int(temperature.replace("°C", ""))
        l_temperatures.append(treatment)
    
    smaller = min(l_temperatures)
    bigger = max(l_temperatures)
    scale = bigger - smaller
    spacing = round(190 / scale)
    
    l_temperatureScale = [None, None, None, None, None, None, None, None, None]
    scaleIndex = smaller
    for s in range(scale + 1):
        for i in range(9):
            if l_temperatures[i] == scaleIndex:
                l_temperatureScale[i] = s
        scaleIndex += 1

    l_graphData = list(zip(l_temperatures, l_temperatureScale))
    
    return spacing, l_graphData

class Canvas():
    """
    Classe para criação de objetos do tipo Canvas destinada para desenho de figuras geométricas/gráficos e etc.
    """
    
    def __init__(self, name, save=True, width=2, color=(0, 0, 0), form="line", lineCoordinates=[0, 0, 16, 0], visible=True, zOrder=0):
        """
        Constrói objeto Canvas.
        
        Parâmetros:
            self (game_utils.Text) - objeto da classe Canvas
            name (str) - nome do objeto
            save (bool) - adiciona objeto em d_objects
            width (int) - largura da linha
            color (list) - cor da linha de desenho
            form (str) - forma geométrica
            lineCoordinates (list) - coordenadas de linha
            visible (bool) - visibilidade do objeto
            zOrder (int) - ordenação na janela
        
        Return:
            Objeto     
        """
        
        self.name = name
        self.width = width
        self.color = color
        self.form = form
        self.lineCoordinates = lineCoordinates
        self.visible = visible
        self.zOrder = zOrder
        
        if save:
            c["d_objects"][self.name] = self
        
    def draw_object(self, surface):
        """
        Desenha Text na tela.
        
        Parâmetros:
            self (game_utils.Text) - objeto da classe Text
            surface (pygame.surface.Surface) - tela do pygame
        
        Return:
            Objeto renderizado na tela
        """
        
        if self.form == "line":
            pg.draw.line(surface, self.color, (self.lineCoordinates[0], self.lineCoordinates[1]), (self.lineCoordinates[2], self.lineCoordinates[3]), self.width)

class Text():
    """
    Classe para criação de objetos do tipo Text.
    """
    def __init__(self, name, save=True, font="Candara Bold", size=16, color=[0, 0, 0], background=None, text="Olá mundo!", position=[0, 0], visible=True, zOrder=0, antialias=False):
        """
        Constrói objeto Text.
        
        Parâmetros:
            self (game_utils.Text) - objeto da classe Text
            name (str) - nome do objeto
            save (bool) - adiciona objeto em d_objects
            size (int) - tamanho da fonte
            font (str) - nome da fonte
            color (list) - cor da fonte
            background (tuple) - cor de fundo
            text (str) - texto
            position (list) - posição do Text
            visible (bool) - visibilidade do objeto
            zOrder (int) - ordenação na janela
            antialias (bool) - ativa/desativa anti-aliasing da fonte
        
        Return:
            Objeto
        """
        
        self.name = name
        self.font_style = font
        self.size = size
        self.font = pg.font.SysFont(font, size)
        self.color = color
        self.background = background
        self.text = text
        self.position = position
        self.visible = visible
        self.zOrder = zOrder
        self.antialias = antialias
        self.timer_0 = 0
        
        if save:
            c["d_objects"][self.name] = self
    
    def draw_object(self, surface):
        """
        Desenha Text na tela.
        
        Parâmetros:
            self (game_utils.Text) - objeto da classe Text
            surface (pygame.surface.Surface) - tela do pygame
        
        Return:
            Objeto renderizado na tela
        """
        
        if self.visible == True:
            lines = self.text.split("\n")
            for i in range(len(lines)):
                position = (self.position[0], self.position[1] + ((self.size + 0) * i))
                surface.blit(self.font.render(lines[i], self.antialias, self.color, self.background), position)
                
    def set_size(self, newSize):
        """
        Atualiza tamanho da fonte.
        
        Parâmetros:
            newSize (int) - novo tamanho
        
        Return:
            Fonte com tamanho atualizado
        """
        
        self.size = newSize
        self.font = pg.font.SysFont(self.font_style, self.size)
        
    def set_position(self, x, y):
        """
        Atualiza posição do objeto.
        
        Parâmetros:
            x (float) - x do objeto
            y (float) - y do objeto
            
        Retorno:
            Posição de objeto atualiza
        """
        
        self.position = [x, y]
        
    def flickering_background(self, target, color1, color2):
        """
        Ativa flickering de cor para background.
        
        Parâmetros:
            target (int) - atraso
            
        Retorno:
            Cor do background do objeto atualizado
        """
        
        if self.timer_0 == 0:
            self.background = color1
        if self.timer_0 == target:
            self.background = color2
        self.timer_0 += 1
        if self.timer_0 == target * 2:
            self.timer_0 = 0

class SpriteObject(pg.sprite.Sprite):
    """
    Classe para criação de objetos do tipo SpriteObject.
    """
    def __init__(self, name, save=True, position=[0, 0], image=pg.Surface((16, 16)), visible=True, zOrder=0, animation=None, frame=0, imageSize=None, color=(0, 0, 0)):
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
            animation (str) - nome da animação
            frame (int) - número do frame da animação
            imageSize (tuple) - altura e largura da imagem do objeto
            color (tuple) - cor de preenchimento da imagem
        
        Retorno:
            SpriteObject     
        """    

        pg.sprite.Sprite.__init__(self)
        self.name = name
        self.rect = pg.Rect((position[0], position[1], 16, 16))
        self.image = image
        self.visible = visible
        self.zOrder = zOrder
        self.animation = animation
        self.frame = frame
        self.color = color
        self.timer_0 = 0
        
        if animation != None: 
            self.d_sprites = load_sprites(name)
            self.image = self.d_sprites[animation][frame]
        else: 
            self.d_sprites = None
            self.image.fill(color)

        if imageSize != None:
            self.imageSize = imageSize
            self.image = pg.transform.scale(self.image, self.imageSize)
        else:
            self.imageSize = (image.get_width(), image.get_height())
        
        if save:
            c["d_objects"][self.name] = self
            #c["spriteGroup"].add(self, layer=self.zOrder)
    
    def set_position(self, x, y):
        """
        Atualiza posição do objeto.
        
        Parâmetros:
            x (float) - x do objeto
            y (float) - y do objeto
            
        Retorno:
            Posição de objeto atualiza
        """
        
        self.rect.x = x
        self.rect.y = y
    
    def switch_visible(self, visible=None):
        """
        Ativa/desativa visibilidade do objeto.
        
        Parâmetros:
            visible (bool) - defini visibilidade do objeto
            
        Retorno:
            Visibilidade do objeto atualizada
        """
        
        if visible == None:
            if self.visible == True:
                self.visible = False
            else:
                self.visible = True
        else:
            self.visible = visible
    
    def flickering(self, target):
        """
        Ativa flickering.
        
        Parâmetros:
            target (int) - atraso
            
        Retorno:
            Visibilidade do objeto atualizada
        """
        
        if self.timer_0 == 0:
            self.switch_visible()
        if self.timer_0 == target:
            self.switch_visible()
        self.timer_0 += 1
        if self.timer_0 == target * 2:
            self.timer_0 = 0
    
    def draw_object(self, surface):
        """
        Desenha SpriteObject na tela.
        
        Parâmetros:
            self (game_utils.SpriteObject) - objeto da classe SpriteObject
            surface (pygame.surface.Surface) - tela do pygame
        
        Return:
            Objeto renderizado na tela
        """
        
        if self.visible == True:
            surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def set_imageSize(self, width, height):
        """
        Atualiza tamanho da imagem do objeto.
        
        Parâmetros:
            width (float) - largura do objeto
            height (float) - altura do objeto
            
        Retorno:
            Tamanho da imagem do objeto atualiza
        """
        
        self.imageSize = (width, height)
        self.image = pg.transform.scale(self.image, self.imageSize)
        
    def set_imageFill(self, newColor):
        """
        Preenche área da imagem com uma nova cor.
        
        Parâmetros:
            newColor (tuple) - nova cor
            
        Retorno:
            Área da imagem preenchida com nova cor
        """
        
        self.image.fill(newColor)
        
    def set_animation(self, animation, frame=0):
        """
        Defini a animação e frame do objeto.
        
        Parâmetros:
            animation (str) - nome da animação
            frame (int) - número do frame da animação
            
        Retorno:
            Animação e frame definidos
        """
        
        self.animation = animation
        self.frame = frame
        self.image = self.d_sprites[self.animation][self.frame]