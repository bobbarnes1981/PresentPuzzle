"""PresentPuzzle"""

# python imports
import argparse
import logging
import os
import time

# external imports
import pygame

class Location:
    """"""
    def __init__(self, name:str, presents:int, x:int, y:int) -> None:
        """"""
        self.__name = name
        self.__present = presents
        self.__x = x
        self.__y = y
    def get_location(self, scale) -> tuple[float, float]:
        """"""
        return (self.__x/scale, self.__y/scale)
    def draw(self, surface:pygame.Surface, scale:float) -> None:
        """"""
        colour = (0xff, 0x00, 0x00)
        location = self.get_location(scale)
        radius = 5
        pygame.draw.circle(surface, colour, location, radius)

class Link:
    """"""
    def __init__(self, a:Location, b:Location, minutes:int) -> None:
        """"""
        self.__a = a
        self.__b = b
        self.__minutes = minutes
    def draw(self, surface:pygame.Surface, font:pygame.font.Font, scale:float) -> None:
        """"""
        colour = (0x00, 0x00, 0xff)
        start = self.__a.get_location(scale)
        end = self.__b.get_location(scale)
        width = 3
        pygame.draw.line(surface, colour, start, end, width)
        colour = (0x00, 0x00, 0x00)
        img = font.render(str(self.__minutes), True, colour)
        if start[0] < end[0]:
            left = start[0] + ((end[0]-start[0])/2)
        else:
            left = end[0] + ((start[0]-end[0])/2)
        if start[1] < end[1]:
            top = start[1] + ((end[1]-start[1])/2)
        else:
            top = end[1] + ((start[1]-end[1])/2)
        colour = (0xff, 0xff, 0x00)
        pygame.draw.circle(surface, colour, (left, top), 10)
        left = left - (img.get_width()/2)
        top = top  - (img.get_height()/2)
        surface.blit(img, (left, top))

