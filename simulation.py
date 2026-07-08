from models import Graph, Zone, Connection, Drone
from pathfinder import Pathfinder
from parsing import Parser
from typing import List

class Simulation:
    def __init__(self,graph: Graph) -> None:
        self.graph = graph
        self.drones: list[Drone] = []
        self.turn: int = 0
    
    def give_me_all_paths(self) -> None:
        pathfinder = Pathfinder(self.graph)
        paths = pathfinder.find_all_paths()
        for i in range(self.graph.nb_drones):
            drone = Drone(drone_id = i + 1, start = self.graph.start)
            drone.path = paths[i % len(paths)]
            self.drones.append(drone)
        for drone in self.drones:
            print(f"D{drone.drone_id} -> {[z.name for z in drone.path]}")

    def can_i(self) -> bool:
        if self.inside_zone >= self.max_drones:
            return False
        return True
    
    def leave(self) -> None:
        self.inside_zone -= 1

    def enter(self) -> None:
        self.inside_zone += 1

    def step_to_goal(self) -> None:
        for drone in self.drones:
            if drone.delivered:
                continue
            next_zone = drone.path[drone.path_index]
            if next_zone.zone_type == "blocked":
                continue
            elif next_zone.zone_type == "restricted":
                pass
            else:
                drone.current_zone = next_zone
                drone.path_index += 1
                if drone.current_zone == self.graph.end:
                    drone.delivered = True            
    def all_delivered(self) -> bool:
        return all(drone.delivered for drone in self.drones)

    def run(self) -> None:
        drone_informations: list[str]  = []
        while not self.all_delivered():
            self.turn += 1
            self.step_to_goal()
            for drone in self.drones:
                drone_informations.append(f"D{drone.drone_id}-{drone.current_zone.name}")
        print(f"turns : {self.turn}  drone info: {drone_informations}")


def main():
    filepath = "map/my_maps.txt"
    parser = Parser()
    graph = parser.parse(filepath)
    simulation = Simulation(graph)
    # simulation.give_me_all_paths()
    simulation.give_me_all_paths()
    # simulation.all_delivered()
    simulation.run()
    # simulation.step_to_goal()
main()