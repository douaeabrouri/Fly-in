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
            if drone.path_index >= len(drone.path) - 1:
                continue
            if drone.doing_turns > 0:
                drone.doing_turns -= 1
                if drone.doing_turns == 0:
                    drone.current_zone = drone.destination_zone
                    drone.path_index += 1
                    drone.destination_zone = None
                continue
            next_zone = drone.path[drone.path_index + 1]
                
            if next_zone.zone_type == "restricted":
                drone.destination_zone = next_zone
                drone.doing_turns = 1
            else:
                drone.current_zone = next_zone
                drone.path_index += 1
                if drone.current_zone == self.graph.end:
                    drone.delivered = True
            # print(
            #     drone.drone_id,
            #     drone.path_index,
            #     drone.current_zone.name,
            #     drone.doing_turns
            # )
            print(f"D_i: {drone.drone_id} - PI: {drone.path_index} - zone name: {drone.current_zone.name} - turns: {drone.doing_turns}")
            # print(f"PI: {drone.path_index}")
            # print(f"zone name: {drone.current_zone.name}")
            # print(f"turns: {drone.doing_turns}")
                    
      
    def all_delivered(self) -> bool:
        return all(drone.delivered for drone in self.drones)

    def run(self) -> None:
        drone_informations: list[str]  = []
        while not self.all_delivered():
            self.turn += 1
            self.step_to_goal()
            # for drone in self.drones:
            #     drone_informations.append(f"D{drone.drone_id}-{drone.current_zone.name}")
            if self.turn > 15:
                break
        for info in drone_informations:
            print(info)


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