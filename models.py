
class Zone:
    def __init__(self, name: str, x: int, y :int, zone_type: str, color: str,max_drones: int) -> None:
        self.name = name 
        self.x = x
        self.y = y
        self.color = color
        self.zone_type = zone_type
        self.max_drones = max_drones
        self.inside_zone: int = 0
        self.incoming_drones: int = 0
    
class Connection:
    def __init__(self, zone_a: Zone, zone_b: Zone, max_link_capacity: int) -> None:
       self.zone_a = zone_a
       self.zone_b = zone_b
       self.max_link_capacity = max_link_capacity
  
class Graph:
    def __init__(self) -> None:
       self.zones: dict[str, Zone] = {}
       self.connections: list[Connection] = []
       self.start: Zone | None = None
       self.end: Zone | None = None
       self.nb_drones: int = 0

    def add_zone(self, zone: Zone) -> None:
        self.zones[zone.name] = zone
    
    def add_connection(self, connection: Connection) -> None:
        self.connections.append(connection)
    
    def get_zone(self, name: str) -> Zone | None:
        return self.zones.get(name)

    def get_neighbors(self, zone: Zone) -> list[Zone]:
        neighbors: list[Zone] = []
        for con in self.connections:
            if con.zone_a == zone:
                neighbors.append(con.zone_b)
            if con.zone_b == zone:
                neighbors.append(con.zone_a)
        return neighbors

class Drone:
    def __init__(self, drone_id: int, start: Zone) -> None:
        self.drone_id = drone_id 
        self.path: list[Zone] = []
        self.path_index: int = 0
        self.current_zone = start
        self.delivered: bool = False
        self.doing_turns: int = 0
        self.destination_zone: Zone | None = None
        self.waiting_for: Zone | None = None

