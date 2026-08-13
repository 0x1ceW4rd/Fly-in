from parser import Parser, ZoneTypes, Graph
from argparse import ArgumentParser, Namespace
from typing import List
import heapq


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
        argparser.add_argument("--map",
                            default="maps/easy/01_linear_path.txt")
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