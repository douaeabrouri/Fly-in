from models import Graph, Zone, Connection
from collections import deque
from parsing import Parser
import queue

class Pathfinder:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
    
    def find_path(self) -> list[Zone]:
        try:
            queue = deque([[self.graph.start]])
            # current = self.graph.start
            visited = {self.graph.start.name}
            while queue:
                path = queue.popleft()
                # print(f"path: {path}")
                current = path[-1]
                # print(f"visiting: {current.name}")
    
                if current == self.graph.end:
                    return path
                
                for neighbor in self.graph.get_neighbors(current):
                    # print(f"neighbor: {neighbor.name}")
                    if neighbor.name not in visited and neighbor.zone_type != "blocked":
                       visited.add(neighbor.name)
                       queue.append(path + [neighbor])
                # print(f"visited: {visited}")
            return []
        except Exception as e:
            print(f"Found an error: {e}")
    def find_all_paths(self):
        pass
def main():
    filepath = "map/my_maps.txt"

    parser = Parser()
    graph = parser.parse(filepath)
    pathfinder = Pathfinder(graph)
    path = pathfinder.find_path()
    for zone in path:
        print(zone.name)

main()