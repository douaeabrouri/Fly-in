from models import Zone, Connection, Graph

def _help_to_parse_hub(content: str) -> Zone:
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
                max_drones = data.split("=")[1]
            
        zone = Zone(name=name, x=x, y=y,
                    zone_type=zone_type,
                    color=color,
                    max_drones=max_drones)
        return Zone
    except Exception as e:
        print(f"Warning: {e}")

class Parser:


    def parse(filepath: str) -> Graph:
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
                        except ValueError:
                            raise ValueError(f"The line {line_num}: invalid drone numbers values")

                    elif line.startswith("start_hub"):
                        content = str(line.removeprefix("start_hub:")).strip()
                        # zone = self._help_to_parse_hub(content)

                    elif line.startswith("end_hub"):
                        content = str(line.removeprefix("end_hub:")).strip()
                        # zone = self._help_to_parse_hub(content)

                    elif line.startswith("hub"):
                        content = str(line.removeprefix("hub:")).strip()
                        # zone = self._help_to_parse_hub(content)

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
                                if data.startswith("max_lint_capacity="):
                                    max_link_capacity = data.split("=")[1]
                                    if max_link_capacity <= 2:
                                        raise ValueError("Capacity must be positive")

                        except Exception as e:
                            pass

                       
                    
        except Exception as e:
            pass

def main():
    filepath = "map/my_maps.txt"
    ob = Parser.parse(filepath)
main()