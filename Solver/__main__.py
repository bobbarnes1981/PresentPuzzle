"""PresentPuzzle"""

# python imports
import argparse
import logging
import os
import time

# external imports
import pygame

class Node:
    """"""
    def __init__(self, name:str, presents:int, x:int, y:int) -> None:
        """"""
        self.name = name
        self.presents = presents
        self.__x = x
        self.__y = y
    def get_location(self, scale) -> tuple[float, float]:
        """"""
        return (self.__x/scale, self.__y/scale)
    def draw(self, surface:pygame.Surface, font:pygame.font.Font, scale:float, current:bool) -> None:
        """"""
        colour = (0x00, 0xff, 0x00) if current else (0xff, 0x00, 0x00)
        location = self.get_location(scale)
        radius = 5
        pygame.draw.circle(surface, colour, location, radius)
        colour = (0x00, 0x00, 0x00)
        img = font.render(str("{0} ({1})".format(self.name, self.presents)), True, colour)
        left = location[0] - img.get_width()
        top = location[1] - img.get_height()
        surface.blit(img, (left, top))

class Edge:
    """"""
    def __init__(self, a:Node, b:Node, minutes:int) -> None:
        """"""
        self.a = a
        self.b = b
        self.minutes = minutes
    def draw(self, surface:pygame.Surface, font:pygame.font.Font, scale:float) -> None:
        """"""
        colour = (0x00, 0x00, 0xff)
        start = self.a.get_location(scale)
        end = self.b.get_location(scale)
        width = 3
        pygame.draw.line(surface, colour, start, end, width)
        colour = (0x00, 0x00, 0x00)
        img = font.render(str(self.minutes), True, colour)
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
    def has_node(self, node_name:str) -> bool:
        return self.a.name == node_name or self.b.name == node_name
    def get_other_node(self, node_name:str) -> Node:
        if self.a.name == node_name:
            return self.b
        return self.a

class Network:
    """"""
    def __init__(self) -> None:
        aberdeen        = Node("Aberdeen", 8, 1184, 533)
        belfast         = Node("Belfast", 12, 688, 1075)
        birmingham      = Node("Birmingham", 15, 1212, 1573)
        blackpool       = Node("Blackpool", 7, 1058, 1274)
        brighton        = Node("Brighton", 6, 1459, 1936)
        cardiff         = Node("Cardiff", 13, 1032, 1791)
        carlisle        = Node("Carlisle", 4, 1076, 1035)
        cork            = Node("Cork", 9, 309, 1668)
        dover           = Node("Dover", 3, 1658, 1861)
        dublin          = Node("Dublin", 10, 632, 1364)
        edinburgh       = Node("Edinburgh", 15, 1047, 800)
        fort_william    = Node("Fort William", 2, 819, 597)
        glasgow         = Node("Glasgow", 6, 916, 817)
        london          = Node("London", 18, 1460, 1784)
        manchester      = Node("Manchester", 14, 1164, 1351)
        newcastle       = Node("Newcastle", 11, 1246, 1017)
        norwich         = Node("Norwich", 8, 1643, 1528)
        nottingham      = Node("Nottingham", 5, 1311, 1468)
        plymouth        = Node("Plymouth", 14, 890, 2035)
        southampton     = Node("Southampton", 2, 1280, 1920)
        swansea         = Node("Swansea", 7, 927, 1759)
        york            = Node("York", 13, 1317, 1242)
        self.nodes = {
            aberdeen.name:      aberdeen,
            belfast.name:       belfast,
            birmingham.name:    birmingham,
            blackpool.name:     blackpool,
            brighton.name:      brighton,
            cardiff.name:       cardiff,
            carlisle.name:      carlisle,
            cork.name:          cork,
            dover.name:         dover,
            dublin.name:        dublin,
            edinburgh.name:     edinburgh,
            fort_william.name:  fort_william,
            glasgow.name:       glasgow,
            london.name:        london,
            manchester.name:    manchester,
            newcastle.name:     newcastle,
            norwich.name:       norwich,
            nottingham.name:    nottingham,
            plymouth.name:      plymouth,
            southampton.name:   southampton,
            swansea.name:       swansea,
            york.name:          york,
        }
        self.edges = [
            Edge(plymouth, cork, 8),
            Edge(plymouth, cardiff, 5),
            Edge(plymouth, southampton, 4),

            Edge(southampton, cardiff, 2),
            Edge(southampton, london, 3),
            Edge(southampton, brighton, 2),
            
            Edge(brighton, london, 2),
            Edge(brighton, dover, 3),
            
            Edge(dover, london, 2),
            
            Edge(london, birmingham, 3),
            Edge(london, norwich, 3),
            
            Edge(norwich, birmingham, 4),
            Edge(norwich, nottingham, 3),
            Edge(norwich, york, 3),
            
            Edge(cardiff, swansea, 1),
            Edge(cardiff, birmingham, 2),

            Edge(birmingham, manchester, 3),
            Edge(birmingham, nottingham, 2),

            Edge(swansea, cork, 5),
            Edge(swansea, dublin, 6),

            Edge(cork, dublin, 4),

            Edge(dublin, belfast, 2),
            Edge(dublin, manchester, 5),

            Edge(belfast, glasgow, 4),
            Edge(belfast, carlisle, 5),
            Edge(belfast, manchester, 7),

            Edge(york, nottingham, 2),
            Edge(york, manchester, 2),
            Edge(york, blackpool, 3),
            Edge(york, carlisle, 4),
            Edge(york, newcastle, 4),

            Edge(blackpool, manchester, 2),
            Edge(blackpool, carlisle, 1),
            
            Edge(carlisle, newcastle, 1),
            Edge(carlisle, glasgow, 3),
            
            Edge(glasgow, newcastle, 3),
            Edge(glasgow, fort_william, 2),
            Edge(glasgow, edinburgh, 1),
            
            Edge(fort_william, edinburgh, 2),

            Edge(aberdeen, fort_william, 4),
            Edge(aberdeen, edinburgh, 3),
        ]
        self.current_node = plymouth.name
    def draw(self, surface:pygame.Surface, font:pygame.font.Font, scale:float) -> None:
        for edge in self.edges:
            edge.draw(surface, font, scale)
        for key in self.nodes:
            self.nodes[key].draw(surface, font, scale, True if key == self.current_node else False)
    def get_edges(self, node_name:str) -> list[Edge]:
        e:list[Edge] = []
        for edge in self.edges:
            if edge.has_node(node_name):
                e.append(edge)
        return e

