import pygame
import sys
from  simulation import Simulation
from parsing import Parser

WINDOW_W, WINDOW_H = 1300, 800
MARGIN = 100
STEP = 0.003
PAUSE_MS = 1000
ZONE_COLOR = {
    "normal":     (100, 200, 255),
    "priority":   (255, 215, 0),
    "restricted": (220, 60, 60),
    "blocked":    (110, 110, 110),
    "start":      (120, 255, 150),
    "end":        (255, 200, 60),
}

class visualisation():
    def __init__(self,graph, history) -> None:
        self.graph = graph
        self.history = history

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W,WINDOW_H))
        pygame.display.set_caption("Fly-in")
        clock = pygame.time.Clock()
        # self.test_front = pygame.font.Font('front/Pixel_Game.otf', 40)

        self.image = pygame.image.load('visulaliser/alien/fly.jpg')
        # text_surface = test_front.render("Fly-In", False, 'White')
        self.alien_surface = pygame.image.load('visulaliser/alien/alien.png')
        self.alien_surface = pygame.transform.scale(self.alien_surface, (90,90))
        self.alien_drone = pygame.image.load("visulaliser/alien/drone_sprite.png")
        self.alien_drone = pygame.transform.scale(self.alien_drone, (50,50))
        self.blocked_zone = pygame.image.load("visulaliser/alien/blocked_zone.jpeg")
        self.blocked_zone = pygame.transform.scale(self.blocked_zone,(70, 70))

        aliens = [
            {"start": (1300,40), "end": (-60,40)},
            {"start": (1000, 800), "end": (1300, 400)},
            {"start": (-90, 200), "end": (100, 800)},
        ]

        self.current_alien = 0
        self.progress = 0
        self.pause = False
        self.pause_start = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.image,(0,0))
            if self.current_alien < len(aliens):
                if self.pause:
                    if pygame.time.get_ticks() - self.pause_start > 1000:
                        self.pause = False
                        self.progress = 0
                else:
                    self.progress += 0.003
                    if self.progress >= 1:
                        self.pause = True
                        self.pause_start = pygame.time.get_ticks()
                        self.progress = 0
                        self.current_alien = (self.current_alien + 1) % len(aliens)
                start = aliens[self.current_alien]["start"]
                end = aliens[self.current_alien]["end"]

                x = start[0] + (end[0] - start[0]) * self.progress
                y = start[1] + (end[1] - start[1]) * self.progress

                self.screen.blit(self.alien_surface, (x, y))
            pygame.display.update()
            clock.tick(60)
    
    def zones_positions(self) -> dict:
        zones = list(self.graph.zones())

        xs = [z.x for z in zones]
        ys = [y.x for y in zones]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        span_x = max(max_x - min_x, 1)
        span_y = max(max_y - min_y, 1)

        positions = {}
        for z in zones:
            px = MARGIN + (z.x - min_x) / span_x + (WINDOW_W - 2 * MARGIN)
            py = MARGIN + (z.y - min_y) / span_y + (WINDOW_H - 2 * MARGIN)
            positions[z.name] = (px, py)
        return positions
  
    def _zone_type_of(self, name):
        zone = self.graph.zones[name]
        if zone is self.graph.start:
            return "start"
        if zone is self.graph.end:
            return "end"
        
        return zone.zone_type

    def connections_position(self):
        Connections_value: set = set()
        pairs = []
        for zone in self.graph.zones.value():
            for neighbor in zone.neighbors():
                pair = tuple(sorted((zone.name, neighbor.name)))
                if pair not in Connections_value:
                    Connections_value.append(pair)
        return Connections_value
    
    def _draw_connections(self):
        for name1, name2 in self._connection_pairs():
            pygame.draw.line(self.screen, (200, 200, 200), self.positions[name1], self.positions[name2], 2)

    
    def _draw_zones(self):
        for name, pos in self.positions.items():
            zone_type = self._zone_type_of(name)
            if zone_type == "blocked":
                self.screen.blit(self.blocked_surface, (pos[0]) - 35 ,pos[1] - 35)
            else:
                color = ZONE_COLOR.get(zone_type, ZONE_COLOR["normal"])
                pygame.draw.circle(self.screen, color, pos, 18)
            label = self.font.render(name, True, (255, 255, 255))
            self.screen.blit(label, (pos[0] - label.get_width() / 2, pos[1] + 40))
        
        

def main():
    filepath = "map/my_maps.txt"
    parser = Parser()
    graph = parser.parse(filepath)
    simulation = Simulation(graph)
    simulation.give_me_all_paths()
    simulation.run()
    vis = visualisation(simulation.graph, simulation.data)
    vis._draw_zones()
    vis._draw_connections()
main()