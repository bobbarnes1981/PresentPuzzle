"""PresentPuzzle"""

# python imports
import argparse
import logging
import os
import time

# external imports
import pygame

class App:
    def __init__(self, delay:float) -> None:
        self.__running = True
        self.__display_surf = None
        self.__time = time.time()
        self.__counter = 0
        self.__delay = 1.0
        self.__size = None
    def on_render(self) -> None:
        self.__display_surf.blit(self.__map, self.__map_rect)
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

        self.__map = pygame.image.load(os.path.join("Over_gb", "GBOverviewPlus.tif"))
        w = self.__map.get_width()
        h = self.__map.get_height()
        logging.info("(%s,%s)", w, h)

        w = w / 5
        h = h / 5
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

