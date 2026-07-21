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

        self.image = pygame.image.load('visulaliser/alien/fly.jpeg')
        # text_surface = test_front.render("Fly-In", False, 'White')
        self.alien_surface = pygame.image.load('visulaliser/alien/alien.png')
        self.alien_surface = pygame.transform.scale(self.alien_surface, (90,90))
        self.alien_drone = pygame.image.load("visulaliser/alien/alien_drone.png")
        self.alien_drone = pygame.transform.scale(self.alien_drone, (50,50))
        self.blocked_zone = pygame.image.load("visulaliser/alien/blocked_zone.png")
        self.blocked_zone = pygame.transform.scale(self.blocked_zone,(70, 70))
        self.goal_zone = pygame.image.load("visulaliser/alien/goal.png")
        self.goal_zone = pygame.transform.scale(self.goal_zone, (90, 90))
        self.start_zone = pygame.image.load("visulaliser/alien/start_zone.png")
        self.start_zone = pygame.transform.scale(self.start_zone, (90, 90))
        self.priority_zone = pygame.image.load("visulaliser/alien/priority_zone.png")
        self.priority_zone = pygame.transform.scale(self.priority_zone, (90, 90))
        self.normal_zone = pygame.image.load("visulaliser/alien/normal_zone.png")
        self.normal_zone = pygame.transform.scale(self.normal_zone, (70, 70))       
        self.station_zone = pygame.image.load("visulaliser/alien/space_station.png")
        self.station_zone = pygame.transform.scale(self.station_zone, (70, 70))

        aliens = [
            {"start": (1300,40), "end": (-60,40)},
            {"start": (1000, 800), "end": (1300, 400)},
            {"start": (-90, 200), "end": (100, 800)},
        ]

        self.turn_index: int = 0
        self.positions = self.zones_positions()
        self.current_alien = 0
        self.progress = 0.0
        self.pause = False
        self.pause_start = 0
        self.stations = {}
        self.transit_origin: dict[int, str] = {}
        self.create_all_stations()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(self.image,(0,0))
            self._draw_connections()
            self._draw_zones()
            self._draw_stations()
            self._draw_drones()

            if self.turn_index < len(self.history) - 1:
                # print("DRAW", self.progress))
                if self.pause:
                    print("PAUSE IS TRUE")
                    print(f"the timing is : ${pygame.time.get_ticks() - self.pause_start}")
                    if pygame.time.get_ticks() - self.pause_start > 1000:
                        print("RESETING SELF TO FALSE")
                        self.pause = False
                else:
                    # print("UPDATE", self.progress)
                    print("PAUSE IS FALSE")
                    self.progress += 0.008
                    if self.progress >= 0.99:
                        self.pause = True
                        self.pause_start = pygame.time.get_ticks()
                        self.progress = 0
                        self.turn_index += 1
                        # if self.turn_index < len(self.history) - 1:
                        #     self.pause = True
                # start = aliens[self.current_alien]["start"]
                # end = aliens[self.current_alien]["end"]

                # x = start[0] + (end[0] - start[0]) * self.progress
                # y = start[1] + (end[1] - start[1]) * self.progress

                # self.screen.blit(self.alien_surface, (x, y))

            pygame.display.update()
            clock.tick(60)
    
    def zones_positions(self) -> dict:
        zones = list(self.graph.zones.values())

        xs = [z.x for z in zones]
        ys = [z.y for z in zones]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        span_x = max(max_x - min_x, 1)
        span_y = max(max_y - min_y, 1)

        positions = {}
        for z in zones:
            px = MARGIN + ((z.x - min_x) / span_x) * (WINDOW_W - 2 * MARGIN)
            py = MARGIN + ((z.y - min_y) / span_y) * (WINDOW_H - 2 * MARGIN)
            positions[z.name] = (px, py)
        graph_center_x = sum(p[0] for p in positions.values()) / len(positions)
        graph_center_y = sum(p[1] for p in positions.values()) / len(positions)
        
        offset_x = WINDOW_W / 2 - graph_center_x
        offset_y = WINDOW_H / 2 - graph_center_y
        for name, (x, y) in positions.items():
            positions[name] = (x + offset_x, y + offset_y)
        return positions
  
    def _zone_type_of(self, name):
        zone = self.graph.zones[name]
        if zone is self.graph.start:
            return "start"
        if zone is self.graph.end:
            return "end"
        return zone.zone_type

    def connections_position(self):
        return [(c.zone_a.name, c.zone_b.name) for c in self.graph.connections]
    
    def _draw_connections(self):
        for name1, name2 in self.connections_position():
            pygame.draw.line(self.screen, (200, 200, 200), self.positions[name1], self.positions[name2], 2)
            
    def _draw_zones(self):
        for name, pos in self.positions.items():
            zone_type = self._zone_type_of(name)
            if zone_type == "blocked":
                self.screen.blit(self.blocked_zone, (pos[0] - 35 ,pos[1] - 35))
            else:
                color = ZONE_COLOR.get(zone_type, ZONE_COLOR["normal"])
                pygame.draw.circle(self.screen, color, pos, 18)
            my_font = pygame.font.Font(None, 24)
            label_surface = my_font.render(name,True, (255, 255, 255))
            self.screen.blit(label_surface, (pos[0] - label_surface.get_width() / 2, pos[1] + 40))
    
    def create_all_stations(self):
        for connection in self.graph.connections:
            zone_a = connection.zone_a.name
            zone_b = connection.zone_b.name

            start = self.positions[zone_a]
            end = self.positions[zone_b]

            station_x = (start[0] + end[0]) / 2
            station_y = (start[1] + end[1]) / 2
            self.stations[(zone_a, zone_b)] = (station_x, station_y)

    def _draw_stations(self):
        for (from_zone, to_zone), (station_x, station_y) in self.stations.items():
            zone = self.graph.zones[to_zone]

            if zone.zone_type != "restricted":
                continue

            self.screen.blit(
                self.station_zone,
                (station_x - 35, station_y - 35)
            )

    def _draw_drones(self):
        if self.turn_index >= len(self.history) - 1:
            return
        frame_from = self.history[self.turn_index]
        frame_to = self.history[self.turn_index + 1]
        # print("FRAME_FROM =", frame_from)
        # print("FRAME_TO   =", frame_to)
        for drone_id, to_zone in frame_to.items():
            self.positions = self.zones_positions()
            from_zone = frame_from.get(drone_id)
            if from_zone is None:
                continue
            
            if (
                isinstance(from_zone, str)
                and not from_zone.startswith(("waiting_", "moving_waiting_"))
                and isinstance(to_zone, str)
                and to_zone.startswith("moving_waiting_")
            ):
                # print("LEG 1")
                real_zone = to_zone.replace("moving_waiting_", "")
                self.transit_origin[drone_id] = from_zone

                if from_zone not in self.positions or real_zone not in self.positions :
                    continue
                    
                    
                station_x, station_y = self.stations[(from_zone, real_zone)]
                first_pos = self.positions[from_zone]
                x = first_pos[0] + (
                    station_x - first_pos[0]
                ) * self.progress

                y = first_pos[1] + (
                    station_y - first_pos[1]
                ) * self.progress
                offset = drone_id * 10
                self.screen.blit(
                    self.alien_drone,
                    (x - 25 + offset, y - 25)
                )
                continue
            if (
                isinstance(from_zone, str)
                and from_zone.startswith("moving_waiting_")
                and isinstance(to_zone, str)
                and to_zone.startswith("waiting_")
            ):
                # print("LEG 2")

                real_zone = to_zone.replace("waiting_", "")
                origin_zone = self.transit_origin.get(drone_id)

                if origin_zone is None:
                    continue

                x, y = self.stations[(origin_zone, real_zone)]
                offset = drone_id * 10
                self.screen.blit(
                    self.alien_drone,
                    (x - 25 + offset, y - 25)
                )

                continue
            if isinstance(from_zone, str) and from_zone.startswith("waiting_"):
                # print("LEG 3")
                # print(
                #     "LEG3",
                #     "progress=", self.progress,
                #     "pause=", self.pause
                # )
                # print(self.pause)
                origin_zone = self.transit_origin.get(drone_id)
                if origin_zone is None or to_zone not in self.positions:
                    continue
                station_x, station_y = self.stations[(origin_zone, to_zone)]
                end_x, end_y = self.positions[to_zone]
                x = station_x + (end_x - station_x) * self.progress
                y = station_y + (end_y - station_y) * self.progress
                offset = drone_id * 10
                self.screen.blit(self.alien_drone, (x - 25 + offset, y - 25))
                continue


            if from_zone not in self.positions:
                continue
            if to_zone not in self.positions:
                continue
            start = self.positions[from_zone]
            end = self.positions[to_zone]      
            x = start[0] + (end[0] - start[0]) * self.progress
            y = start[1] + (end[1] - start[1]) * self.progress  
            offset = drone_id * 10
            self.screen.blit(self.alien_drone, (x - 25 + offset, y - 25))
            continue

def main():
    filepath = "map/my_maps.txt"
    parser = Parser()
    graph = parser.parse(filepath)
    simulation = Simulation(graph)
    simulation.give_me_all_paths()
    data = simulation.run()
    vis = visualisation(simulation.graph, data)
main()
