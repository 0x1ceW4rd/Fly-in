from parser import Parser, ZoneTypes, Graph, Zone
from argparse import ArgumentParser, Namespace
from typing import List, Dict, Tuple
from visual import Visualizer
import heapq


class ReservationTable:
    def __init__(self, graph: Graph):
        self.graph = graph
        # zone_name -> {turn: drone_count}
        self.zones: Dict[str, Dict[int, int]] = {}
        # (from_zone_name, to_zone_name) -> {turn: drone_count}
        self.links: Dict[Tuple[str, str], Dict[int, int]] = {}

    def ismax_drones(self, zone: Zone, turn: int) -> bool:
        if (
            zone.name == self.graph.start_hub.name
            or zone.name == self.graph.end_hub.name
        ):
            return True

        numofdrones = self.zones.get(zone.name, {}).get(turn, 0)
        return numofdrones < zone.max_drones

    def ismax_link_capacity(self, from_zone: Zone,
                            to_zone: Zone, turn: int) -> bool:
        link_key = (from_zone.name, to_zone.name)
        numofdrones = self.links.get(link_key, {}).get(turn, 0)
        max_capacity = from_zone.connections[to_zone.name]

        return bool(numofdrones < max_capacity)

    def book_path(self, path: List[str]) -> None:
        current_turn = 0

        for i in range(len(path) - 1):
            from_name = path[i]
            to_name = path[i + 1]
            current_turn += 1

            if from_name != to_name:
                link_key = (from_name, to_name)
                if link_key not in self.links:
                    self.links[link_key] = {}
                self.links[link_key][current_turn] = (
                    self.links[link_key].get(current_turn, 0) + 1
                )

            if to_name not in self.zones:
                self.zones[to_name] = {}
            self.zones[to_name][current_turn] = (
                self.zones[to_name].get(current_turn, 0) + 1
            )


class Pathfinder:
    def __init__(self, graph: Graph, res_table: ReservationTable):
        self.graph = graph
        self.zone_value = {
            ZoneTypes.NORMAL: 1,
            ZoneTypes.RESTRICTED: 2,
            ZoneTypes.PRIORITY: 1,
            ZoneTypes.BLOCKED: float("inf"),
        }
        self.res_table = res_table

    def the_algo(self) -> List[str]:
        graph = self.graph
        sta = graph.start_hub.name
        p_queue: List[Tuple[int, int, str, List[str]]] = [(0, 0, sta, [sta])]
        heapq.heapify(p_queue)

        d_tracker = {(graph.start_hub.name, 0): (0, 0)}

        while p_queue:
            curr = heapq.heappop(p_queue)
            curr_cost, curr_priority_count, curr_zone_name, curr_path = curr

            if curr_zone_name == graph.end_hub.name:
                return curr_path

            curr_state = (curr_cost, curr_priority_count)
            if (
                d_tracker.get((curr_zone_name, curr_cost), (float("inf"), 0))
                < curr_state
            ):
                continue
            else:
                d_tracker[curr_zone_name, curr_cost] = curr_state

            if self.res_table.ismax_drones(graph.zones[curr_zone_name],
                                           curr_cost + 1):
                if d_tracker.get((curr_zone_name, curr_cost + 1),
                                 (float("inf"), 0)) > (
                    curr_cost + 1,
                    curr_priority_count,
                ):
                    d_tracker[(curr_zone_name, curr_cost + 1)] = (
                        curr_cost + 1,
                        curr_priority_count,
                    )
                    heapq.heappush(
                        p_queue,
                        (
                            curr_cost + 1,
                            curr_priority_count,
                            curr_zone_name,
                            curr_path + [curr_zone_name],
                        ),
                    )

            for neighbor in graph.zones[curr_zone_name].connections:

                neighbor_zone = graph.zones[neighbor]
                if neighbor_zone.zone_type == ZoneTypes.BLOCKED:
                    continue
                if not self.res_table.ismax_link_capacity(
                    graph.zones[curr_zone_name], neighbor_zone, curr_cost + 1
                ):
                    continue

                if not self.res_table.ismax_drones(neighbor_zone,
                                                   curr_cost + 1):
                    continue

                if neighbor_zone.zone_type == ZoneTypes.RESTRICTED:
                    if not self.res_table.ismax_drones(neighbor_zone,
                                                       curr_cost + 2):
                        continue

                a = ZoneTypes.PRIORITY
                is_priority = (1 if neighbor_zone.zone_type == a else 0)
                new_priority_count = curr_priority_count - is_priority
                new_cost = curr_cost + self.zone_value[neighbor_zone.zone_type]

                n_state = (int(new_cost), new_priority_count)
                old_state = d_tracker.get(
                    (neighbor_zone.name, int(new_cost)), (float("inf"), 0)
                )

                if n_state < old_state:
                    d_tracker[(neighbor_zone.name, int(new_cost))] = n_state
                    duration = (
                        2 if neighbor_zone.zone_type == ZoneTypes.RESTRICTED
                        else 1
                    )
                    new_path = curr_path + ([neighbor_zone.name] * duration)
                    heapq.heappush(p_queue,
                                   (int(new_cost), new_priority_count,
                                    neighbor_zone.name,
                                    new_path))

        raise ValueError("No valid path exists between start and end zones")


def main() -> None:
    try:
        argparser: ArgumentParser = ArgumentParser()
        argparser.add_argument("--map", default="maper.txt")
        argparser.add_argument("--vis_type", default="terminal")
        args: Namespace = argparser.parse_args()

        map_file = args.map
        parser = Parser(map_file)
        graph = parser.maping()

        res_table = ReservationTable(graph)
        path_finder = Pathfinder(graph, res_table)

        torok_len = []
        torok = []
        for i in range(graph.nb_drones):
            route = path_finder.the_algo()
            torok.append(route)
            torok_len.append(len(route) - 1)
            res_table.book_path(route)

        vis_type = args.vis_type
        visualizer = Visualizer(vis_type, torok_len, torok, graph)
        visualizer.visualise()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
