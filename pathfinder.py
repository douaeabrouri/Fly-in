from models import Graph, Zone, Connection
from collections import deque
from parsing import Parser
import queue

class pathfinder:
    def __init__(self, graph: Graph) -> None:
        self.graph = graph
    
    def find_path(self) -> list[Zone]:
        try:
            queue = deque([[self.graph.start]])
            # current = self.graph.start
            visited = {self.graph.start.name}
            while queue:
                path = queue.popleft()
                current = path[-1]
    
                if current == self.graph.end:
                    return path
                for neighbor in self.graph.get_neighbors(current):
                    if neighbor.name not in visited and neighbor.zone_type != "blocked":
                       visited.add(neighbor.name)
                       queue.append(path + [neighbor])
            return []        
        except Exception as e:
            print(f"Found an error: {e}")
    def find_all_paths(self):
        pass
def main():
    test = pathfinder()
    print(test.find_path())
main()