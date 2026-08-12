from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum

class ZoneTypes(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"

class Zone(BaseModel):
    name: str
    coords: tuple[int, int]
    max_drones: int 
    color: Optional[str]
    zone_type: ZoneTypes
    connections: Optional[Dict[str, Any]] = Field(default_factory=dict)

    def __repr__(self) -> str:
        connected_zones = list(self.connections.keys()) if self.connections else []
        
        return (
            f"Zone('{self.name}', type={self.zone_type.value}, "
            f"max_drones={self.max_drones}, links={connected_zones})"
        )

class Graph:
    def __init__(self, np_drones):
        self.np_drones = np_drones
        self.start_hub: Zone
        self.zones: Dict[str, Zone] = dict()
        self.end_hub: Zone

    def __repr__(self) -> str:
        return (
            f"Graph(drones={self.np_drones}, "
            f"total_zones={len(self.zones)}, "
            f"start='{self.start_hub.name}', "
            f"end='{self.end_hub.name}')"
        )
    
class Parser:
    def __init__(self, map):
        self.map = map
        self.start_points = 0
        self.end_points = 0

    def hub_data_extractor(self, line: str, the_graph: Graph) -> Dict[str, Zone]:
        splited = line.split()
        if "start_hub:" in splited[0]:
            self.start_points += 1
        

        if "end_hub:" in splited[0]:
            self.end_points += 1
        
        
        zname = splited[1]
        if '-' in zname:
            raise(ValueError("Zone name cant have '-' in it"))
        
        zcoords = tuple((int(splited[2]), int(splited[3])))
        zmax_drones = 1
        zcolor = None
        zzone_type = ZoneTypes.NORMAL

        if '[' in line:
            start = line.find('[')
            end = line.find(']')
            zdata = line[start+1: end]

            for data in zdata.split():
                if "color" in data:
                    zcolor = data.split('=')[1]

                elif "max_drones" in data:
                    zmax_drones = int(data.split('=')[1])
                    if zmax_drones < 0:
                        raise(ValueError("max drones cant be negative"))

                elif "zone" in data:
                    zzone_type = data.split('=')[1]
                    if zzone_type == "normal":
                        zzone_type = ZoneTypes.NORMAL

                    elif zzone_type == "restricted":
                        zzone_type = ZoneTypes.RESTRICTED

                    elif zzone_type == "priority":
                        zzone_type = ZoneTypes.PRIORITY

                    elif zzone_type == "blocked":
                        zzone_type = ZoneTypes.BLOCKED

                    else:
                        raise(ValueError("Zone type provided is wrong"))

                else:
                    raise(ValueError(f"'{data}'is not a valid metadata for this zone({zname})"))

        if line.startswith("start_hub"):
            start_hub=Zone(name=zname, coords=zcoords,
                                     max_drones=zmax_drones, color=zcolor,
                                     zone_type=zzone_type)
            the_graph.start_hub=start_hub
            return({zname: start_hub})

        if line.startswith("end_hub"):
            end_hub=Zone(name=zname, coords=zcoords,
                                     max_drones=zmax_drones, color=zcolor,
                                     zone_type=zzone_type)
            the_graph.end_hub=end_hub
            return({zname: end_hub})

        return({zname: Zone(name=zname, coords=zcoords,
                    max_drones=zmax_drones, color=zcolor,
                    zone_type=zzone_type)})
    

    def conector(self, line: str, the_graph: Graph) -> None:
        trajet = line.split()[1].split('-')

        from_zone = trajet[0]
        to_zone = trajet[1]

        zmax_link_capacity = 1
        if '[' in line:
                    start = line.find('[')
                    end = line.find(']')
                    zdata = line[start+1: end]
        
                    for data in zdata.split():
                        if "max_link_capacity" in data:
                            zmax_link_capacity = int(data.split('=')[1])
                        else:
                            raise(ValueError(f"'{data}'is not a valid metadata for this connection"))

        if zmax_link_capacity <= 0:
            raise ValueError("max_link_capacity must be a positive integer bigger than 0")
        if from_zone not in the_graph.zones or to_zone not in the_graph.zones:
            raise ValueError(f"Connection references unknown zone: {from_zone}-{to_zone}")
        if to_zone in the_graph.zones[from_zone].connections:
            raise ValueError(f"Duplicate connection found between '{from_zone}' and '{to_zone}'")
        the_graph.zones[from_zone].connections[to_zone] = zmax_link_capacity
        the_graph.zones[to_zone].connections[from_zone] = zmax_link_capacity

        

    def maping(self):
        try:
            with open(self.map, "r") as map:
                for line in map:
                    if line.startswith('#'):
                        continue
                    if line.startswith('\n'):
                        continue
                    else:
                        firstline = line
                        break

                if "nb_drones" not in firstline:
                    raise(ValueError("The first line must define the number of drones using 'nb_drones: <positive_integer>'"))
                elif '-' in firstline:
                    raise(ValueError("The number of drones must be a positive integer"))
                else:
                    np_drones = int(line.split()[1])

                the_graph = Graph(np_drones)
                for line in map:
                    if line.startswith('#'):
                        continue
                    if line.startswith('\n'):
                        continue
                    

                    # extratcting zone's data
                    
                    if line.startswith(("start_hub", "hub", "end_hub")):
                        the_graph.zones.update(self.hub_data_extractor(line, the_graph))
                    elif line.startswith("connection"):
                        self.conector(line, the_graph)
                
                if self.start_points != 1:
                    raise(ValueError("It must be max one start point"))
                if self.end_points != 1:
                    raise(ValueError("It must be max of one end point"))    

                return the_graph

                
        except Exception as e:
            print(e)