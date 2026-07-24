import pygame
import sys
from simulation import Simulation
from parsing import Parser

WINDOW_W, WINDOW_H = 1300, 800
MARGIN = 80
STEP = 0.003
PAUSE_MS = 1000

ZONE_COLOR = {
    "normal": (100, 200, 255),
    "priority": (255, 215, 0),
    "restricted": (220, 60, 60),
    "blocked": (110, 110, 110),
    "start": (120, 255, 150),
    "end": (255, 200, 60),
}


class visualisation:
    def __init__(self, graph, history) -> None:
        self.graph = graph
        self.history = history

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        pygame.display.set_caption("Fly-in")
        clock = pygame.time.Clock()

        self.image = pygame.image.load("visulaliser/alien/fly.jpeg")
        self.alien_surface = pygame.image.load("visulaliser/alien/alien.png")
        self.alien_surface = pygame.transform.scale(self.alien_surface, (90, 90))
        self.alien_drone = pygame.image.load("visulaliser/alien/alien_drone.png")
        self.alien_drone = pygame.transform.scale(self.alien_drone, (50, 50))
        self.blocked_zone = pygame.image.load("visulaliser/alien/blocked_zone.png")
        self.blocked_zone = pygame.transform.scale(self.blocked_zone, (70, 70))
        self.station_zone = pygame.image.load("visulaliser/alien/space_station.png")
        self.station_zone = pygame.transform.scale(self.station_zone, (55, 55))

        aliens = [
            {"start": (1300, 40), "end": (-60, 40)},
            {"start": (1000, 800), "end": (1300, 400)},
            {"start": (-90, 200), "end": (100, 800)},
        ]

        self.turn_index: int = 0
        self.positions = self.zones_positions(WINDOW_W, WINDOW_H, MARGIN)
        self.current_alien = 0
        self.progress = 0.0
        self.pause = False
        self.pause_start = 0
        self.stations = {}
        self.transit_origin: dict[int, str] = {}
        self.create_all_stations()
        self.aliens = aliens
        self.progress_for_animation: int = 0.0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.blit(self.image, (0, 0))
            self._draw_connections()
            self._draw_zones()
            self._draw_stations()
            self._draw_drones()

            if self.turn_index < len(self.history) - 1:
                if self.pause:
                    if pygame.time.get_ticks() - self.pause_start > 1000:
                        self.pause = False
                else:
                    self.progress += 0.01
                    if self.progress >= 0.99:
                        self.pause = True
                        self.pause_start = pygame.time.get_ticks()
                        self.progress = 0
                        self.turn_index += 1
            alien = self.aliens[self.current_alien]
            start = alien["start"]
            end = alien["end"]
            self.progress_for_animation += 0.004
            if self.progress_for_animation >= 1.0:
                self.progress_for_animation = 0.0
                self.current_alien = (self.current_alien + 1) % len(self.aliens)
                alien = self.aliens[self.current_alien]
                start = alien["start"]
                end = alien["end"]

            x = start[0] + (end[0] - start[0]) * self.progress_for_animation
            y = start[1] + (end[1] - start[1]) * self.progress_for_animation
            self.screen.blit(self.alien_surface, (x, y))
            pygame.display.update()
            clock.tick(60)

    def _grid_offset(
        self, drone_id: int, per_row: int = 4, spacing: int = 10
    ) -> tuple[float, float]:
        index = drone_id - 1
        row = index // per_row
        col = index % per_row
        x_off = (col - (per_row - 1) / 2) * spacing
        y_off = row * spacing
        return x_off, y_off

    def zones_positions(self, current_window_w, current_window_h, margin=50) -> dict:
        zones = list(self.graph.zones.values())
        if not zones:
            return {}

        xs = [z.x for z in zones]
        ys = [z.y for z in zones]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        

        span_x = max(max_x - min_x, 1)
        span_y = max(max_y - min_y, 1)
        usable_w = current_window_w - (2 * margin)
        usable_h = current_window_h - (2 * margin)
        scale = min(usable_w / span_x, usable_h / span_y)

        positions = {}
        for z in zones:
            px = (z.x - min_x) * scale
            py = (z.y - min_y) * scale
            positions[z.name] = (px, py)

        graph_width = span_x * scale
        graph_height = span_y * scale
        offset_x = (current_window_w - graph_width) / 2
        offset_y = (current_window_h - graph_height) / 2
        for name, (px, py) in positions.items():
            positions[name] = (px + offset_x, py + offset_y)

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
            pygame.draw.line(
                self.screen,
                (200, 200, 200),
                self.positions[name1],
                self.positions[name2],
                2,
            )

    def _draw_zones(self):
            radius = 32  
            my_font = pygame.font.Font(None, 19) 
            line_spacing = 2

            for name, pos in self.positions.items():
                zone_type = self._zone_type_of(name)
                text_color = (255, 255, 255) if zone_type == "blocked" else (0, 0, 0)
                part1, part2 = name, ""
                
                for delim in ['_', ' ', '-']:
                    if delim in name:
                        parts = name.split(delim)
                        mid = max(1, len(parts) // 2)
                        part1 = delim.join(parts[:mid])
                        part2 = delim.join(parts[mid:])
                        break
                else:
                    if len(name) > 7:
                        mid = len(name) // 2
                        part1 = name[:mid] + "-"
                        part2 = name[mid:]
                surface1 = my_font.render(part1, True, text_color)
                w1, h1 = surface1.get_width(), surface1.get_height()
                
                if part2:
                    surface2 = my_font.render(part2, True, text_color)
                    w2, h2 = surface2.get_width(), surface2.get_height()
                    total_h = h1 + h2 + line_spacing
                else:
                    surface2 = None
                    w2, h2 = 0, 0
                    total_h = h1

                if zone_type == "blocked":
                    scaled_blocked = pygame.transform.scale(self.blocked_zone, (radius * 2, radius * 2))
                    self.screen.blit(scaled_blocked, (pos[0] - radius, pos[1] - radius))
                else:
                    color = ZONE_COLOR.get(zone_type, ZONE_COLOR["normal"])
                    pygame.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), radius)

                start_y = pos[1] - total_h / 2
            
                text1_x = pos[0] - w1 / 2
                self.screen.blit(surface1, (text1_x, start_y))
            
                if surface2:
                    text2_x = pos[0] - w2 / 2
                    self.screen.blit(surface2, (text2_x, start_y + h1 + line_spacing))

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
            self.screen.blit(self.station_zone, (station_x - 35, station_y - 35))

    def _get_station_pos(self, zone1: str, zone2: str) -> tuple[float, float]:
        if (zone1, zone2) in self.stations:
            return self.stations[(zone1, zone2)]
        return self.stations[(zone2, zone1)]

    def _draw_drones(self):
        if self.turn_index >= len(self.history) - 1:
            return
            
        frame_from = self.history[self.turn_index]
        frame_to = self.history[self.turn_index + 1]
        path_groups = {}
        drone_path_keys = {}
        
        for drone_id, to_zone in frame_to.items():
            from_zone = frame_from.get(drone_id)
            if from_zone is None:
                continue
            
            path_key = (from_zone, to_zone)
            if path_key not in path_groups:
                path_groups[path_key] = []
            path_groups[path_key].append(drone_id)
            drone_path_keys[drone_id] = path_key
        for drone_id, to_zone in frame_to.items():
            from_zone = frame_from.get(drone_id)
            if from_zone is None:
                continue
                
            path_key = drone_path_keys.get(drone_id)
            if not path_key:
                continue
                
            shared_drones = path_groups[path_key]
            local_index = shared_drones.index(drone_id)
            total_on_path = len(shared_drones)

            if (from_zone in self.positions 
                and isinstance(to_zone, str) 
                and to_zone.startswith("moving_waiting_")):
                
                real_zone = to_zone.replace("moving_waiting_", "")
                self.transit_origin[drone_id] = from_zone

                if from_zone not in self.positions or real_zone not in self.positions:
                    continue

                station_x, station_y = self._get_station_pos(from_zone, real_zone)
                start_pos = self.positions[from_zone] 
                x = start_pos[0] + (station_x - start_pos[0]) * self.progress
                y = start_pos[1] + (station_y - start_pos[1]) * self.progress
                dx = station_x - start_pos[0]
                dy = station_y - start_pos[1]

                dist = (dx**2 + dy**2)**0.5
                if dist > 0:
                    nx, ny = -dy / dist, dx / dist
                    lane_offset = (local_index - (total_on_path - 1) / 2) * 14
                    x += nx * lane_offset
                    y += ny * lane_offset

                self.screen.blit(self.alien_drone, (x - 25, y - 25))
                continue

            if (isinstance(from_zone, str) 
                and from_zone.startswith("moving_waiting_") 
                and isinstance(to_zone, str) 
                and to_zone.startswith("waiting_")
                and to_zone not in self.positions):
                
                real_zone = to_zone.replace("waiting_", "")
                origin_zone = self.transit_origin.get(drone_id)
                if origin_zone is None:
                    continue
                    
                x, y = self._get_station_pos(origin_zone, real_zone)
                
                row = local_index // 3
                col = local_index % 3
                x_off = (col - 1) * 12
                y_off = (row - 0.5) * 12
                
                self.screen.blit(self.alien_drone, (x - 25 + x_off, y - 25 + y_off))
                continue

            if (isinstance(from_zone, str) 
                and from_zone.startswith("waiting_") 
                and from_zone not in self.positions):
                
                origin_zone = self.transit_origin.get(drone_id)
                if origin_zone is None or to_zone not in self.positions:
                    continue
                    
                station_x, station_y = self._get_station_pos(origin_zone, to_zone)
                end_pos = self.positions[to_zone]
                
                x = station_x + (end_pos[0] - station_x) * self.progress
                y = station_y + (end_pos[1] - station_y) * self.progress
                dx = end_pos[0] - station_x
                dy = end_pos[1] - station_y
                dist = (dx**2 + dy**2)**0.5
                if dist > 0:
                    nx, ny = -dy / dist, dx / dist
                    lane_offset = (local_index - (total_on_path - 1) / 2) * 14
                    x += nx * lane_offset
                    y += ny * lane_offset

                self.screen.blit(self.alien_drone, (x - 25, y - 25))
                continue

            if from_zone not in self.positions or to_zone not in self.positions:
                continue

            start_pos = self.positions[from_zone]
            end_pos = self.positions[to_zone]
            
            x = start_pos[0] + (end_pos[0] - start_pos[0]) * self.progress
            y = start_pos[1] + (end_pos[1] - start_pos[1]) * self.progress
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                nx, ny = -dy / dist, dx / dist
                lane_offset = (local_index - (total_on_path - 1) / 2) * 14
                x += nx * lane_offset
                y += ny * lane_offset

            self.screen.blit(self.alien_drone, (x - 25, y - 25))
def main():
    filepath = "map/my_maps.txt"
    parser = Parser()
    graph = parser.parse(filepath)
    simulation = Simulation(graph)
    simulation.give_me_all_paths()
    data = simulation.run()
    vis = visualisation(simulation.graph, data)
main()
