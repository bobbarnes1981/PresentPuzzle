"""PresentPuzzle"""

# python imports
import argparse
import logging
import os
import time

# external imports
import pygame

class Node:
    """Class representing a netowrk node"""
    def __init__(self, name: str, presents: int, x: int, y: int) -> None:
        """Initialise the node"""
        self.name: str = name
        self.presents: int = presents
        self.__x: int = x
        self.__y: int = y
    def get_scaled_location(self, scale: float) -> tuple[float, float]:
        """Get the scaled location of the node"""
        return (self.__x/scale, self.__y/scale)
    def draw(self, surface: pygame.Surface, font: pygame.font.Font, scale: float, current: bool) -> None:
        """Draw the node"""
        circle_colour: tuple = (0x00, 0xff, 0x00) if current else (0xff, 0x00, 0x00)
        location: tuple[float, float] = self.get_scaled_location(scale)
        radius: int = 5
        pygame.draw.circle(surface, circle_colour, location, radius)
        text_colour: tuple = (0x00, 0x00, 0x00)
        img: pygame.Surface = font.render(f"{self.name} ({self.presents})", True, text_colour)
        left: float = location[0] - img.get_width()
        top: float = location[1] - img.get_height()
        surface.blit(img, (left, top))

class Edge:
    """Class representing a network edge"""
    def __init__(self, a: Node, b: Node, minutes: int) -> None:
        """Initialise the edge"""
        self.a: Node = a
        self.b: Node = b
        self.minutes: int = minutes
    def draw(self, surface: pygame.Surface, font: pygame.font.Font, scale: float) -> None:
        """Draw the edge"""
        line_colour: tuple = (0x00, 0x00, 0xff)
        start: tuple[float, float] = self.a.get_scaled_location(scale)
        end: tuple[float, float] = self.b.get_scaled_location(scale)
        width: int = 3
        pygame.draw.line(surface, line_colour, start, end, width)
        text_colour: tuple = (0x00, 0x00, 0x00)
        img = font.render(str(self.minutes), True, text_colour)
        if start[0] < end[0]:
            left = start[0] + ((end[0]-start[0])/2)
        else:
            left = end[0] + ((start[0]-end[0])/2)
        if start[1] < end[1]:
            top = start[1] + ((end[1]-start[1])/2)
        else:
            top = end[1] + ((start[1]-end[1])/2)
        circle_colour: tuple = (0xff, 0xff, 0x00)
        pygame.draw.circle(surface, circle_colour, (left, top), 10)
        text_left: float = left - (img.get_width()/2)
        text_top: float = top  - (img.get_height()/2)
        surface.blit(img, (text_left, text_top))
    def has_node(self, node_name: str) -> bool:
        """Returns true if the edge references the node"""
        return node_name in (self.a.name, self.b.name)
    def get_other_node(self, node_name: str) -> Node:
        """Returns the name of the other node on the edge"""
        if self.a.name == node_name:
            return self.b
        return self.a

