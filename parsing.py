
from models import Zone, Connection, Graph
import sys

class Parser:

    def _help_to_parse_hub(self, content: str) -> Zone:
        try:
            if '[' in content:
                main_part, meta_part = content.split('[', 1)
                meta_part = meta_part.rstrip(']')
            else:
                main_part = content
                meta_part = ""
                
            part = main_part.strip().split()
            name: str = part[0]
            x: int = int(part[1])
            y: int = int(part[2])

            zone_type: str = "normal"
            color: str = ""
            max_drones: int = 1
            for data in meta_part.split():
                if data.startswith("zone="):
                    zone_type = data.split("=")[1]
                elif data.startswith("color="):
                    color = data.split("=")[1]
                elif data.startswith("max_drones="):
                    max_drones = int(data.split("=")[1])
                
            zone = Zone(name=name, x=x, y=y,
                        zone_type=zone_type,
                        color=color,
                        max_drones=max_drones)
            return zone
        except Exception as e:
            print(f"Warning: {e}")
    def parse(self, filepath: str) -> Graph:
        try:
            graph = Graph()
            with open(filepath, 'r') as file:
                for line_num, line in enumerate(file, start=1):
                    line = line.strip()
                    if line.startswith('#') or line == "":
                        continue

                    elif line.startswith("nb_drones"):
                        try:
                            drone_numb: int = 0
                            drone_numb = int(line.removeprefix("nb_drones:").strip())
                            if drone_numb <= 0:
                                raise ValueError("The number of drones must be positive!")
                            graph.nb_drones = drone_numb
                        except ValueError:
                            raise ValueError(f"The line {line_num}: invalid drone numbers values")

                    elif line.startswith("start_hub"):
                        content = str(line.removeprefix("start_hub:")).strip()
                        zone = self._help_to_parse_hub(content)
                        graph.add_zone(zone)
                        graph.start = zone

                    elif line.startswith("end_hub"):
                        content = str(line.removeprefix("end_hub:")).strip()
                        zone = self._help_to_parse_hub(content)
                        graph.add_zone(zone)
                        graph.end = zone


                    elif line.startswith("hub"):
                        content = str(line.removeprefix("hub:")).strip()
                        zone = self._help_to_parse_hub(content)
                        graph.add_zone(zone)

                    elif line.startswith("connection"):
                        try:
                            content = str(line.removeprefix("connection:")).strip()
                            if '[' in content:
                                main_part, meta_part = content.split('[', 1)
                                meta_part = meta_part.rstrip(']')
                            else:
                                main_part = content
                                meta_part = ""
                            names: list = main_part.strip().split('-')
                            if len(names) != 2:
                                raise ValueError("the numbers of names must be 2")
                            name1: str = names[0].strip()
                            name2: str = names[1].strip()
                            max_link_capacity: int = 1
                            for data in meta_part.split():
                                if data.startswith("max_link_capacity="):
                                    max_link_capacity = int(data.split("=")[1])
                                    if max_link_capacity <= 2:
                                        raise ValueError("Capacity must be positive")
                            zone_a = graph.get_zone(name1)
                            zone_b = graph.get_zone(name2)
                            connection = Connection(zone_a, zone_b, max_link_capacity)
                            graph.add_connection(connection)
                        except Exception as e:
                                print(f"error: {e}")
        except Exception as e:
            print(f"Error on line {line_num}: {e}")
            sys.exit(1)
        return graph