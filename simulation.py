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
        
        try:
            pathfinder = Pathfinder(self.graph)
            paths = pathfinder.find_all_paths()
            path_usage = [0] * len(paths)
            for i in range(self.graph.nb_drones):
                drone = Drone(drone_id = i + 1, start = self.graph.start)
                best_idx = min(range(len(paths)), key=lambda idx: path_usage[idx])

                drone.path = paths[best_idx]
                path_usage[best_idx] += 1
                self.drones.append(drone)
            self.graph.start.inside_zone = self.graph.nb_drones
        except Exception as e:
            print(f"ERROR: {e}")

    def step_to_goal(self) -> None:
        
        for drone in self.drones:
            if drone.delivered:
                continue
            if drone.path_index >= len(drone.path) - 1:
                continue


            if drone.doing_turns > 0:
                drone.doing_turns -= 1
                if drone.doing_turns == 0:
                    old_zone = drone.current_zone 
                    old_zone.inside_zone -= 1
                    drone.destination_zone.inside_zone += 1
                    drone.destination_zone.incoming_drones -= 1
                    drone.current_zone = drone.destination_zone
                    drone.path_index += 1
                    # movements.append(
                    #     f"D{drone.drone_id}-{drone.current_zone.name}"
                    # )
                    drone.destination_zone = None
                continue

            next_zone = drone.path[drone.path_index + 1]

            if next_zone not in (self.graph.start, self.graph.end):
                if (next_zone.inside_zone + next_zone.incoming_drones) >= next_zone.max_drones:        
                   continue

            if next_zone.zone_type == "restricted" :
                drone.destination_zone = next_zone
                drone.waiting_for = next_zone.name
                drone.doing_turns = 1
                next_zone.incoming_drones += 1
                continue
    
            old_zone = drone.current_zone
            old_zone.inside_zone -= 1
            # next_zone.incoming_drones += 1
            next_zone.inside_zone += 1
            drone.current_zone = next_zone
            drone.path_index += 1

            # movements.append(
            #     f"D{drone.drone_id}-{drone.current_zone.name}"
            # )

            if drone.current_zone == self.graph.end:
                drone.delivered = True


    def all_delivered(self) -> bool:
        return all(drone.delivered for drone in self.drones)

    def run(self) -> list:

        self.data = []
        # self.data.append(
        #     {d.drone_id: d.current_zone.name for d in self.drones}
        # )
        while True:
            frame = {}
            for d in self.drones:
                if d.doing_turns > 2 and d.destination_zone:
                    frame[d.drone_id] = (f"moving_waiting_{d.destination_zone.name}")
                elif d.doing_turns == 1 and d.destination_zone:
                    frame[d.drone_id] =  (f"waiting_{d.destination_zone.name}")
                else:
                    frame[d.drone_id] = d.current_zone.name
            self.data.append(frame)
            if self.all_delivered():
                break

            self.turn += 1
            self.step_to_goal()
            # movements = []
            # if movements:
            #     move = " ".join(movements)
            #     print(f"Turn {self.turn} -> {move}")
            # return movements

        return self.data
def main():
    filepath = "map/my_maps.txt"
    parser = Parser()
    graph = parser.parse(filepath)
    simulation = Simulation(graph)
    simulation.give_me_all_paths()
    data = simulation.run()
    for turn, frame in enumerate(data):
        print(f"turn {turn}: {frame}")
main()