class App:
    """"""
    def __init__(self, delay:float) -> None:
        self.__running = True
        self.__display_surf = None
        self.__time = time.time()
        self.__counter = 0
        self.__delay = 1.0
        self.__size = None
        self.__scale = 3

        aberdeen    = Location("Aberdeen", 8, 1184, 533)
        belfast     = Location("Belfast", 12, 688, 1075)
        birmingham  = Location("Birmingham", 15, 1212, 1573)
        blackpool   = Location("Blackpool", 7, 1058, 1274)
        brighton    = Location("Brighton", 6, 1459, 1936)
        cardiff     = Location("Cardiff", 13, 1032, 1791)
        carlisle    = Location("Carlisle", 4, 1076, 1035)
        cork        = Location("Cork", 9, 309, 1668)
        dover       = Location("Dover", 3, 1658, 1861)
        dublin      = Location("Dublin", 10, 632, 1364)
        edinburgh   = Location("Edinburgh", 15, 1047, 800)
        fortWilliam = Location("Fort William", 2, 819, 597)
        glasgow     = Location("Glasgow", 6, 916, 817)
        london      = Location("London", 18, 1460, 1784)
        manchester  = Location("Manchester", 14, 1164, 1351)
        newcastle   = Location("Newcastle", 11, 1246, 1017)
        norwich     = Location("Norwich", 8, 1643, 1528)
        nottingham  = Location("Nottingham", 5, 1311, 1468)
        plymouth    = Location("Plymouth", 14, 890, 2035)
        southampton = Location("Southampton", 2, 1280, 1920)
        swansea     = Location("Swansea", 7, 927, 1759)
        york        = Location("York", 13, 1317, 1242)
        self.__locations = [
            aberdeen,
            belfast,
            birmingham,
            blackpool,
            brighton,
            cardiff,
            carlisle,
            cork,
            dover,
            dublin,
            edinburgh,
            fortWilliam,
            glasgow,
            london,
            manchester,
            newcastle,
            norwich,
            nottingham,
            plymouth,
            southampton,
            swansea,
            york,
        ]
        self.__links = [
            Link(plymouth, cork, 8),
            Link(plymouth, cardiff, 5),
            Link(plymouth, southampton, 4),

            Link(southampton, cardiff, 2),
            Link(southampton, london, 3),
            Link(southampton, brighton, 2),
            
            Link(brighton, london, 2),
            Link(brighton, dover, 3),
            
            Link(dover, london, 2),
            
            Link(london, birmingham, 3),
            Link(london, norwich, 3),
            
            Link(norwich, birmingham, 4),
            Link(norwich, nottingham, 3),
            Link(norwich, york, 3),
            
            Link(cardiff, swansea, 1),
            Link(cardiff, birmingham, 2),

            Link(birmingham, manchester, 3),
            Link(birmingham, nottingham, 2),

            Link(swansea, cork, 5),
            Link(swansea, dublin, 6),

            Link(cork, dublin, 4),

            Link(dublin, belfast, 2),
            Link(dublin, manchester, 5),

            Link(belfast, glasgow, 4),
            Link(belfast, carlisle, 5),
            Link(belfast, manchester, 7),

            Link(york, nottingham, 2),
            Link(york, manchester, 2),
            Link(york, blackpool, 3),
            Link(york, carlisle, 4),
            Link(york, newcastle, 4),

            Link(blackpool, manchester, 2),
            Link(blackpool, carlisle, 1),
            
            Link(carlisle, newcastle, 1),
            Link(carlisle, glasgow, 3),
            
            Link(glasgow, newcastle, 3),
            Link(glasgow, fortWilliam, 2),
            Link(glasgow, edinburgh, 1),
            
            Link(fortWilliam, edinburgh, 2),

            Link(aberdeen, fortWilliam, 4),
            Link(aberdeen, edinburgh, 3),
        ]
    def on_render(self) -> None:
        self.__display_surf.blit(self.__map, self.__map_rect)
        for link in self.__links:
            link.draw(self.__display_surf, self.__font, self.__scale)
        for location in self.__locations:
            location.draw(self.__display_surf, self.__scale)
        pygame.display.update()
    def on_event(self, event) -> None:
        """Handle event"""
        if event.type == pygame.QUIT:
            self.__running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                self.__running = False
        else:
            logging.debug(event)
    def on_loop(self, elapsed:float) -> None:
        """Execute step"""
        self.__counter += elapsed
        if self.__counter > self.__delay:
            logging.info("Step")
            self.__counter = 0
    def on_init(self) -> None:
        """Init"""
        pygame.init()
        pygame.display.set_caption("Solver")
        self.__running = True
        font_name = pygame.font.get_default_font()
        logging.info("Font: %s", font_name)
        self.__font = pygame.font.SysFont(font_name, 22)

        map = pygame.image.load(os.path.join("Over_gb", "GBOverviewPlus.tif"))

        crop_w = 1769
        crop_h = 2197
        self.__map = pygame.Surface((crop_w, crop_h))
        
        self.__map.blit(map, (0, 0), (902, 753, crop_w, crop_h))

        w = self.__map.get_width()
        h = self.__map.get_height()
        logging.info("(%s,%s)", w, h)

        w = w / self.__scale
        h = h / self.__scale
        self.__size = (w, h)
        self.__map = pygame.transform.scale(self.__map, (w, h))

        self.__map_rect = self.__map.get_rect()
        
        self.__display_surf = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        return True
    def on_cleanup(self) -> None:
        """Cleanup"""
        pygame.quit()
    def on_execute(self) -> None:
        """Execute application"""
        if not self.on_init():
            self.__running = False
        while self.__running:
            current = time.time()
            elapsed = current - self.__time
            self.__time = current
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(elapsed)
            self.on_render()
        self.on_cleanup()

if __name__ == '__main__':
    loglevels = [
        'DEBUG',
        'INFO',
        'WARNING',
        'ERROR',
        'CRITICAL'
    ]

    parser = argparse.ArgumentParser(description='solve puzzle')
    parser.add_argument('-d',
                        '--delay',
                        type=float,
                        required=False,
                        default=1.0,
                        dest='delay')
    parser.add_argument('-l',
                        '--logging',
                        type=str,
                        required=False,
                        default='INFO',
                        dest='logging',
                        choices=loglevels)
    args = parser.parse_args()

    loglevel = getattr(logging, args.logging, None)
    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(name)s %(message)s')

    a = App(args.delay)
    a.on_execute()

