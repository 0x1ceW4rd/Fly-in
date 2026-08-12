from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from enum import Enum

class ZoneTypes(Enum):
    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"

class Zone(BaseModel):
    name: str
    coords: tuple[int, int]
    max_drones: int = 1
    color: Optional[str] = None
    zone_type: ZoneTypes = ZoneTypes.NORMAL
    connections: Optional[Dict[str, Any]] = None

class Graph:
    def __init__(self, np_drones, zones):
        self.np_drones = np_drones
        self.zones: List[Zone]= zones

class Parser:
    def __init__(self, map):
        self.map = map


    def hub_data_extractor(self, line: str):
        alldata = list()

        splited = line.split()
        
        zname = splited[1]
        zcoords = tuple((splited[2], splited[3]))

        alldata.append(zname)
        alldata.append(zcoords)

        start = line.find('[')
        end = line.find(']')

        zdata = line[start+1: end]
        
        for data in zdata.split():
            if "color" in data:
                zcolor = data.split('=')[1]
                alldata.append(zcolor)

            elif "max_drones" in data:
                zmax_drones = int(data.split('=')[1])
                if zmax_drones < 0:
                    raise(ValueError("max drones cant be negative"))
                else:
                    alldata.append(zmax_drones)

            elif "zone_type" in data:
                zzone_type = data.split('=')[1]
                if zzone_type == "normal":
                    zzone_type = ZoneTypes.NORMAL
                    alldata.append(zzone_type)
                elif zzone_type == "restricted":
                    zzone_type = ZoneTypes.RESTRICTED
                    alldata.append(zzone_type)
                elif zzone_type == "priority":
                    zzone_type = ZoneTypes.PRIORITY
                    alldata.append(zzone_type)
                elif zzone_type == "blocked":
                    zzone_type = ZoneTypes.BLOCKED
                    alldata.append(zzone_type)
                else:
                    raise(ValueError("Zone type provided is wrong"))
                
            else:
                raise(ValueError(f"'{data}'is not a valid metadata for this project"))

        return(alldata)
    

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
                        # print(firstline)
                        break

                if "nb_drones" not in firstline:
                    raise(ValueError("The first line must define the number of drones using 'nb_drones: <positive_integer>'"))
                elif '-' in firstline:
                    raise(ValueError("The number of drones must be a positive integer"))
                else:
                    np_drones = int(line.split(' ')[1])

                zones = list()
                for line in map:
                    if line.startswith('#'):
                        continue
                    if line.startswith('\n'):
                        continue
                    if line.startswith('connection'):
                        continue

                    # extratcting zone's data
                    zdata = self.hub_data_extractor(line)

                    print(zdata)

                
        except Exception as e:
            print(e)