class SolveOneHourMaxPresents:
    """"""
    def __init__(self, network:Network) -> None:
        """"""
        self.network = network
        self.__visited = []
        self.__presents = 0
        self.__elapsed = 0
        self.__maximum_elapsed = 60
        self.finished = False
    def step(self) -> None:
        """"""
        logging.info("Location: %s Presents: %s  Elapsed: %s", self.network.current_node, self.__presents, self.__elapsed)
        edges = self.network.get_edges(self.network.current_node)
        chosen = None
        highest = 0
        visited_edges:list[Edge] = []
        for edge in edges:
            if edge.minutes + self.__elapsed > self.__maximum_elapsed:
                # skip nodes that mean we have taken too long
                continue
            other = edge.get_other_node(self.network.current_node)
            if other.name in self.__visited:
                # skip nodes that have been visited
                visited_edges.append(edge)
                continue
            presents = other.presents
            pm = presents/edge.minutes
            logging.info("Node: %s Presents: %s Minutes: %s ppm: %s", other.name, presents, edge.minutes, pm)
            if chosen is None or pm > highest:
                chosen = edge
                highest = pm

        if chosen is None:
            logging.info("Visited all edges")
            lowest = 0
            for edge in visited_edges:
                if chosen is None or edge.minutes < lowest:
                    chosen = edge
                    lowest = edge.minutes

        if chosen is None:
            logging.info("Finished")
            self.finished = True
            return

        dest = chosen.get_other_node(self.network.current_node)
        logging.info("Travelling to: %s", dest.name)

        self.network.current_node = dest.name
        self.__visited.append(dest.name)
        self.__presents += dest.presents
        self.__elapsed += chosen.minutes

class App:
    """"""
    def __init__(self, delay:float) -> None:
        self.__running = True
        self.__display_surf = None
        self.__time = time.time()
        self.__counter = 0
        self.__steps = 0
        self.__delay = delay
        self.__size = None
        self.__scale = 3
        self.__solver = SolveOneHourMaxPresents(Network())
    def on_render(self) -> None:
        self.__display_surf.blit(self.__map, self.__map_rect)
        self.__solver.network.draw(self.__display_surf, self.__font, self.__scale)
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
            self.__steps += 1
            if self.__steps > 3 and self.__solver.finished is False:
                self.__solver.step()
            self.__counter = 0
    def on_init(self) -> None:
        """Init"""
        pygame.init()
        pygame.display.set_caption("Solver")
        self.__running = True
        font_name = pygame.font.get_default_font()
        logging.info("Font: %s", font_name)
        self.__font = pygame.font.SysFont(font_name, 18)

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

    app = App(args.delay)
    app.on_execute()

