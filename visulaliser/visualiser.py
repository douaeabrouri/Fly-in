import pygame
import sys
from models import Graph, Connection, Zone
from simulation import Simulation
from parsing import Parser

WINDOW_W, WINDOW_H = 1300, 800
MARGIN = 100
STEP = 0.003
PAUSE_MS = 1000

class visualisation():
    def __init__(self,graph, history) -> None:
        self.graph = graph
        self.history = history

        pygame.init()
        screen = pygame.display.set_mode((WINDOW_W,WINDOW_H))
        pygame.display.set_caption("Fly-in")
        clock = pygame.time.Clock()
        test_front = pygame.font.Font('front/Pixel_Game.otf', 40)

        image = pygame.image.load('alien/fly.jpg')
        # text_surface = test_front.render("Fly-In", False, 'White')
        alien_surface = pygame.image.load('alien/alien.png')
        alien_surface = pygame.transform.scale(alien_surface, (90,90))

        aliens = [
            {"start": (1300,40), "end": (-60,40)},
            {"start": (1000, 800), "end": (1300, 400)},
            {"start": (-90, 200), "end": (100, 800)},
        ]

        current_alien = 0
        progress = 0
        pause = False
        pause_start = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.blit(image,(0,0))
            if current_alien < len(aliens):
                if pause:
                    if pygame.time.get_ticks() - pause_start > 1000:
                        pause = False
                        progress = 0
                else:
                    progress += 0.003
                    if progress >= 1:
                        pause = True
                        pause_start = pygame.time.get_ticks()
                        progress = 0
                        current_alien = (current_alien + 1) % len(aliens)
                start = aliens[current_alien]["start"]
                end = aliens[current_alien]["end"]

                x = start[0] + (end[0] - start[0]) * progress
                y = start[1] + (end[1] - start[1]) * progress

                screen.blit(alien_surface, (x, y))
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
            
    def connections_position(self):
        pass


def main():
    filepath = "map/my_maps.txt"
    parser = Parser()
    graph = parser.parse(filepath)
    simulation = Simulation(graph)
    simulation.give_me_all_paths()
    simulation.run()
    vis = visualisation(simulation.graph, simulation.run())
main()