class Network:
    """Class representing a network"""
    def __init__(self) -> None:
        """Initialise the network"""
        # pylint: disable=too-many-locals
        aberdeen: Node      = Node("Aberdeen", 8, 1184, 533)
        belfast: Node       = Node("Belfast", 12, 688, 1075)
        birmingham: Node    = Node("Birmingham", 15, 1212, 1573)
        blackpool: Node     = Node("Blackpool", 7, 1058, 1274)
        brighton: Node      = Node("Brighton", 6, 1459, 1936)
        cardiff: Node       = Node("Cardiff", 13, 1032, 1791)
        carlisle: Node      = Node("Carlisle", 4, 1076, 1035)
        cork: Node          = Node("Cork", 9, 309, 1668)
        dover: Node         = Node("Dover", 3, 1658, 1861)
        dublin: Node        = Node("Dublin", 10, 632, 1364)
        edinburgh: Node     = Node("Edinburgh", 15, 1047, 800)
        fort_william: Node  = Node("Fort William", 2, 819, 597)
        glasgow: Node       = Node("Glasgow", 6, 916, 817)
        london: Node        = Node("London", 18, 1460, 1784)
        manchester: Node    = Node("Manchester", 14, 1164, 1351)
        newcastle: Node     = Node("Newcastle", 11, 1246, 1017)
        norwich: Node       = Node("Norwich", 8, 1643, 1528)
        nottingham: Node    = Node("Nottingham", 5, 1311, 1468)
        plymouth: Node      = Node("Plymouth", 14, 890, 2035)
        southampton: Node   = Node("Southampton", 2, 1280, 1920)
        swansea: Node       = Node("Swansea", 7, 927, 1759)
        york: Node          = Node("York", 13, 1317, 1242)
        self.nodes: dict[str, Node] = {
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
        self.edges: list[Edge] = [
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
    def draw(self, surface: pygame.Surface, font: pygame.font.Font, scale: float) -> None:
        """Draw the network"""
        for edge in self.edges:
            edge.draw(surface, font, scale)
        # pylint: disable=consider-using-dict-items
        for key in self.nodes:
            self.nodes[key].draw(surface, font, scale, key == self.current_node)
    def get_edges(self, node_name: str) -> list[Edge]:
        """Get a list of edges that reference the node"""
        e:list[Edge] = []
        for edge in self.edges:
            if edge.has_node(node_name):
                e.append(edge)
        return e

class SolveOneHourMaxPresents:
    """Solve for max presents in one hour, 183 presents in 59 minutes"""
    # pylint: disable=too-few-public-methods
    def __init__(self, network: Network) -> None:
        """Initialise the solver"""
        self.network: Network = network
        self.__visited: list[str] = []
        self.presents: int = 0
        self.elapsed: int = 0
        self.__maximum_elapsed: int = 60
        self.finished: bool = False
    def step(self) -> None:
        """Take one step"""
        logging.info("Location: %s Presents: %s  Elapsed: %s", self.network.current_node, self.presents, self.elapsed)
        edges: list[Edge] = self.network.get_edges(self.network.current_node)
        chosen: Edge|None = None
        highest: float = 0
        visited_edges: list[Edge] = []
        for edge in edges:
            if edge.minutes + self.elapsed > self.__maximum_elapsed:
                # skip nodes that mean we have taken too long
                continue
            other: Node = edge.get_other_node(self.network.current_node)
            if other.name in self.__visited:
                # skip nodes that have been visited
                visited_edges.append(edge)
                continue
            presents: int = other.presents
            pm: float = presents/edge.minutes
            logging.info("Node: %s Presents: %s Minutes: %s ppm: %s", other.name, presents, edge.minutes, pm)
            if chosen is None or pm > highest:
                chosen = edge
                highest = pm

        if chosen is None:
            logging.info("Visited all edges")
            lowest: int = 0
            for edge in visited_edges:
                if chosen is None or edge.minutes < lowest:
                    chosen = edge
                    lowest = edge.minutes

        if chosen is None:
            logging.info("Finished")
            self.finished = True
            return

        dest: Node = chosen.get_other_node(self.network.current_node)
        logging.info("Travelling to: %s", dest.name)

        self.network.current_node = dest.name
        self.__visited.append(dest.name)
        self.presents += dest.presents
        self.elapsed += chosen.minutes

class App:
    """Present Puzzle App"""
    # pylint: disable=too-many-instance-attributes
    def __init__(self, delay: float) -> None:
        """Initialise the application"""
        self.__running: bool = True
        self.__display_surf: pygame.Surface
        self.__font: pygame.font.Font
        self.__time: float = time.time()
        self.__counter: float = 0
        self.__steps: int = 0
        self.__delay: float = delay
        self.__size: tuple
        self.__scale: float = 3
        self.__solver = SolveOneHourMaxPresents(Network())
        self.__map: pygame.Surface
        self.__map_rect: pygame.Rect
    def on_render(self) -> None:
        """Render the application"""
        self.__display_surf.blit(self.__map, self.__map_rect)
        colour: tuple = (0x00, 0x00, 0x00)
        img: pygame.Surface = self.__font.render(f"Location: {self.__solver.network.current_node} Presents: {self.__solver.presents} Elapsed: {self.__solver.elapsed}", True, colour)
        left: int = 0
        top: int = 0
        self.__display_surf.blit(img, (left, top))
        self.__solver.network.draw(self.__display_surf, self.__font, self.__scale)
        pygame.display.update()
    def on_event(self, event: pygame.event.Event) -> None:
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
    def on_init(self) -> bool:
        """Init"""
        pygame.init()
        pygame.display.set_caption("Solver")
        self.__running: bool = True
        font_name: str = pygame.font.get_default_font()
        logging.info("Font: %s", font_name)
        self.__font = pygame.font.SysFont(font_name, 18)
        map_surface: pygame.Surface = pygame.image.load(os.path.join("Over_gb", "GBOverviewPlus.tif"))
        crop_w: int = 1769
        crop_h: int = 2197
        self.__map = pygame.Surface((crop_w, crop_h))
        self.__map.blit(map_surface, (0, 0), (902, 753, crop_w, crop_h))
        w: float = self.__map.get_width()
        h: float = self.__map.get_height()
        logging.info("(%s,%s)", w, h)
        w = w / self.__scale
        h = h / self.__scale
        self.__size = (w, h)
        self.__map = pygame.transform.scale(self.__map, (w, h))
        self.__map_rect = self.__map.get_rect()
        self.__display_surf = pygame.display.set_mode(self.__size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        return True
    def on_cleanup(self) -> None:
        """Cleanup the application"""
        pygame.quit()
    def on_execute(self) -> None:
        """Execute the application"""
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

    parser: argparse.ArgumentParser = argparse.ArgumentParser(description='solve puzzle')
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
