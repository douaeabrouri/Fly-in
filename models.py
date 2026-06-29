
class Zone:
    def __init__(self, name: str, x: int, y :int, zone_type: str, color: str,max_drones: int) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.color: color
        self.zone_type = zone_type
        self.max_drones = max_drones
    
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
                neighbors.append(con.zone_a)
            if con.zone_b == zone:
                neighbors.append(con.zone_b)
        return neighbors


    