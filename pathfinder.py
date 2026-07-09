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
    def find_all_paths(self) ->list[list]:
        all_paths: list[list] = []

        queue = deque([[self.graph.start]])
        try:
            while queue:
                path = queue.popleft()
                current = path[-1]
    
                if current == self.graph.end:
                    all_paths.append(path)
                for neighbor in self.graph.get_neighbors(current):
                    if neighbor.zone_type != "blocked" and neighbor not in path:
                        queue.append(path + [neighbor])
            return all_paths
        except Exception as e:
            print(e)
def main():
    filepath = "map/my_maps.txt"
    parser = Parser()
    graph = parser.parse(filepath)
    pathfinder = Pathfinder(graph)
    paths = pathfinder.find_all_paths()
    

    # for path in paths:
    #     print([zone.name for zone in path])

main()