from parser import Parser, ZoneTypes, Graph, Zone
from argparse import ArgumentParser, Namespace
from typing import List, Dict
import heapq


class Drone:
    def __init__(self, id, path):
        self.id: int = id
        self.path = path 

from typing import Dict, List, Tuple

class ReservationTable:
    def __init__(self, graph: Graph):
        self.graph = graph
        # zone_name -> {turn: drone_count}
        self.zones: Dict[str, Dict[int, int]] = {}
        # (from_zone_name, to_zone_name) -> {turn: drone_count}
        self.links: Dict[Tuple[str, str], Dict[int, int]] = {}

    def ismax_drones(self, zone: Zone, turn: int) -> bool:
        if zone.name == self.graph.start_hub.name or zone.name == self.graph.end_hub.name:
            return True
        
        numofdrones = self.zones.get(zone.name, {}).get(turn, 0)
        return numofdrones < zone.max_drones

    def ismax_link_capacity(self, from_zone: Zone, to_zone: Zone, turn: int) -> bool:
        link_key = (from_zone.name, to_zone.name)
        numofdrones = self.links.get(link_key, {}).get(turn, 0)
        max_capacity = from_zone.connections[to_zone.name]
        
        return numofdrones < max_capacity

    def book_path(self, path: List[str]) -> None:
        current_turn = 0
        
        for i in range(len(path) - 1):
            from_name = path[i]
            to_name = path[i + 1]
            
            if from_name == to_name:
                current_turn += 1
                if to_name not in self.zones:
                    self.zones[to_name] = {}
                self.zones[to_name][current_turn] = self.zones[to_name].get(current_turn, 0) + 1
                continue

            link_key = (from_name, to_name)
            entry_turn = current_turn + 1
            
            if link_key not in self.links:
                self.links[link_key] = {}
            self.links[link_key][entry_turn] = self.links[link_key].get(entry_turn, 0) + 1
            
            to_zone = self.graph.zones[to_name]
            duration = 2 if to_zone.zone_type == ZoneTypes.RESTRICTED else 1
            
            if to_name not in self.zones:
                self.zones[to_name] = {}
                
            for t in range(1, duration + 1):
                occupied_turn = current_turn + t
                self.zones[to_name][occupied_turn] = self.zones[to_name].get(occupied_turn, 0) + 1
                
            current_turn += duration


class Pathfinder:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.zone_value = {ZoneTypes.NORMAL: 1,
                           ZoneTypes.RESTRICTED: 2,
                           ZoneTypes.PRIORITY: 1,
                           ZoneTypes.BLOCKED: float('inf')}

    def the_algo(self) -> List[str]:
        graph = self.graph

        p_queue = [(0, 0, graph.start_hub.name, [graph.start_hub.name])]
        heapq.heapify(p_queue)

        d_tracker = {graph.start_hub.name: (0, 0)}

        while p_queue:
            curr = heapq.heappop(p_queue)
            curr_cost, curr_priority_count, curr_zone_name, curr_path = curr

            if curr_zone_name == graph.end_hub.name:
                return curr_path

            curr_state = (curr_cost, curr_priority_count)
            if d_tracker[curr_zone_name] < curr_state:
                continue
            else:
                d_tracker[curr_zone_name] = curr_state
            
            for neighbor in graph.zones[curr_zone_name].connections:

                neighbor_zone = graph.zones[neighbor]
                if neighbor_zone.zone_type == ZoneTypes.BLOCKED:
                    continue

                is_priority = 1 if neighbor_zone.zone_type == ZoneTypes.PRIORITY else 0
                new_priority_count = curr_priority_count - is_priority
                new_cost = curr_cost + self.zone_value[neighbor_zone.zone_type]

                n_state = (new_cost, new_priority_count)
                old_state = d_tracker.get(neighbor_zone.name, (float('inf'), 0))

                if n_state < old_state:
                    d_tracker[neighbor_zone.name] = n_state 
                    new_path = curr_path + [neighbor_zone.name]
                    heapq.heappush(p_queue, (new_cost, new_priority_count, neighbor_zone.name, new_path))
        
        raise ValueError("No valid path exists between start and end zones")


 

def main() -> None:
    try:
        argparser: ArgumentParser = ArgumentParser()
        argparser.add_argument("--map", default="maper.txt")
        args: Namespace = argparser.parse_args()

        map = args.map
        parser = Parser(map)
        graph = parser.maping()

        p = Pathfinder(graph)

        print(p.the_algo())
        

    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()