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
        self.__name = name
        self.__present = presents
        self.__x = x
        self.__y = y
    def draw(self, surface:pygame.Surface, scale:float) -> None:
        pygame.draw.circle(surface, (0xff, 0x00, 0x00), (self.__x/scale, self.__y/scale), 10)

class App:
    """"""
    def __init__(self, delay:float) -> None:
        self.__running = True
        self.__display_surf = None
        self.__time = time.time()
        self.__counter = 0
        self.__delay = 1.0
        self.__size = None
        self.__scale = 2.5
        self.__locations = [
            Location("Aberdeen", 8, 1184, 533),
            Location("Belfast", 12, 688, 1075),
            Location("Birmingham", 15, 1212, 1573),
            Location("Blackpool", 7, 1058, 1274),
            Location("Brighton", 6, 1459, 1936),
            Location("Cardiff", 13, 1032, 1791),
            Location("Carlisle", 4, 1076, 1035),
            Location("Cork", 9, 309, 1668),
            Location("Dover", 3, 1658, 1861),
            Location("Dublin", 10, 632, 1364),
            Location("Edinburgh", 15, 1047, 800),
            Location("Fort William", 2, 819, 597),
            Location("Glasgow", 6, 916, 817),
            Location("London", 18, 1460, 1784),
            Location("Manchester", 14, 1164, 1351),
            Location("Newcastle", 11, 1246, 1017),
            Location("Norwich", 8, 1643, 1528),
            Location("Nottingham", 5, 1311, 1468),
            Location("Plymouth", 14, 890, 2035),
            Location("Southampton", 2, 1280, 1920),
            Location("Swansea", 7, 927, 1759),
            Location("York", 13, 1317, 1242),
        ]
    def on_render(self) -> None:
        self.__display_surf.blit(self.__map, self.__map_rect)
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

